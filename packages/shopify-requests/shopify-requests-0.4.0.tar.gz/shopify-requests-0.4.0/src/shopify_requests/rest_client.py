from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

RATE_LIMIT_CODES = (429, 430)


class RestClient():
    """Create a session client for this Shopify store.

    :note:

    - Only `access_token` or (`username` and `password`) are required
    - urllib3 documents backoff_factor as
        - ``{backoff factor} * (2 ** ({number of total retries} - 1))``

    :param myshopify_domain: foobar.myshopify.com
    :param access_token: OAuth token from a pubilc app
    :param username: Username for private app
    :param password: Password for private app
    :param connect_retries: ``[default: 3]`` how many connection-related errors to retry on
    :param backoff_factor: ``[default: 0.5]`` how quickly to backoff for safe retries
    :param max_limit_retries: ``[default: 0]`` how many retries to do when rate limited
    :param limit_backoff_factor: ``[default: 0.5]`` same as backoff_factor but for rate limited
    :param version: ``[default: unstable]`` the Shopify API version to use
    """

    def __init__(
            self, myshopify_domain,
            access_token=None,
            username=None,
            password=None,
            connect_retries=None,
            backoff_factor=None,
            max_limit_retries=None,
            limit_backoff_factor=None,
            version=None,
    ):
        if connect_retries is None:
            connect_retries = 3
        if backoff_factor is None:
            backoff_factor = 0.5
        if max_limit_retries is None:
            max_limit_retries = 0
        if limit_backoff_factor is None:
            limit_backoff_factor = 0.5

        self.version = version or 'unstable'
        self.myshopify_domain = myshopify_domain
        if myshopify_domain is None:
            raise TypeError('myshopify_domain is required')

        self.session = requests.Session()
        if access_token:
            self.session.headers['X-Shopify-Access-Token'] = access_token
        elif username and password:
            self.session.auth = username, password
        else:
            msg = 'access_token or username and password are required'
            raise ValueError(msg)

        self.max_limit_retries = max_limit_retries
        self.limit_backoff_factor = limit_backoff_factor

        retry = Retry(
            total=None,  # fallback on other counts
            read=0,  # dont retry after data made it to the server
            connect=connect_retries,
            backoff_factor=backoff_factor,
            respect_retry_after_header=False,
            redirect=0,
        )
        adapter = HTTPAdapter(max_retries=retry)
        prefix = "https://{}/admin/api/{}/".format(self.myshopify_domain, self.version)
        self.session.mount(prefix, adapter)

        self.session.headers['Accept'] = 'application/json'

        self._usage = '0/40'

    def _url(self, url):
        return "https://{}/admin/api/{}/{}".format(self.myshopify_domain, self.version, url)

    def _within_limit(self, f):
        max_attempts = self.max_limit_retries + 1
        attempt = 0
        while attempt < max_attempts:
            resp = f()
            usage = resp.headers.get('X-Shopify-Shop-Api-Call-Limit')
            if usage is not None:
                self._usage = usage
            if resp.status_code not in RATE_LIMIT_CODES:
                break
            attempt += 1
            if attempt < max_attempts:
                tts = self.limit_backoff_factor * (2 ** (attempt - 1))
                sleep(tts)
        return resp

    def calls_used(self):
        """Return the number of API calls used.

        :rtype: int
        :see also: `Shopify API call limits`_

        .. _`Shopify API call limits`: https://help.shopify.com/en/api/getting-started/api-call-limit
        """
        return int(self._usage.split('/')[0])

    def calls_remaining(self):
        """Return the number of API calls remaining.

        :rtype: int
        :see also: `Shopify API call limits`_

        .. _`Shopify API call limits`: https://help.shopify.com/en/api/getting-started/api-call-limit
        """
        used, total = self._usage.split('/')
        remaining = int(total) - int(used)
        return remaining

    def max_available(self):
        """Return the bucket size for the token.

        :rtype: int
        :see also: `Shopify API call limits`_

        .. _`Shopify API call limits`: https://help.shopify.com/en/api/getting-started/api-call-limit
        """
        return int(self._usage.split('/')[1])

    def get(self, url, **kwargs):
        r"""Send a GET request.

        :param url: URL for the new Request object.
        :param \*\*kwargs: Optional arguments that session takes.
        :rtype: requests.Response
        :see also: requests.Session.get_.

        .. _requests.Session.get: http://docs.python-requests.org/en/master/api/#requests.Session.get
        """
        return self._within_limit(
            lambda: self.session.get(self._url(url), **kwargs)
        )

    def put(self, url, **kwargs):
        r"""Send a PUT request.

        :param url: URL for the new Request object.
        :param \*\*kwargs: Optional arguments that session takes.
        :rtype: requests.Response
        :see also: requests.Session.put_.

        .. _requests.Session.put: http://docs.python-requests.org/en/master/api/#requests.Session.put
        """
        return self._within_limit(
            lambda: self.session.put(self._url(url), **kwargs)
        )

    def post(self, url, **kwargs):
        r"""Send a POST request.

        :param url: URL for the new Request object.
        :param \*\*kwargs: Optional arguments that session takes.
        :rtype: requests.Response
        :see also: requests.Session.post_.

        .. _requests.Session.post: http://docs.python-requests.org/en/master/api/#requests.Session.post
        """
        return self._within_limit(
            lambda: self.session.post(self._url(url), **kwargs)
        )

    def patch(self, url, **kwargs):
        r"""Send a PATCH request.

        :param url: URL for the new Request object.
        :param \*\*kwargs: Optional arguments that session takes.
        :rtype: requests.Response
        :see also: requests.Session.patch_.

        .. _requests.Session.patch: http://docs.python-requests.org/en/master/api/#requests.Session.patch
        """
        return self._within_limit(
            lambda: self.session.patch(self._url(url), **kwargs)
        )

    def delete(self, url, **kwargs):
        r"""Send a DELETE request.

        :param url: URL for the new Request object.
        :param \*\*kwargs: Optional arguments that session takes.
        :rtype: requests.Response
        :see also: requests.Session.delete_.

        .. _requests.Session.delete: http://docs.python-requests.org/en/master/api/#requests.Session.delete
        """
        return self._within_limit(
            lambda: self.session.delete(self._url(url), **kwargs)
        )

    def close(self):
        """Close the session.

        :see also: requests.Session.close_.

        .. _requests.Session.close: http://docs.python-requests.org/en/master/api/#requests.Session.close
        """
        self.session.close()
