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
""" restible-swagger decorators. """
from __future__ import absolute_import, unicode_literals

# stdlib imports
from types import FunctionType
from typing import Any, Dict, List

# 3rd party imports
import attr

# local imports
from . import util


@attr.s
class RouteMeta(object):
    """ A helper class to store all the metadata about a given route.

    """
    responses = attr.ib(type=Dict[int, Any], default=None)
    route_params = attr.ib(type=List[Any], default=None)

    PARAM_NAME = '_restible_route_meta'

    def __attrs_post_init__(self):
        self.responses = self.responses or {}
        self.route_params = self.route_params or []

    def set_response(self, status_code, response_def):
        # type: (int, Dict[Text, Any]) -> None
        """ Set route response for the given HTTP status code. """
        self.responses[status_code] = response_def

    @classmethod
    def load(cls, fn):
        # type: (FunctionType) -> RouteMeta
        """ Load (or create) metadata for the given route.

        If the metadata is not yet saved on the handler, a new instance of
        `RouteMeta` will be created. You will need to save it manually in order
        for it to be persisted on the handler.
        """
        meta = getattr(fn, cls.PARAM_NAME, RouteMeta())
        meta.fn = fn
        return meta

    def save(self):
        # type: () -> None
        """ Save route metadata into the handler it was loaded for. """
        setattr(self.fn, self.PARAM_NAME, self)


def responses(resp_def):
    """ Define responses for the given handlers. """
    def decorator(fn):  # pylint: disable=missing-docstring
        meta = RouteMeta.load(fn)
        meta.responses = resp_def
        meta.save()
        return fn
    return decorator


def response(status, response_def):
    """ Define a single response for the given handler.

    You can define multiple responses for the given handler by using this
    decorator multiple times.
    """
    def decorator(fn):  # pylint: disable=missing-docstring
        meta = RouteMeta.load(fn)
        meta.set_response(status, response_def)
        meta.save()
        return fn
    return decorator


def response_200(description, array=False, schema=None):
    """ A standard HTTP 200 response

    A quick helper to easily define a standard 200 response where the response
    schema matches the main resource schema for any given restible resource.
    """
    return response(200, {
        "description": description,
        "schema": schema or ("__self_array__" if array else "__self__")
    })


def response_201(description, schema=None):
    """ A standard HTTP 201 response

    A quick helper to easily define a standard 201 response where the response
    schema matches the main resource schema for any given restible resource.
    """
    return response(201, {
        "description": description,
        "schema": schema or "__self__",
    })


def response_204(description=None):
    """ A standard HTTP 201 response

    A quick helper to easily define a standard 201 response where the response
    schema matches the main resource schema for any given restible resource.
    """
    description = description or "Item deleted"
    return response(204, {"description": description})


def response_401():
    """ A standard HTTP 401 response

    A quick helper for defining 401 responses. If you're using a custom error
    schema you'll have to build those manually. Otherwise you can use this
    little helper.
    """
    return response(401, util.RESPONSE_401)


def response_403():
    """ A standard HTTP 403 response

    A quick helper for defining 403 responses. If you're using a custom error
    schema you'll have to build those manually. Otherwise you can use this
    little helper.
    """
    return response(403, util.RESPONSE_403)


def response_404(description=None):
    """ A standard HTTP 404 response

    A quick helper for defining 404 responses. If you're using a custom error
    schema you'll have to build those manually. Otherwise you can use this
    little helper.
    """
    resp_def = dict(util.RESPONSE_404)
    if description is not None:
        resp_def['description'] = description

    return response(404, resp_def)


def route_params(params_def):
    """ Define route parameters.

    This allows you to define route params for any route. This allows to
    document the API at the finest level of detail.
    """
    def decorator(fn):  # pylint: disable=missing-docstring
        meta = RouteMeta.load(fn)
        meta.route_params = params_def
        meta.save()
        return fn

    return decorator


# Used only in type hint comments
del FunctionType
