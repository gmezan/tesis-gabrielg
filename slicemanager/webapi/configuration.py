import environ
import os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ODL_IP = env('ODL_IP')
ODL_API_port = env('ODL_API_port')
ODL_BASE_URL = 'http://' + ODL_IP + ':' + ODL_API_port
ODL_user = env('ODL_user')
ODL_password = env('ODL_password')
ODL_switch_id = env('ODL_switch_id')

CONTROLLER_IP = env('CONTROLLER_IP')
COMPUTE_API_PORT = env('COMPUTE_API_PORT')
IDENTITY_API_PORT = env('IDENTITY_API_PORT')
IMAGE_API_PORT = env('IMAGE_API_PORT')
NETWORK_API_PORT = env('NETWORK_API_PORT')
PLACEMENT_API_PORT = env('PLACEMENT_API_PORT')
IMAGE_OPENSTACK = env('IMAGE_OPENSTACK')
FLAVOR_OPENSTACK = env('FLAVOR_OPENSTACK')

SLICE_MANAGER_IP = env('SLICE_MANAGER_IP')
SLICE_MANAGER_PORT = env('SLICE_MANAGER_PORT')
CYBERSECURITY_MODULE_IP = env('CYBERSECURITY_MODULE_IP')
CYBERSECURITY_MODULE_PORT = env('CYBERSECURITY_MODULE_PORT')

OS_USERNAME = env('OS_USERNAME')
OS_PASSWORD = env('OS_PASSWORD')
OS_USER_DOMAIN_ID = env('OS_USER_DOMAIN_ID')
OS_PROJECT_NAME = env('OS_PROJECT_NAME')
OS_PROJECT_DOMAIN_ID = env('OS_PROJECT_DOMAIN_ID')

OVS_NETWORK = env('OVS_NETWORK')
SRIOV_NETWORK = env('SRIOV_NETWORK')

MANAGEMENT_NET = env('MANAGEMENT_NET')
MANAGEMENT_NET_ID = env('MANAGEMENT_NET_ID')

KEY_PAIR_NAME = env('KEY_PAIR_NAME')

controller_openflow_port_dict = {}
computes_openflow_port_dict = {}

compute_availability_zone = env.list('COMPUTE_AVAILABILITY_ZONE')
aux_array = env.list('COMPUTE_OPENFLOW_PORT')

# Building computes_openflow_port_dict
assert len(aux_array) == len(compute_availability_zone)
for j in range(len(compute_availability_zone)):
    computes_openflow_port_dict[compute_availability_zone[j]] = aux_array[j]

# Building compute_availability_zone
for i in range(len(compute_availability_zone)):
    compute_availability_zone[i] = "nova:" + compute_availability_zone[i]


auth_data_admin = { "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "domain": { "id": OS_USER_DOMAIN_ID }, "name": OS_USERNAME, "password": OS_PASSWORD } } }, "scope": { "project": { "domain": { "id": OS_PROJECT_DOMAIN_ID }, "name": OS_PROJECT_NAME } } } }

security_group = { "security_group": { "name": "", "description": "" } }
sg_default_rules = { "security_group_rule": { "direction": "egress", "remote_ip_prefix": "", "security_group_id": "" } }

DELAY_WAIT_MS = 0.250