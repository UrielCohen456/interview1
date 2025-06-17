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

In order to test the chart on a free Kubernetes cluster, I created a kind cluster that deploys an nginx controller and deployed the chart.

Now, since the nginx ingress is serving as a proxy, if you dont add the proxy headers a curl to the localhost application will yield the ip of the cluster bridge network.
Example:
```
curl localhost
172.18.0.1
```

So I modified the controller to forward proxy header 

to deploy the local test follow these steps:

1. kind create cluster --config infra/kind_config.yaml
2. kubectl apply -f infra/deploy-ingress-nginx.yaml
3. wait for controller to be running
4. helm upgrade --install app ./chart
5. wait for app the be running
6. curl localhost:80