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
""" OpenAPI spec generator for restible. """
from __future__ import absolute_import

# package interface
from .decorators import response
from .decorators import response_200
from .decorators import response_201
from .decorators import response_204
from .decorators import response_401
from .decorators import response_403
from .decorators import response_404
from .decorators import responses
from .decorators import route_params
from .logic import extract_api_spec
from .util import RESPONSE_401
from .util import RESPONSE_404
from .util import RESPONSE_500

__version__ = '0.3.2'
