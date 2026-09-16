import asyncio

import httpx2


class SyncASGIClient:
    def __init__(self, app):
        self.app = app

    def request(self, method, url, **kwargs):
        follow_redirects = kwargs.pop("follow_redirects", True)

        async def send_request():
            transport = httpx2.ASGITransport(app=self.app)
            async with httpx2.AsyncClient(
                transport=transport,
                base_url="http://testserver",
                follow_redirects=follow_redirects,
            ) as client:
                return await client.request(method, url, **kwargs)

        return asyncio.run(send_request())

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)
