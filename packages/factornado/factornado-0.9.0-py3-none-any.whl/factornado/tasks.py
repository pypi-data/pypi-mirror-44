# -*- coding: utf-8 -*-

from tornado import web, escape
import pandas as pd
import json
import bson
import pymongo
import logging

factornado_logger = logging.getLogger('factornado')


class SwaggerPath(str):
    """A simple class to overload str.format."""
    def format(self, uri, **kwargs):
        return super().format(
            uri=uri.replace("/([^/]*?)", ""), **kwargs)


def tansform_bson_id(y):
    x = {key: val for key, val in y.items()}
    x['id'] = str(x['id']) if x['id'] is not None else None
    return x


class Action(web.RequestHandler):
    swagger = {
        "path": SwaggerPath("/{name}/{uri}/{{task}}/{{key}}/{{action}}"),
        "operations": [
            {
                "notes": "Change a task status in applying an action.",
                "method": "PUT",
                "responseMessages": [
                    {"message": "OK", "code": 200},
                    {"message": "Unauthorized", "code": 401},
                    {"message": "Forbidden", "code": 403},
                    {"message": "Not Found", "code": 404}
                    ],
                "deprecated": False,
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "task",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someTask",
                        "description": "The task category."
                        },
                    {
                        "name": "key",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someKey",
                        "description": "The task key : it has to be unique."
                        },
                    {
                        "name": "action",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "stack",
                        "description": "The action to perform : delete|assign|success|stack|error."
                        },
                    {
                        "name": "body",
                        "paramType": "body",
                        "required": False,
                        "defaultValue": "{\"day\":\"2016-05-01\"}",
                        "description": "Data attached to the task."
                        }
                    ]
                }
            ]}

    def put(self, task, key, action):

        # Parse arguments
        priority = self.get_argument('priority', None)
        if priority is not None:
            try:
                priority = int(priority)
            except Exception:
                raise web.HTTPError(409, 'priority argument must be an int')

        # Parse data
        try:
            data = escape.json_decode(self.request.body) if len(self.request.body) else {}
        except Exception:
            raise web.HTTPError(
                501,
                reason="Bytes `{}...` are not JSON serializable".format(self.request.body[:30]))

        action = action.lower()
        if action not in self.application.config['actions']:
            raise web.HTTPError(
                411,
                reason="Action '{}' not understood. Expect {}.".format(
                    action, '|'.join(self.application.config['actions'])))
        _id = '/'.join([task, key])

        while True:
            before = self.application.mongo.tasks.find_one({'_id': _id})
            if before is None:
                before = {
                    '_id': _id,
                    'id': None,
                    'task': task,
                    'key': key,
                    'status': 'none',
                    'data': {},
                    'statusSince': None,
                    'try': 0,
                    'priority': 0,
                    }

            next_status = self.application.config['actions'][action].get(before['status'])
            if next_status is None:
                raise web.HTTPError(
                    411,
                    reason="Action '{}' cannot be performed on status '{}'.".format(
                        action, before['status']))
            after = {
                '_id': _id,
                'id': before['id'],
                'task': task,
                'key': key,
                'status': next_status,
                'data': dict(before['data'].copy(), **data),
                'statusSince': (
                    before['statusSince'] if next_status == before['status']
                    else pd.Timestamp.utcnow().value),
                'try': before['try'] + (action == 'error'),
                'priority': priority if priority is not None else before.get('priority')
                }

            changed = (json.dumps(tansform_bson_id(before), sort_keys=True) !=
                       json.dumps(tansform_bson_id(after), sort_keys=True))
            if changed:
                if after['status'] == 'none':
                    change = self.application.mongo.tasks.delete_one({'_id': _id,
                                                                      'id': before['id']})
                    count = change.deleted_count
                    assert change.raw_result['ok']
                elif before['status'] == 'none':
                    factornado_logger.debug('Will insert')
                    after['id'] = bson.ObjectId()
                    try:
                        self.application.mongo.tasks.insert_one(after)
                        count = 1
                    except pymongo.errors.DuplicateKeyError:
                        count = 0
                else:
                    after['id'] = bson.ObjectId()
                    change = self.application.mongo.tasks.replace_one(
                        {'_id': _id, 'id': before['id']}, after, upsert=False)
                    count = change.modified_count
                    assert change.raw_result['ok']

                if count == 0:
                    # Someone came before
                    if action == 'assign':
                        # Cannot assign the task if someone came before.
                        self.set_status(204, reason='No task to do')
                    else:
                        # You can perform the action ; let's try again.
                        pass
                else:
                    # We got the right to write
                    self.write({
                            'changed': changed,
                            'before': tansform_bson_id(before),
                            'after': tansform_bson_id(after)})
                    break
            else:
                # We had nothing to write
                self.write({'changed': changed,
                            'before': tansform_bson_id(before),
                            'after': tansform_bson_id(after)})
                break


