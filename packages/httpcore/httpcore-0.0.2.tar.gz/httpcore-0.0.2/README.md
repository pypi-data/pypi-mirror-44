# HTTPCore

```python
import httpcore

response = await httpcore.request('GET', 'http://example.com')
assert response.status_code == 200
assert response.body == b'Hello, world'
```

Top-level API...

```python
response = await httpcore.request(method, url, [headers], [body], [stream])
```

Explicit PoolManager...

```python
async with httpcore.PoolManager([ssl], [timeout], [limits]) as pool:
    response = await pool.request(method, url, [headers], [body], [stream])
```

Streaming...

```python
response = await httpcore.request(method, url, stream=True)
async for part in response.stream():
    ...
```
