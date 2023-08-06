# HTTPCore

```python
import httpcore

http = httpcore.ConnectionPool()
response = await http.request('GET', 'http://example.com')
assert response.status_code == 200
assert response.body == b'Hello, world'
```

Top-level API...

```python
http = httpcore.ConnectionPool([ssl], [timeout], [limits])
response = await http.request(method, url, [headers], [body], [stream])
```

ConnectionPool as a context-manager...

```python
async with httpcore.ConnectionPool([ssl], [timeout], [limits]) as http:
    response = await http.request(method, url, [headers], [body], [stream])
```

Streaming...

```python
http = httpcore.ConnectionPool()
response = await http.request(method, url, stream=True)
async for part in response.stream():
    ...
```

The level of abstraction fits in really well if you're just writing at
the raw ASGI level. Eg. Here's an how an ASGI gateway server looks against the
API, including streaming uploads and downloads...

```python
import httpcore


class GatewayServer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.http = httpcore.ConnectionPool()

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        path = scope['path']
        query = scope['query_string']
        method = scope['method']
        headers = scope['headers']

        url = self.base_url + path
        if query:
            url += '?' + query.decode()

        async def body():
            nonlocal receive

            while True:
                message = await receive()
                yield message.get('body', b'')
                if not message.get('more_body', False):
                    break

        response = await self.http.request(
            method, url, headers=headers, body=body, stream=True
        )

        await send({
            'type': 'http.response.start',
            'status': response.status_code,
            'headers': response.headers
        })
        async for data in response.raw():
            await send({
                'type': 'http.response.body',
                'body': data,
                'more_body': True
            })
        await send({'type': 'http.response.body'})


app = GatewayServer('http://example.org')
```

Run with...

```shell
uvicorn example:app
```
