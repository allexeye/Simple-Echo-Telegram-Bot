import logging
import warnings
import hashlib
import hmac
import time
from requests import Session

logger = logging.getLogger(__name__)


class RestfulApiClient(Session):

    def __init__(self, base_url,
                 auth=None, auth_class=None):
        super(RestfulApiClient, self).__init__()
        self.base_url = base_url
        if auth and auth_class:
            raise ValueError('You can not set both!')
        if auth_class:
            warnings.warn('auth_class is deprecated, please use auth instead.',
                          DeprecationWarning)
            self.auth = auth_class()
        if auth:
            self.auth = auth

    def request(self, method, url, **kwargs):
        response = super(RestfulApiClient, self).request(method, url, **kwargs)
        logger.debug(response.text)

        trace_id = None
        if 'x-trace-id' in response.headers:
            trace_id = response.headers['x-trace-id']
        logger.debug("sent to %s using method %s and %s - trace_id=%s",
                     url, method, kwargs, trace_id)

        return response


class HmacSignature(object):
    """
    HmacSignature class. Introduces the method for generation the
    HMAC signature hash basing on user, key and time.
    :param user: User name
    :param key: The pass key for appropriate user
    """

    def __init__(self, user, key):
        self.user = user
        self.key = key

    def generate(self, path, method, body='', timestamp=None):
        """
        The HMAC signature generator
        :param path: The resource path
        :param method: Method of the request
        :param body: Body of the request
        :param timestamp:
        :return: The HMAC signature hash
        """

        timestamp = timestamp or '%d' % (time.time(), )
        request_hash = ''.join([
            timestamp, method, path, hashlib.sha1(body).hexdigest()
        ])
        signature = hmac.new(self.key, request_hash, hashlib.sha1).hexdigest()
        return '{user}.{time}.{signature}'.format(
            user=self.user, time=timestamp, signature=signature)


class HmacSignatureAuth(object):
    """
    Class that implement the auth protocol as defined by Python
    Requests to sign requests to send using HMAC-SHA1.
    """
    user = 'test'
    secret_key = 'test'

    def __init__(self, user=None, secret_key=None):
        if user:
            self.user = user
            self.secret_key = secret_key
        self._hmac_signature = HmacSignature(self.user, self.secret_key)

    def __call__(self, req):
        if not req.headers.get('Authentication'):
            req.headers['Authentication'] = self._generate_signature(
                req.path_url, req.method, req.body or '')
        return req

    def _generate_signature(self, path, method, body):
        return self._hmac_signature.generate(path, method, body)
