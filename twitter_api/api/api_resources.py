from twitter_api.client.request.request_client import RequestClient


class ApiResources:
    def __init__(self, client: RequestClient) -> None:
        self._client = client

    @property
    def request_client(self) -> RequestClient:
        return self._client
