import kubernetes
from kubernetes import config
from lightkube import Client, KubeConfig
from lightkube.config.models import Cluster, User

CLIENT_HOST = "https://kubernetes.default.svc:443"
config.load_incluster_config()
# Create a custom configuration object to disable SSL verification
client_config = kubernetes.client.Configuration()

# Create a custom configuration object with the correct host name
client_config.host = CLIENT_HOST

# Load the service account token and create the API client
client_config.api_key = {
    "authorization": "Bearer "
    + open("/var/run/secrets/kubernetes.io/serviceaccount/token").read()
}
client_config.ssl_ca_cert = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"


def get_batch_client():
    return kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(client_config))

def get_apps_client():
    return kubernetes.client.AppsV1Api(kubernetes.client.ApiClient(client_config))

def get_core_api_client():
    return kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(client_config))

def get_lightkube_client():
    lightuser = User(token=open("/var/run/secrets/kubernetes.io/serviceaccount/token").read())
    lightcluster = Cluster(server=CLIENT_HOST, certificate_auth="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt")
    lightconfig = KubeConfig.from_one(cluster=lightcluster, user=lightuser)
    return Client(config=lightconfig)