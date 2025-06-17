# interview1

This app returns the ip of the requester.

By default this uses the default requests object to return the ip. If the app is behind a proxy, such as nginx in the case of a deployment to a cluster, the proxy should use the header "X-Forwarded-For".
In the case of nginx this can be set in the server block in this way:

```
location / {
    proxy_pass http://127.0.0.1:8000/; # the uvicorn server address
    proxy_set_header   Host             $host;
    proxy_set_header   X-Real-IP        $remote_addr;
    proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
}
```

I used the extension devcontainers to build and test the app.