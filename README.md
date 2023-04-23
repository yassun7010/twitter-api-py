# <p align="center">✨✨ Twitter API Client by Typed Python ✨✨</p>

<p align="center">
    <a href="https://github.com/yassun4dev/twitter-api-py/actions">
        <img src="https://github.com/yassun4dev/twitter-api-py/actions/workflows/test-suite.yml/badge.svg" alt="Test Suite">
    </a>
</p>

![demo](https://raw.githubusercontent.com/yassun4dev/twitter-api-py/main/images/demo.gif)

## Install

```sh
pip install twitter_api_py
```

## Features

- Fully type annotated.
- OAuth1 / OAuth2 support.
- Sync / Async Client support.
- Mock Client support.


## Usage
The simplest way to use the library is as follows:

As a characteristic feature of the library, it explicitly prompts the user to write the Endpoint URL, which makes it clear from the source code which Twitter API is being called.

```python
from twitter_api import TwitterApiClient

twitter_client = TwitterApiClient.from_oauth2_app_env()

response = (
    twitter_client.resource("https://api.twitter.com/2/tweets")
    .get({
        "ids": "1460323737035677698",
        "expansions": ["referenced_tweets.id"]
    })
)
```

## Test Code

A mock client is provided by the library to simplify the writing of test code.

This client has the same interface as TwitterApiClient/TwitterApiAsyncClient, and also provides methods (`inject_*_response_body`) for injecting test data.

```python
from twitter_api import TwitterApiClient
from twitter_api.client.twitter_api_mock_client import TwitterApiMockClient

def your_logic(twitter_client: TwitterApiClient):
    ...

def test_your_logic():
    twitter_client = (
        TwitterApiMockClient.from_oauth2_app_env()
        .inject_post_response_body("https://api.twitter.com/2/tweets", post_response)
        .inject_get_response_body("https://api.twitter.com/2/tweets/:id", get_response)
        .inject_delete_response_body("https://api.twitter.com/2/tweets", delete_response)
    )

    assert your_logic(twitter_client) is True
```


