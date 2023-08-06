# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['shopify_requests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'shopify-requests',
    'version': '0.4.0',
    'description': 'Wrapper around the Shopify API using requests.',
    'long_description': "# Shopify Requests\n[![pipeline status](https://gitlab.com/perobertson/shopify-requests/badges/master/pipeline.svg)](https://gitlab.com/perobertson/shopify-requests/commits/master)\n[![coverage report](https://gitlab.com/perobertson/shopify-requests/badges/master/coverage.svg)](https://gitlab.com/perobertson/shopify-requests/commits/master)\n[![Documentation Status](https://readthedocs.org/projects/shopify-requests/badge/?version=latest)](https://shopify-requests.readthedocs.io/en/latest/?badge=latest)\n\nShopifyRequests is an API client for Shopify built on top of the [requests](http://docs.python-requests.org/en/master/) library.\n\nThe main goals of this project are:\n- remove boiler plate code needed to do a single API call\n- work well with testing libraries like VCR and RequestsMock\n- easy to use\n\nThere are also future plans to support `http2`, `asyncio`, and `GraphQL`.\n\n## Usage\n```python\nfrom shopify_requests import RestClient\n\nclient = RestClient('foo.myshopify.com', access_token='abc123')\nresponse = client.get('shop.json')\n```\nThe `RestClient` is the configuration point so that all requests made with it will have the same options.\nSome of the options you can configure are:\n- Oauth token vs private app token\n- API version\n- Safe retries\n- Rate limit backoff\n\nFor more configuration options check out the [API Docs](https://shopify-requests.readthedocs.io/en/latest/index.html#api-docs)\n\nAn additional benefits of using the same client is that it will reuse the same TCP connection so the SSL handshake only has to happen once.\n\n## Did you find a bug or have a question?\nThe [issue board](https://gitlab.com/perobertson/shopify-requests/issues) will be the best place to reach out and get the problem sorted out.\n",
    'author': 'Paul Robertson',
    'author_email': 't.paulrobertson@gmail.com',
    'url': 'https://gitlab.com/perobertson/shopify-requests',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
