# auth1api

auth1api provides methods to access your Auth1 instance.

Example Usage:
```python
from auth1api import Auth1Client

client = Auth1Client("http://localhost:8080")
client.register("username", "hello@world.com", "foobar")
res = client.login("username", None, None, "foobar")
```