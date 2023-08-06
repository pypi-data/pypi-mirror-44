# -*- coding: utf-8 -*-
# Copyright 2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
""" Endpoint builder. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
import textwrap

# 3rd party imports
from restible import ModelResource
from six import iteritems, string_types     # pylint: disable=wrong-import-order

# local imports
from . import util
from .decorators import RouteMeta


class EndpointBuilder(object):
    """ A helper class for building resource endpoints. """
    def __init__(self, route):
        self.route = route

    def actions_endpoint(self, actions):
        """ Extract spec for all action endpoints on the resource. """
        from restible import api_action

        res_cls = self.route.res_cls
        name = util.make_name(res_cls.name)
        endp = {}

        by_method = {}
        for action in actions:
            meta = api_action.get_meta(action)
            for method in meta.methods:
                by_method[method] = action

        for method, action in by_method.items():
            meta = api_action.get_meta(action)
            summary, desc = _parse_docstring(action)
            endp[method] = {
                "tags": [name],
                "summary": summary,
                "description": desc,
            }

            responses = self._get_responses(action, self_schema=meta.schema)
            if responses is not None:
                endp[method]['responses'] = responses

            if meta.schema:
                endp[method]['parameters'] = [{
                    "name": "payload",
                    "in": "body",
                    "schema": meta.schema,
                }]

        return endp

    def generic_endpoint(self):
        """ Extract spec for all generic endpoints on the resource. """
        res_cls = self.route.res_cls
        resource = res_cls()
        res_name = res_cls.name
        is_model_res = issubclass(res_cls, ModelResource)
        name = util.make_name(res_cls.name)
        endpoints = {}
        res_methods = {
            'create': 'create_item' if is_model_res else 'rest_create',
            'query': 'query_items' if is_model_res else 'rest_query',
        }

        if resource.implements('query'):
            res_method = getattr(res_cls, res_methods['query'])
            query_summary, query_desc = _parse_docstring(res_method)
            responses = self._get_responses(res_method, res_cls.schema, {
                "200": {
                    "description": "A list of {}s".format(res_name),
                    "schema": "__self_array__",
                },
                "401": util.RESPONSE_401
            })

            endpoints["get"] = {
                "tags": [name],
                "summary": query_summary,
                "description": query_desc,
                "responses": responses
            }

        if resource.implements('create'):
            res_method = getattr(res_cls, res_methods['create'])
            create_summary, create_desc = _parse_docstring(res_method)
            responses = self._get_responses(res_method, res_cls.schema, {
                "201": {
                    "description": "{} successfully created".format(name),
                    "schema": '__self__',
                },
                "401": util.RESPONSE_401
            })

            endpoints["post"] = {
                "tags": [name],
                "summary": create_summary,
                "description": create_desc,
                "parameters": [
                    {
                        "name": res_name,
                        "in": "body",
                        "description": "Initial {} data".format(res_name),
                        "schema": res_cls.schema,
                    }
                ],
                "responses": responses
            }

        return endpoints

    def detail_endpoint(self):
        """ Extract spec for all detail endpoints on the resource. """
        res_cls = self.route.res_cls
        resource = res_cls()
        res_name = res_cls.name
        is_model_res = issubclass(res_cls, ModelResource)
        name = util.make_name(res_cls.name)
        endpoints = {"parameters": res_cls.route_params}
        res_methods = {
            'get': 'get_item' if is_model_res else 'rest_get',
            'update': 'update_item' if is_model_res else 'rest_update',
            'delete': 'delete_item' if is_model_res else 'rest_delete',
        }

        if resource.implements('get'):
            res_method = getattr(res_cls, res_methods['get'])
            get_summary, get_desc = _parse_docstring(res_method)
            responses = self._get_responses(res_method, res_cls.schema, {
                "200": {
                    "description": "A list of {}s".format(res_name),
                    "schema": '__self_array__',
                },
                "401": util.RESPONSE_401,
                "404": util.RESPONSE_404
            })
            endpoints["get"] = {
                "tags": [name],
                "summary": get_summary,
                "description": get_desc,
                "responses": responses
            }

        if resource.implements('update'):
            res_method = getattr(res_cls, res_methods['update'])
            put_summary, put_desc = _parse_docstring(res_method)
            responses = self._get_responses(res_method, res_cls.schema, {
                "200": {
                    "description": "An updated {}".format(res_name),
                    "schema": '__self__',
                },
                "401": util.RESPONSE_401,
                "404": util.RESPONSE_404
            })
            endpoints["put"] = {
                "tags": [name],
                "summary": put_summary,
                "description": put_desc,
                "parameters": [
                    {
                        "name": res_name,
                        "in": "body",
                        "description": "{} data".format(res_name),
                        "schema": res_cls.schema,
                    }
                ],
                "responses": responses
            }

        if resource.implements('delete'):
            res_method = getattr(res_cls, res_methods['delete'])
            del_summary, del_desc = _parse_docstring(res_method)
            responses = self._get_responses(res_method, res_cls.schema, {
                "200": {"description": "Successfully deleted"},
                "401": util.RESPONSE_401,
                "404": util.RESPONSE_404
            })
            endpoints["delete"] = {
                "tags": [name],
                "summary": del_summary,
                "description": del_desc,
                "responses": responses,
            }

        return endpoints

    def _get_responses(self, handler, self_schema, defaults=None):
        route_meta = RouteMeta.load(handler)
        responses = route_meta.responses or defaults or {}

        for _, resp_spec in iteritems(responses):
            schema = resp_spec.get('schema', None)

            if isinstance(schema, string_types):
                if schema == '__self__':
                    resp_spec['schema'] = self_schema
                elif schema == '__self_array__':
                    resp_spec['schema'] = {
                        "type": "array",
                        "items": self_schema
                    }

        return responses


def _parse_docstring(obj):
    if obj.__doc__ is None:
        return None, None

    docstring = obj.__doc__.strip()
    parts = docstring.split('\n\n', 1)
    summary = parts[0]

    if len(parts) == 2:
        desc = parts[1]
    else:
        desc = parts[0]

    desc = textwrap.dedent(desc)

    return summary, desc