class Force(web.RequestHandler):
    swagger = {
        "path": SwaggerPath("/{name}/{uri}/{{task}}/{{key}}/{{status}}"),
        "operations": [
            {
                "notes": "Force a task status.",
                "method": "PUT",
                "responseMessages": [
                    {"message": "OK", "code": 200},
                    {"message": "Unauthorized", "code": 401},
                    {"message": "Forbidden", "code": 403},
                    {"message": "Not Found", "code": 404},
                    {"message": "Not Found", "code": 409},
                    {"message": "Task unknown", "code": 410},
                    {"message": "data is not JSON", "code": 501}
                    ],
                "deprecated": False,
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "task",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someTask",
                        "description": "The task category."
                        },
                    {
                        "name": "key",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someKey",
                        "description": "The task key : it has to be unique."
                        },
                    {
                        "name": "status",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "todo",
                        "description": "The status to be set : done|toredo|fail|todo|doing|none."
                        },
                    {
                        "name": "body",
                        "paramType": "body",
                        "required": False,
                        "defaultValue": "{\"day\":\"2016-05-01\"}",
                        "description": "Data attached to the task."
                        }
                    ]
                }
            ]}

    def put(self, task, key, status):
        # Parse arguments
        priority = self.get_argument('priority', None)
        if priority is not None:
            try:
                priority = int(priority)
            except Exception:
                raise web.HTTPError(409, 'priority argument must be an int')

        # Parse data
        try:
            data = escape.json_decode(self.request.body) if len(self.request.body) else {}
        except Exception:
            raise web.HTTPError(
                501,
                reason="Bytes `{}...` are not JSON serializable".format(self.request.body[:30]))

        status = status.lower()
        if status not in self.application.config['actions']['delete']:
            raise web.HTTPError(
                411,
                reason="Status '{}' not understood. Expect {}.".format(
                    status, '|'.join(self.application.config['actions']['delete'])))
        _id = '/'.join([task, key])
        before = self.application.mongo.tasks.find_one({'_id': _id})
        if before is None:
            before = {
                '_id': _id,
                'id': None,
                'task': task,
                'key': key,
                'status': 'none',
                'data': {},
                'statusSince': None,
                'try': 0,
                'priority': 0,
                }

        after = {
            '_id': _id,
            'id': before['id'],
            'task': task,
            'key': key,
            'status': status,
            'data': dict(before['data'].copy(), **data),
            'statusSince': (
                before['statusSince'] if status == before['status']
                else pd.Timestamp.utcnow().value),
            'try': before['try'],
            'priority': priority if priority is not None else before.get('priority')
            }
        changed = (json.dumps(tansform_bson_id(before), sort_keys=True) !=
                   json.dumps(tansform_bson_id(after), sort_keys=True))

        if changed:
            if after['status'] == 'none':
                change = self.application.mongo.tasks.delete_one({'_id': _id})
            else:
                after['id'] = bson.ObjectId()
                change = self.application.mongo.tasks.replace_one(
                    {'_id': _id}, after, upsert=True)
            assert change.raw_result['ok']

        self.write({'changed': changed,
                    'before': tansform_bson_id(before),
                    'after': tansform_bson_id(after)})


