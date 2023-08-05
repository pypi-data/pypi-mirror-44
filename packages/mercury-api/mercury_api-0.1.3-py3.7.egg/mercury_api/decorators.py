# Copyright 2017 Ruben Quinones (ruben.quinones@rackspace.com)
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
from flask import request

from mercury_api.exceptions import HTTPError

log = logging.getLogger(__name__)


def validate_json(f):
    """
    Validates the request json body and headers when receiving a POST request.
    """

    def wrapper(*args, **kwargs):
        try:
            # If the application content type is not set then
            # request.json is None
            if not request.json:
                raise HTTPError(
                    'JSON request or mimetype is missing', status_code=400)
        except ValueError:
            body = request.body.read()
            log.debug('JSON request is malformed: {}'.format(body))
            raise HTTPError('JSON request is malformed', status_code=400)
        return f(*args, **kwargs)

    return wrapper


def check_query(f):
    """
    Validates that there is a query dictionary in the request body.
    """

    def wrapper(*args, **kwargs):
        if not isinstance(request.json.get('query'), dict):
            raise HTTPError('JSON request is malformed', status_code=400)
        return f(*args, **kwargs)

    return wrapper
