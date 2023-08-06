# auth1api

auth1api provides methods to access your Auth1 instance.

Example Usage:
```python
client = Auth1Client("http://localhost:8080")
client.register("username", "hello@world.com", "foobar")
token, exp_time = client.login("username", None, None, "foobar")
if client.check_auth_token(token):
    print("Login success!")
else:
    print("Login failure.")
```