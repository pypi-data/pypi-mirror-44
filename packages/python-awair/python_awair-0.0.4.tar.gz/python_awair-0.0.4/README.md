# python_awair

![Latest PyPI version](https://img.shields.io/pypi/v/python_awair.svg)
![Latest Travis CI build status](https://travis-ci.org/ahayworth/python_awair.png)
![Coveralls](https://coveralls.io/repos/github/ahayworth/python_awair/badge.svg?branch=master)

This is a WIP library to access the Awair API.
Features:
- uses graphql to access data (not sure if that's really a feature, but it's cool).
- async friendly!

Not yet supported:
- graphql mutations. There aren't docs on the developer site yet. We may implement them
  via REST.
- anything other than hobbyist-level endpoints (eg, no organizations)

Getting started:
- You'll need an access token from the [Awair Developer Console](https://developer.getawair.com/console). It's free.

Usage:

```python
from python_awair import AwairClient
import aiohttp
import asyncio

async def test_it():
  session = aiohttp.ClientSession()
  client = AwairClient('your_access_token', session=session)
  result = await client.air_data_latest("device_uuid")
  print(result)
  await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.ensure_future(test_it()))
loop.close()
```
