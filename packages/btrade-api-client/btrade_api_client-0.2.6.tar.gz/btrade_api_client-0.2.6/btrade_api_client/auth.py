"""
Request signing library for the Bit Trade API client
"""
import datetime
import base64
import hashlib
import hmac

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class Auth:
    """
    Request signing library for the Bit Trade API client
    """
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key.encode('ascii')

    def __call__(self, request):
        method = request.method
        content_type = request.headers.get('content-type')
        if content_type and isinstance(content_type, bytes):
            content_type = content_type.decode('utf-8')
        if not content_type:
            content_type = ''

        content_md5 = request.headers.get('content-md5')
        if not content_md5:
            if request.body != None and request.body != "":
                md5_hash = hashlib.md5()
                md5_hash.update(request.body.encode('utf-8'))
                content_md5 = base64.encodebytes(md5_hash.digest()).rstrip().decode('utf-8')
            else:
                content_md5 = ''
        httpdate = request.headers.get('date')
        if not httpdate:
            now = datetime.datetime.utcnow()
            httpdate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
            request.headers['Date'] = httpdate

        url = urlparse(request.url)
        path = url.path
        if url.query:
            path = path + "?" + url.query
        string_to_sign = '\n'.join([method, content_md5, content_type, httpdate, path])\
            .encode('utf-8')
        digest = hmac.new(self.secret_key, string_to_sign, hashlib.sha256).digest()
        signature = base64.encodebytes(digest).rstrip().decode('utf-8')

        if self.access_key == '':
            request.headers['Authorization'] = 'HMAC %s' % signature
        elif self.secret_key == '':
            raise ValueError('HMAC secret key cannot be empty.')
        else:
            request.headers['Authorization'] = 'HMAC %s:%s' % (self.access_key, signature)
        return request
