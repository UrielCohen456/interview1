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

After extensive testing and trying out different things, I could not get the ingress controller to succesfully pass the ip of the request and would always get the docker bridge network ip in the headers.
Example:
```
curl localhost
172.18.0.1
```
My theory is that because the kind cluster can only be setup on a bridge type of network on docker and not host network, any request to the cluster goes through docker and that makes it lose the original ip address.
Ideally the settings on the configmap of the ingress controller should work:
```use-forwarded-headers: "true"```
More can be read here: https://github.com/kubernetes/ingress-nginx/blob/main/docs/user-guide/nginx-configuration/configmap.md#forwarded-for-proxy-protocol-header
similar issue: https://github.com/kubernetes/ingress-nginx/issues/11994

perhaps k3d or another more customizable k8s deployment is configurable to allow the proper flow of networking, but due to limitations on time I will leave it as is for now.

to deploy the local test follow these steps:

1. kind create cluster --config infra/kind_config.yaml
2. kubectl apply -f infra/deploy-ingress-nginx.yaml
3. wait for controller to be running
4. helm upgrade --install app ./chart
5. wait for app the be running
6. curl localhost:80