class AssignOne(web.RequestHandler):
    swagger = {
        "path": SwaggerPath("/{name}/{uri}/{{task}}"),
        "operations": [
            {
                "notes": "Pick a task that has not been done yet, and assign it.",
                "method": "PUT",
                "responseMessages": [
                    {"message": "OK", "code": 200},
                    {"message": "No task to do", "code": 204},
                    {"message": "Unauthorized", "code": 401},
                    {"message": "Forbidden", "code": 403},
                    {"message": "Not Found", "code": 404},
                    {"message": "Not Found", "code": 409},
                    {"message": "Task unknown", "code": 410}
                    ],
                "deprecated": False,
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "task",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someTask",
                        "description": "The taskname category."
                        }
                    ]
                }
            ]}

    def put(self, task):
        while True:
            cursor = self.application.mongo.tasks.find(
                {'status': 'todo', 'task': task},
                sort=[('priority', -1), ('ldt', 1)])
            yielded = 0
            for todo in cursor:
                r = self.application.mongo.tasks.update_one(
                    {'_id': todo['_id'], 'id': todo['id']},
                    {'$set': {
                            'status': 'doing',
                            'statusSince': pd.Timestamp.utcnow().value,
                            'id': bson.ObjectId(),
                        }})
                if r.modified_count == 1:
                    self.write(pd.io.json.dumps(tansform_bson_id(todo)))
                    yielded = 1
                    break
                else:
                    # Someone got this one before. Let's try another one
                    pass

            if yielded == 1:
                # We got a task. It's finished
                break
            elif cursor.retrieved == 0:
                # There where no task to do.
                self.set_status(204, reason='No task to do')
                break
            else:
                # There where tasks, but they where all got by someone else.
                # Let's retry
                pass


class GetByKey(web.RequestHandler):
    swagger = {
        "path": SwaggerPath("/{name}/{uri}/{{task}}/{{key}}"),
        "operations": [
            {
                "notes": "Get a task with given key (alter nothing).",
                "method": "GET",
                "responseMessages": [
                    {"message": "OK", "code": 200},
                    {"message": "No task matching", "code": 204},
                    {"message": "Unauthorized", "code": 401},
                    {"message": "Forbidden", "code": 403},
                    {"message": "Not Found", "code": 404},
                    {"message": "Not Found", "code": 409},
                    {"message": "Task unknown", "code": 410},
                    {"message": "Task unknown", "code": 411},
                    {"message": "Task unknown", "code": 412}
                    ],
                "deprecated": False,
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "task",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someTask",
                        "description": "The task category."
                        },
                    {
                        "name": "key",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someKey",
                        "description": "The task key : it has to be unique."
                        }
                    ]
                }
            ]}

    def get(self, task, key):
        todo = self.application.mongo.tasks.find_one({'key': key, 'task': task})
        if todo is None:
            self.set_status(204, reason='No task matching')
        else:
            self.write(pd.io.json.dumps(tansform_bson_id(todo)))


class GetByStatus(web.RequestHandler):
    swagger = {
        "path": SwaggerPath("/{name}/{uri}/{{task}}/{{status}}"),
        "operations": [
            {
                "notes": "Get tasks with given status (alter nothing).",
                "method": "GET",
                "responseMessages": [
                    {"message": "OK", "code": 200},
                    {"message": "Unauthorized", "code": 401},
                    {"message": "Forbidden", "code": 403},
                    {"message": "Not Found", "code": 404},
                    {"message": "Not Found", "code": 409},
                    {"message": "Task unknown", "code": 410},
                    {"message": "Task unknown", "code": 411},
                    {"message": "Task unknown", "code": 412}
                    ],
                "deprecated": False,
                "produces": ["application/json"],
                "parameters": [
                    {
                        "name": "task",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "someTask",
                        "description": "The task category."
                        },
                    {
                        "name": "status",
                        "type": "string",
                        "format": None,
                        "paramType": "path",
                        "required": True,
                        "defaultValue": "done,doing",
                        "description": "The status searched: done|toredo|fail|todo|doing|none."
                        }
                    ]
                }
            ]}

    def get(self, task, status_list):
        status_list = escape.url_unescape(status_list.lower()).split(',')
        self.write(pd.io.json.dumps(
            {status: list(map(tansform_bson_id,
                              self.application.mongo.tasks.find({'status': status,
                                                                 'task': task})))
             for status in status_list}))
