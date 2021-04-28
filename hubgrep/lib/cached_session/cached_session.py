"""
A CachedSession wraps requests.Session, to conditionally retrieve cached responses when available,
or send a new request.

Note: All responses coming from a CachedSession are wrapped by CachedResponse, regardless if they were cached or not.
"""

import json
import logging
import requests
import hashlib
from typing import Union

from hubgrep.lib.cached_session.cached_response import CachedResponse
from hubgrep.lib.cached_session.caches.no_cache import NoCache
from hubgrep.lib.cached_session.caches.redis_cache import RedisCache

logger = logging.getLogger(__name__)

class CachedSession:
    """ Wrapper class for request session, caches results and exceptions. """
    def __init__(self, session: requests.Session, cache: Union[NoCache, RedisCache]):
        self.session = session
        self.cache = cache

    def make_key(self, method, url, *args, **kwargs):
        """ Make a unique hash from a request used as a key in the cache. """
        stringified_args = '_'.join(args)
        stringified_kwargs = json.dumps(kwargs, sort_keys=True)
        stringified = '_'.join([method, url, stringified_args, stringified_kwargs])
        request_hash = hashlib.sha1(stringified.encode()).hexdigest()
        return request_hash

    def request(self, method, url, *args, **kwargs) -> CachedResponse:
        """ Retrieve a cached request if available, or make an actual request. """
        key = self.make_key(method, url, *args, **kwargs)

        response_result_str = self.cache.get(key)
        if not response_result_str:
            try:
                logger.debug(f'request {method}, {url}, {args}, {kwargs}')
                response = self.session.request(method, url, *args, **kwargs)
                response_result = CachedResponse.from_response(response)

            except Exception as e:
                response_result = CachedResponse.from_exception(
                    url, exception_str=str(e)
                )
            self.cache.set(key, response_result.serialize())
            return response_result
        else:
            logger.debug("hit cache!")
            response_result = CachedResponse.from_serialized(response_result_str)
            return response_result

    def get(self, url, *args, **kwargs) -> CachedResponse:
        """ Send a GET request. """
        return self.request('get', url, *args, **kwargs)

    @property
    def headers(self):
        return self.session.headers

    @headers.setter
    def headers(self, value):
        self.session.headers = value
