from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from random import randrange

import requests
import json
import copy
import uuid
import random

ODL_IP = '10.0.0.1'
ODL_API_port = '8181'
ODL_BASE_URL = 'http://' + ODL_IP + ':' + ODL_API_port
ODL_user = 'admin'
ODL_password = 'admin'
ODL_switch_id = '431646109239664'

CONTROLLER_IP = '10.0.0.1'
COMPUTE_API_PORT = '8774'
IDENTITY_API_PORT = '5000'
IMAGE_API_PORT = '9292'
NETWORK_API_PORT = '9696'
PLACEMENT_API_PORT = '8778'
IMAGE_OPENSTACK = "01fbec27-00c6-4ed0-ad7b-3cab1db9aecf"
FLAVOR_OPENSTACK = "60f6b74d-4a46-45ef-ab38-827e10d046ab"

SLICE_MANAGER_IP = '10.0.0.1'
SLICE_MANAGER_PORT = '8000'
CYBERSECURITY_MODULE_IP = '10.0.0.1'
CYBERSECURITY_MODULE_PORT = '8001'

controller_openflow_port_dict = { "dev-head-node_openflow_port": "6" }
computes_openflow_port_dict = { "worker-1_openflow_port": "7", "worker-2_openflow_port": "8"}

compute_availability_zone = ["nova:worker-1", "nova:worker-2"]

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

auth_data_admin = { "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "domain": { "id": "default" }, "name": "admin", "password": "openstack" } } }, "scope": { "project": { "domain": { "id": "default" }, "name": "admin" } } } }

security_group = { "security_group": { "name": "", "description": "" } }
sg_default_rules = { "security_group_rule": { "direction": "egress", "remote_ip_prefix": "", "security_group_id": "" } }
def return_sg_default_rules():
    return { "security_group_rule": { "direction": "egress", "remote_ip_prefix": "", "security_group_id": "" } }
def return_all_tcp_sg_rule():
    return { "security_group_rule": { "direction": "ingress", "protocol": "tcp", "remote_ip_prefix": "", "security_group_id": "" } }
def return_tcp_port_sg_rule():
    return { "security_group_rule": { "direction": "ingress", "port_range_min": "", "port_range_max": "", "protocol": "tcp", "remote_ip_prefix": "", "security_group_id": "" } }
def return_set_unset_sg_to_port():
    return { "port": { "security_groups": [] } }
def return_create_router():
    return { "router": { "name": "", "external_gateway_info": { "network_id": "" } } }
def return_config_interface_router():
    return { "subnet_id": "" }
def return_remote_sg_rule():
    return { "security_group_rule": { "direction": "ingress", "ethertype": "IPv4", "remote_group_id": "", "security_group_id": "" } }

def return_create_net():
    return { "network": { "name": "", "provider:network_type": "vlan", "provider:physical_network": "" } }
def return_create_subnet():
    return { "subnet": { "name": "", "network_id": "", "ip_version": "4", "cidr": "", "enable_dhcp": "", "dns_nameservers": [ "8.8.8.8", "8.8.8.4" ] } }
def return_create_subnet_without_gateway():
    return { "subnet": { "name": "", "network_id": "", "ip_version": "4", "cidr": "", "enable_dhcp": "", "gateway_ip": None, "dns_nameservers": [ "8.8.8.8", "8.8.8.4" ] } }
def return_create_port():
    return { "port": { "name": "", "network_id": "" } }
def return_create_direct_port():
    return { "port": { "name": "", "network_id": "", "binding:vnic_type": "direct" } }

def return_create_server():
    return { "server": { "name": "", "imageRef": "", "flavorRef": "", "key_name": "testkey", "availability_zone": "", "networks": [{ "port": "" }, { "port": "" }] } }

def return_access_flow():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "500", "hard-timeout": "0", "idle-timeout": "0", "match": { "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": "0", "apply-actions": { "action": [ { "order": "0", "output-action": { "output-node-connector": "ALL" } } ] } } ] } } ] }
def return_mgnt_flow_type1():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "in-port": "openflow::", "ethernet-match": { "ethernet-source": { "address": "" }, "ethernet-destination": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "output-action": { "output-node-connector": "" } } ] } } ] } } ] }
def return_mgnt_flow_type2():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "in-port": "", "ethernet-match": { "ethernet-source": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "group-action": { "group": "", "group-id": "" } } ] } } ] } } ] }
def return_mgnt_flow_type3():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "in-port": "openflow::", "ethernet-match": { "ethernet-source": { "address": "" }, "ethernet-destination": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "output-action": { "output-node-connector": "" } } ] } } ] } } ] }
def return_mgnt_flow_type4():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "ethernet-match": { "ethernet-destination": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "drop-action": {} } ] } } ] } } ] }
def return_mgnt_flow_type5():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "in-port": "", "ethernet-match": { "ethernet-source": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "group-action": { "group": "", "group-id": "" } } ] } } ] } } ] }
def return_data_flow_type1():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "in-port": "openflow::", "ethernet-match": { "ethernet-source": { "address": "" }, "ethernet-destination": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "output-action": { "output-node-connector": "" } } ] } } ] } } ] }
def return_data_flow_type2():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "in-port": "", "ethernet-match": { "ethernet-source": { "address": "" } }, "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "group-action": { "group": "", "group-id": "" } } ] } } ] } } ] }
def return_default_vlan_drop_flow():
    return { "flow": [ { "table_id": "0", "id": "", "priority": "", "match": { "vlan-match": { "vlan-id": { "vlan-id": "", "vlan-id-present": "true" } } }, "instructions": { "instruction": [ { "order": 0, "apply-actions": { "action": [ { "order": 0, "drop-action": {} } ] } } ] } } ] }

def return_group_table():
    return { "flow-node-inventory:group": [ { "group-id": "", "barrier": "false", "group-name": "", "buckets": { "bucket": [] }, "group-type": "group-all" } ] }
def return_bucket():
    return { "bucket-id": "", "action": [ { "order": "0", "output-action": { "output-node-connector": "" } } ] }

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

""" HANDLE CLIENT REQUEST - CREATE HPC SLICE """

@csrf_exempt
def handle_client_create_request(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)
        cant_masters = int(json_req_body['cant_masters'])
        cant_workers = int(json_req_body['cant_workers'])
        access_network_info = json_req_body['access_network']

        slice_id = create_slice_hpc(cant_masters, cant_workers)

        slice_mgnt_data_net_info = generate_slice_mgnt_data_net_info(slice_id, cant_masters, cant_workers)

        slice_info = {
            "slice_id": slice_id,
            "access_network": access_network_info,
            "management_network": slice_mgnt_data_net_info['management_network'],
            "data_network": slice_mgnt_data_net_info['data_network']
        }
        print("var slice_info ---> " + str(slice_info))

        r = requests.post('http://' + SLICE_MANAGER_IP + ':' + SLICE_MANAGER_PORT + "/slicemanager/request-apply-security", json = slice_info)

        return HttpResponse(str(slice_info))

""" HANDLE CLIENT REQUEST - DELETE HPC SLICE """

@csrf_exempt
def handle_client_delete_request(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)
        slice_id = json_req_body['slice_id']
        cant_masters = int(json_req_body['cant_masters'])
        cant_workers = int(json_req_body['cant_workers'])

        slice_mgnt_data_net_info = generate_slice_mgnt_data_net_info(slice_id, cant_masters, cant_workers)

        slice_info = {
            "slice_id": slice_id,
            "management_network": slice_mgnt_data_net_info['management_network'],
            "data_network": slice_mgnt_data_net_info['data_network']
        }
        print("var slice_info ---> " + str(slice_info))

        r = requests.post('http://' + SLICE_MANAGER_IP + ':' + SLICE_MANAGER_PORT + "/slicemanager/request-remove-security", json = slice_info)

        delete_slice_hpc(slice_id, cant_masters, cant_workers)

        return HttpResponse(str(slice_info))

def create_slice_hpc(cant_masters, cant_workers):

    slice_id_uuid = uuid.uuid4()
    slice_id = str(slice_id_uuid)

    token = generate_token()

    """ CREAR REDES """

    json_create_net = return_create_net()
    json_create_net['network']['name'] = slice_id + '_cluster_access_net'
    json_create_net['network']['provider:physical_network'] = 'provider'
    print("Sending post...")
    r_create_access_net = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks", json = json_create_net, headers = { 'X-Auth-Token': token })
    
    r_dict_create_access_net = json.loads(r_create_access_net.text)
    access_net_id = r_dict_create_access_net['network']['id']

    json_create_net = return_create_net()
    json_create_net['network']['name'] = slice_id + '_cluster_mgnt_net'
    json_create_net['network']['provider:physical_network'] = 'provider'
    json_create_net['network']['port_security_enabled'] = 'false'
    r_create_mgnt_net = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks", json = json_create_net, headers = { 'X-Auth-Token': token })
    r_dict_create_mgnt_net = json.loads(r_create_mgnt_net.text)
    mgnt_net_id = r_dict_create_mgnt_net['network']['id']
    mgnt_net_vlan = str(r_dict_create_mgnt_net['network']['provider:segmentation_id'])

    json_create_net = return_create_net()
    json_create_net['network']['name'] = slice_id + '_cluster_data_net'
    json_create_net['network']['provider:physical_network'] = 'provider'
    json_create_net['network']['port_security_enabled'] = 'false'
    r_create_data_net = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks", json = json_create_net, headers = { 'X-Auth-Token': token })
    r_dict_create_data_net = json.loads(r_create_data_net.text)
    data_net_id = r_dict_create_data_net['network']['id']
    data_net_vlan = str(r_dict_create_data_net['network']['provider:segmentation_id'])

    """ CREAR SUBREDES """

    json_create_subnet = return_create_subnet()
    json_create_subnet['subnet']['name'] = slice_id + '_cluster_access_subnet'
    json_create_subnet['subnet']['network_id'] = access_net_id
    json_create_subnet['subnet']['cidr'] = '10.' + str(randrange(1,254)) + '.' + str(randrange(1,254)) + '.0/24'
    json_create_subnet['subnet']['enable_dhcp'] = 'true'
    r_create_access_subnet = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/subnets", json = json_create_subnet, headers = { 'X-Auth-Token': token })
    r_dict_create_access_subnet = json.loads(r_create_access_subnet.text)
    access_subnet_id = r_dict_create_access_subnet['subnet']['id']

    json_create_subnet = return_create_subnet_without_gateway()
    json_create_subnet['subnet']['name'] = slice_id + '_cluster_mgnt_subnet'
    json_create_subnet['subnet']['network_id'] = mgnt_net_id
    json_create_subnet['subnet']['cidr'] = '10.' + str(randrange(1,254)) + '.' + str(randrange(1,254)) + '.0/24'
    json_create_subnet['subnet']['enable_dhcp'] = 'true'
    r_create_mgnt_subnet = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/subnets", json = json_create_subnet, headers = { 'X-Auth-Token': token })
    r_dict_create_mgnt_subnet = json.loads(r_create_mgnt_subnet.text)
    mgnt_subnet_id = r_dict_create_mgnt_subnet['subnet']['id']

    json_create_subnet = return_create_subnet_without_gateway()
    json_create_subnet['subnet']['name'] = slice_id + '_cluster_data_subnet'
    json_create_subnet['subnet']['network_id'] = data_net_id
    json_create_subnet['subnet']['cidr'] = '10.' + str(randrange(1,254)) + '.' + str(randrange(1,254)) + '.0/24'
    json_create_subnet['subnet']['enable_dhcp'] = 'true'
    r_create_data_subnet = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/subnets", json = json_create_subnet, headers = { 'X-Auth-Token': token })
    r_dict_create_data_subnet = json.loads(r_create_data_subnet.text)
    data_subnet_id = r_dict_create_data_subnet['subnet']['id']

    """ CREAR PUERTOS """

    access_master_ports_ids = []
    for i in range(cant_masters):
        access_port_master_name = slice_id + '_cluster_master' + str(i) + '_access_port'                
        json_port = return_create_port()
        json_port['port']['name'] = access_port_master_name
        json_port['port']['network_id'] = access_net_id
        r_create_port = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports", json = json_port, headers = { 'X-Auth-Token': token })
        r_dict_create_port = json.loads(r_create_port.text)
        access_master_port_id = r_dict_create_port['port']['id']
        access_master_ports_ids.append(access_master_port_id)

    mgnt_master_ports_ids = []
    for i in range(cant_masters):
        mgnt_port_master_name = slice_id + '_cluster_master' + str(i) + '_mgnt_port'                
        json_port = return_create_direct_port()
        json_port['port']['name'] = mgnt_port_master_name
        json_port['port']['network_id'] = mgnt_net_id
        r_create_port = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports", json = json_port, headers = { 'X-Auth-Token': token })
        r_dict_create_port = json.loads(r_create_port.text)
        mgnt_master_port_id = r_dict_create_port['port']['id']
        mgnt_master_ports_ids.append(mgnt_master_port_id)

    mgnt_worker_ports_ids = []
    for i in range(cant_workers):
        mgnt_port_worker_name = slice_id + '_cluster_worker' + str(i) + '_mgnt_port'                
        json_port = return_create_direct_port()
        json_port['port']['name'] = mgnt_port_worker_name
        json_port['port']['network_id'] = mgnt_net_id
        r_create_port = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports", json = json_port, headers = { 'X-Auth-Token': token })
        r_dict_create_port = json.loads(r_create_port.text)
        mgnt_worker_port_id = r_dict_create_port['port']['id']
        mgnt_worker_ports_ids.append(mgnt_worker_port_id)

    data_worker_ports_ids = []
    for i in range(cant_workers):
        data_port_worker_name = slice_id + '_cluster_worker' + str(i) + '_data_port'                
        json_port = return_create_direct_port()
        json_port['port']['name'] = data_port_worker_name
        json_port['port']['network_id'] = data_net_id
        r_create_port = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports", json = json_port, headers = { 'X-Auth-Token': token })
        r_dict_create_port = json.loads(r_create_port.text)
        data_worker_port_id = r_dict_create_port['port']['id']
        data_worker_ports_ids.append(data_worker_port_id)

    """ CREAR ROUTER """

    # Se cambia external_provider por provider1
    r_external_provider_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks?name=external_provider", headers = { 'X-Auth-Token': token })
    r_dict_external_provider_net = json.loads(r_external_provider_net.text)
    external_provider_net_id = r_dict_external_provider_net['networks'][0]['id']

    json_router = return_create_router()
    json_router['router']['name'] = slice_id + '_cluster_router'
    json_router['router']['external_gateway_info']['network_id'] = external_provider_net_id
    r_create_router = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/routers", json = json_router, headers = { 'X-Auth-Token': token })
    r_dict_create_router = json.loads(r_create_router.text)
    print(str(r_dict_create_router))
    router_id = r_dict_create_router['router']['id']

    json_config_interface_router = return_config_interface_router()
    json_config_interface_router['subnet_id'] = access_subnet_id
    r_config_interface_router = requests.put('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/routers/" + router_id + "/add_router_interface", json = json_config_interface_router, headers = { 'X-Auth-Token': token })

    """ CREAR VMs """

    for index, (access_master_port_id, mgnt_master_port_id) in enumerate(zip(access_master_ports_ids, mgnt_master_ports_ids)):
        json_master_server = return_create_server()
        json_master_server['server']['name'] = slice_id + '_cluster_master' + str(index)
        json_master_server['server']['imageRef'] = IMAGE_OPENSTACK
        json_master_server['server']['flavorRef'] = FLAVOR_OPENSTACK

        if (index % 3) == 0:
            json_master_server['server']['availability_zone'] = "nova:worker-1"
        elif (index % 3) == 1:
            json_master_server['server']['availability_zone'] = "nova:worker-2"
        else:
            json_master_server['server']['availability_zone'] = "nova:worker-3"

        json_master_server['server']['networks'][0]['port'] = access_master_port_id
        json_master_server['server']['networks'][1]['port'] = mgnt_master_port_id

        r = requests.post('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + "/v2.1/servers", json = json_master_server, headers = { 'X-Auth-Token': token })

    for index, (mgnt_worker_port_id, data_worker_port_id) in enumerate(zip(mgnt_worker_ports_ids, data_worker_ports_ids)):
        json_worker_server = return_create_server()
        json_worker_server['server']['name'] = slice_id + '_cluster_worker' + str(index)
        json_worker_server['server']['imageRef'] = IMAGE_OPENSTACK
        json_worker_server['server']['flavorRef'] = FLAVOR_OPENSTACK

        if (index % 3) == 0:
            json_worker_server['server']['availability_zone'] = "nova:worker-1"
        elif (index % 3) == 1:
            json_worker_server['server']['availability_zone'] = "nova:worker-2"
        else:
            json_worker_server['server']['availability_zone'] = "nova:worker-3"

        json_worker_server['server']['networks'][0]['port'] = mgnt_worker_port_id
        json_worker_server['server']['networks'][1]['port'] = data_worker_port_id

        r = requests.post('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + "/v2.1/servers", json = json_worker_server, headers = { 'X-Auth-Token': token })
        print(str(json.loads(r.text)))
    return slice_id

def delete_slice_hpc(slice_id, cant_masters, cant_workers):
    token = generate_token()

    """ ELIMINAR VMs """

    for i in range(cant_masters):
        r_get_master = requests.get('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/detail?name=' + slice_id + '_cluster_master' + str(i), headers = { 'X-Auth-Token': token })
        r_dict_master = json.loads(r_get_master.text)
        master_id = r_dict_master['servers'][0]['id']
        r_delete_master = requests.delete('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/' + master_id, headers = { 'X-Auth-Token': token })

    for i in range(cant_workers):
        r_get_worker = requests.get('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/detail?name=' + slice_id + '_cluster_worker' + str(i), headers = { 'X-Auth-Token': token })
        r_dict_worker = json.loads(r_get_worker.text)
        worker_id = r_dict_worker['servers'][0]['id']
        r_delete_worker = requests.delete('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/' + worker_id, headers = { 'X-Auth-Token': token })

    """ ELIMINAR PUERTOS """

    for i in range(cant_masters):
        r_access_port_master = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_master' + str(i) + '_access_port', headers = { 'X-Auth-Token': token })
        r_dict_access_port_master = json.loads(r_access_port_master.text)
        access_port_master_id = r_dict_access_port_master['ports'][0]['id']
        r_delete_port = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports/" + access_port_master_id, headers = { 'X-Auth-Token': token })

    for i in range(cant_masters):
        r_mgnt_port_master = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_master' + str(i) + '_mgnt_port', headers = { 'X-Auth-Token': token })
        r_dict_mgnt_port_master = json.loads(r_mgnt_port_master.text)
        mgnt_port_master_id = r_dict_mgnt_port_master['ports'][0]['id']
        r_delete_port = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports/" + mgnt_port_master_id, headers = { 'X-Auth-Token': token })

    for i in range(cant_workers):
        r_mgnt_port_worker = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_worker' + str(i) + '_mgnt_port', headers = { 'X-Auth-Token': token })
        r_dict_mgnt_port_worker = json.loads(r_mgnt_port_worker.text)
        mgnt_port_worker_id = r_dict_mgnt_port_worker['ports'][0]['id']
        r_delete_port = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports/" + mgnt_port_worker_id, headers = { 'X-Auth-Token': token })

    for i in range(cant_workers):
        r_data_port_worker = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_worker' + str(i) + '_data_port', headers = { 'X-Auth-Token': token })
        r_dict_data_port_worker = json.loads(r_data_port_worker.text)
        data_port_worker_id = r_dict_data_port_worker['ports'][0]['id']
        r_delete_port = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports/" + data_port_worker_id, headers = { 'X-Auth-Token': token })

    """ ELIMINAR ROUTER """

    r_get_router = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/routers?name=' + slice_id + '_cluster_router', headers = { 'X-Auth-Token': token })
    r_dict_router = json.loads(r_get_router.text)
    router_id = r_dict_router['routers'][0]['id']

    r_get_access_subnet = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/subnets?name=" + slice_id + '_cluster_access_subnet', headers = { 'X-Auth-Token': token })
    r_dict_get_access_subnet = json.loads(r_get_access_subnet.text)
    access_subnet_id = r_dict_get_access_subnet['subnets'][0]['id']

    json_config_interface_router = return_config_interface_router()
    json_config_interface_router['subnet_id'] = access_subnet_id
    r_config_interface_router = requests.put('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/routers/" + router_id + "/remove_router_interface", json = json_config_interface_router, headers = { 'X-Auth-Token': token })

    r_delete_router = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/routers/" + router_id, headers = { 'X-Auth-Token': token })

    """ ELIMINAR REDES """

    r_get_access_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks?name=" + slice_id + '_cluster_access_net', headers = { 'X-Auth-Token': token })
    r_dict_get_access_net = json.loads(r_get_access_net.text)
    access_net_id = r_dict_get_access_net['networks'][0]['id']
    r_delete_net = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks/" + access_net_id, headers = { 'X-Auth-Token': token })

    r_get_mgnt_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks?name=" + slice_id + '_cluster_mgnt_net', headers = { 'X-Auth-Token': token })
    r_dict_get_mgnt_net = json.loads(r_get_mgnt_net.text)
    mgnt_net_id = r_dict_get_mgnt_net['networks'][0]['id']
    r_delete_net = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks/" + mgnt_net_id, headers = { 'X-Auth-Token': token })

    r_get_data_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks?name=" + slice_id + '_cluster_data_net', headers = { 'X-Auth-Token': token })
    r_dict_get_data_net = json.loads(r_get_data_net.text)
    data_net_id = r_dict_get_data_net['networks'][0]['id']
    r_delete_net = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/networks/" + data_net_id, headers = { 'X-Auth-Token': token })

    return 'slice deleted'

def generate_slice_mgnt_data_net_info(slice_id, cant_masters, cant_workers):
    token = generate_token()

    r_mgnt_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/networks?name=' + slice_id + '_cluster_mgnt_net', headers = { 'X-Auth-Token': token })
    r_dict_mgnt_net = json.loads(r_mgnt_net.text)
    mgnt_net_id = r_dict_mgnt_net['networks'][0]['id']
    mgnt_net_vlan = str(r_dict_mgnt_net['networks'][0]['provider:segmentation_id'])

    r_data_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/networks?name=' + slice_id + '_cluster_data_net', headers = { 'X-Auth-Token': token })
    r_dict_data_net = json.loads(r_data_net.text)
    data_net_id = r_dict_data_net['networks'][0]['id']
    data_net_vlan = str(r_dict_data_net['networks'][0]['provider:segmentation_id'])

    mgnt_ports_masters_id = []
    mgnt_ports_masters_mac = []
    for i in range(cant_masters):
        r_mgnt_port_master = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_master' + str(i) + '_mgnt_port', headers = { 'X-Auth-Token': token })
        r_dict_mgnt_port_master = json.loads(r_mgnt_port_master.text)
        mgnt_port_master_id = r_dict_mgnt_port_master['ports'][0]['id']
        mgnt_port_master_mac = r_dict_mgnt_port_master['ports'][0]['mac_address']
        mgnt_ports_masters_id.append(mgnt_port_master_id)
        mgnt_ports_masters_mac.append(mgnt_port_master_mac)

    mgnt_ports_workers_id = []
    mgnt_ports_workers_mac = []
    for i in range(cant_workers):
        r_mgnt_port_worker = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_worker' + str(i) + '_mgnt_port', headers = { 'X-Auth-Token': token })
        r_dict_mgnt_port_worker = json.loads(r_mgnt_port_worker.text)
        mgnt_port_worker_id = r_dict_mgnt_port_worker['ports'][0]['id']
        mgnt_port_worker_mac = r_dict_mgnt_port_worker['ports'][0]['mac_address']
        mgnt_ports_workers_id.append(mgnt_port_worker_id)
        mgnt_ports_workers_mac.append(mgnt_port_worker_mac)

    data_ports_workers_id = []
    data_ports_workers_mac = []
    for i in range(cant_workers):
        r_data_port_worker = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/ports?name=' + slice_id + '_cluster_worker' + str(i) + '_data_port', headers = { 'X-Auth-Token': token })
        r_dict_data_port_worker = json.loads(r_data_port_worker.text)
        print(">>> WORKER PORT : " + str(r_dict_data_port_worker))
        data_port_worker_id = r_dict_data_port_worker['ports'][0]['id']
        data_port_worker_mac = r_dict_data_port_worker['ports'][0]['mac_address']
        data_ports_workers_id.append(data_port_worker_id)
        data_ports_workers_mac.append(data_port_worker_mac)

    compute_node_masters = []
    for i in range(cant_masters):
        r_master = requests.get('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/detail?name=' + slice_id + '_cluster_master' + str(i), headers = { 'X-Auth-Token': token })
        r_dict_master = json.loads(r_master.text)
        print(">>> MASTER COMPUTE NODE: " + str(r_dict_master))
        compute_node_master = r_dict_master['servers'][0]['OS-EXT-SRV-ATTR:host']
        compute_node_masters.append(compute_node_master)

    master_openflow_port_array = get_compute_openflow_port(compute_node_masters)
    print("var compute_node_masters ---> " + str(compute_node_masters))

    compute_node_workers = []
    for i in range(cant_workers):
        r_worker = requests.get('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/detail?name=' + slice_id + '_cluster_worker' + str(i), headers = { 'X-Auth-Token': token })
        r_dict_worker = json.loads(r_worker.text)
        compute_node_worker = r_dict_worker['servers'][0]['OS-EXT-SRV-ATTR:host']
        compute_node_workers.append(compute_node_worker)

    worker_openflow_port_array = get_compute_openflow_port(compute_node_workers)
    print("var compute_node_workers ---> " + str(compute_node_workers))

    mgnt_masters=[]
    for mgnt_port_master_mac, master_openflow_port in zip(mgnt_ports_masters_mac,master_openflow_port_array):
        mgnt_masters.append({
            "mac": mgnt_port_master_mac,
            "openflow_port": master_openflow_port
        })

    mgnt_workers=[]
    for mgnt_port_worker_mac, worker_openflow_port in zip(mgnt_ports_workers_mac,worker_openflow_port_array):
        mgnt_workers.append({
            "mac": mgnt_port_worker_mac,
            "openflow_port": worker_openflow_port
        })

    data_workers=[]
    for data_port_worker_mac, worker_openflow_port in zip(data_ports_workers_mac,worker_openflow_port_array):
        data_workers.append({
            "mac": data_port_worker_mac,
            "openflow_port": worker_openflow_port
        })

    slice_mgnt_data_net_info = {
        "management_network": {
            "vlan_id": mgnt_net_vlan,
            "vm_nodes": {
                "masters": mgnt_masters,
                "workers": mgnt_workers
            }
        },
        "data_network": {
            "vlan_id": data_net_vlan,
            "vm_nodes": {
                "workers": data_workers
            }
        }
    }

    return slice_mgnt_data_net_info

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

def get_compute_openflow_port(server_compute_array):
    server_openflow_port_array = []
    for server_compute in server_compute_array:
        server_openflow_port = computes_openflow_port_dict[server_compute + '_openflow_port']
        server_openflow_port_array.append(server_openflow_port)
    return server_openflow_port_array

""" REQUEST APPLY SECURITY """

@csrf_exempt
def request_apply_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        r = requests.post('http://' + CYBERSECURITY_MODULE_IP + ':' + CYBERSECURITY_MODULE_PORT + "/cybersecurity/apply-security", json = json_req_body)

        return HttpResponse('Seguridad aplicada en el slice HPC: ' + json_req_body['slice_id'])

""" REQUEST REMOVE SECURITY """

@csrf_exempt
def request_remove_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        r = requests.post('http://' + CYBERSECURITY_MODULE_IP + ':' + CYBERSECURITY_MODULE_PORT + "/cybersecurity/remove-security", json = json_req_body)

        return HttpResponse('Seguridad removida en el slice HPC: ' + json_req_body['slice_id'])

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

""" OPENSTACK SECURITY """

def generate_token():
    r = requests.post('http://' + CONTROLLER_IP + ':' + IDENTITY_API_PORT + "/v3/auth/tokens", json = auth_data_admin, headers = { 'Content-Type': 'application/json' })
    token = r.headers["X-Subject-Token"]
    return token

def create_sec_group_json(slice_id):
    json_data = security_group
    json_data['security_group']['name'] = slice_id + '_cluster_access_sg'
    json_data['security_group']['description'] = 'Security group for slice ID: ' + slice_id
    return json_data

def create_sg_remote_rule(sec_group_id):
    json_data = return_remote_sg_rule()
    json_data['security_group_rule']['remote_group_id'] = sec_group_id
    json_data['security_group_rule']['security_group_id'] = sec_group_id

    return json_data

def create_sec_group_default_rules(sec_group_id, allowed_range_array):

    json_data_array = []
    for allowed_range in allowed_range_array:

        json_data = return_sg_default_rules()

        json_data['security_group_rule']['remote_ip_prefix'] = allowed_range['allowed_ip_range']
        json_data['security_group_rule']['security_group_id'] = sec_group_id
        json_data_array.append(json_data)

    return json_data_array

def create_tcp_port_rules(sec_group_id, allowed_range_array):
    json_data_array = []
    for allowed_range in allowed_range_array:
        json_data_1 = return_all_tcp_sg_rule()
        if allowed_range['all_tcp_enabled'] == "true":
            json_data_1['security_group_rule']['remote_ip_prefix'] = allowed_range['allowed_ip_range']
            json_data_1['security_group_rule']['security_group_id'] = sec_group_id
            json_data_array.append(json_data_1)
        else:
            for enabled_port in allowed_range['enabled_ports']:
                json_data_2 = return_tcp_port_sg_rule()
                json_data_2['security_group_rule']['remote_ip_prefix'] = allowed_range['allowed_ip_range']
                json_data_2['security_group_rule']['security_group_id'] = sec_group_id
                json_data_2['security_group_rule']['port_range_min'] = enabled_port
                json_data_2['security_group_rule']['port_range_max'] = enabled_port
                json_data_array.append(json_data_2)
    return json_data_array

def configure_sec_group_to_port(sec_group_id, set_or_unset):
    json_data = return_set_unset_sg_to_port()

    if set_or_unset == "set":
        json_data['port']['security_groups'].append(sec_group_id) 
    else:
        json_data['port']['security_groups'] = []

    return json_data

def get_port_id_by_name(token, port_name):
    r = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports?name=" + port_name, headers = { 'X-Auth-Token': token })
    r_dict = json.loads(r.text)
    port_id = r_dict['ports'][0]['id']
    return port_id

def get_master_access_port_id_array(token, slice_id, masters):
    masters_access_port_id_array = []
    for index, master in enumerate(masters):
        port_name = slice_id + '_cluster_' + "master" + str(index) + '_access_port'
        port_id = get_port_id_by_name(token, port_name)

        masters_access_port_id_array.append(port_id)

    return masters_access_port_id_array

def get_sec_group_id_by_name(token, sec_group_name):
    r = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-groups?name=" + sec_group_name, headers = { 'X-Auth-Token': token })
    r_dict = json.loads(r.text)
    sec_group_id = r_dict['security_groups'][0]['id']
    return sec_group_id

def request_token(request):

    return HttpResponse(generate_token())

def create_sec_group(request):

    slice_id = request.GET['sliceid']
    token = generate_token()
    json_body = create_sec_group_json(slice_id)
    r = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-groups", json = json_body, headers = { 'X-Auth-Token': token })
    return HttpResponse(r.text)

""" APPLY OPENSTACK SECURITY """

@csrf_exempt
def apply_openstack_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        slice_id = json_req_body['slice_id']

        allowed_range_array = json_req_body['access_network']['allowed_ranges']

        masters_array = json_req_body['management_network']['vm_nodes']['masters']

        token = generate_token()

        """ CREAR SECURITY GROUP """

        json_sec_group = create_sec_group_json(slice_id)

        r = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-groups", json = json_sec_group, headers = { 'X-Auth-Token': token })
        r_dict = json.loads(r.text)
        sec_group_id = r_dict['security_group']['id']

        """ CREAR REGLAS DE SECURITY GROUP """

        json_sg_remote_rule = create_sg_remote_rule(sec_group_id)

        r = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-group-rules", json = json_sg_remote_rule, headers = { 'X-Auth-Token': token })

        json_array_sec_group_default_rules = create_sec_group_default_rules(sec_group_id, allowed_range_array)

        for sg_rule in json_array_sec_group_default_rules:
            r = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-group-rules", json = sg_rule, headers = { 'X-Auth-Token': token })

        json_array_tcp_port_rules = create_tcp_port_rules(sec_group_id, allowed_range_array)

        for sg_rule in json_array_tcp_port_rules:
            r = requests.post('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-group-rules", json = sg_rule, headers = { 'X-Auth-Token': token })

        """ CONFIGURAR SECURITY GROUP EN PUERTOS ACCESS DE MASTERS """

        masters_access_port_id_array = get_master_access_port_id_array(token, slice_id, masters_array) 

        json_sec_group_port = configure_sec_group_to_port(sec_group_id, "set") 

        for master_id in masters_access_port_id_array:
            r = requests.put('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports/" + master_id, json = json_sec_group_port, headers = { 'X-Auth-Token': token })

        json_response = json.dumps({"sec_group_id": sec_group_id,
            "json_array_sec_group_default_rules": json_array_sec_group_default_rules,
            "json_array_tcp_port_rules": json_array_tcp_port_rules})

        return HttpResponse(json_response, content_type ="application/json")

""" REMOVE OPENSTACK SECURITY """

@csrf_exempt
def remove_openstack_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        slice_id = json_req_body['slice_id']

        masters_array = json_req_body['management_network']['vm_nodes']['masters']

        token = generate_token()

        """ DESCONFIGURAR SECURITY GROUP EN PUERTOS ACCESS DE MASTERS """

        masters_access_port_id_array = get_master_access_port_id_array(token, slice_id, masters_array)

        json_sec_group_port = configure_sec_group_to_port("", "unset")

        for master_id in masters_access_port_id_array:
            r = requests.put('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/ports/" + master_id, json = json_sec_group_port, headers = { 'X-Auth-Token': token })

        """ ELIMINAR SECURITY GROUP """

        sec_group_id = get_sec_group_id_by_name(token, slice_id + "_cluster_access_sg")

        r = requests.delete('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + "/v2.0/security-groups/" + sec_group_id, headers = { 'X-Auth-Token': token })

        return HttpResponse("Seguridad en OpenStack removida")

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

"""  GROUP TABLES """ 

def generate_group_table_id(slice_id):

    group_id = ''.join(c for c in slice_id if c.isdigit())[:9]
    return group_id

def generate_group_all(slice_id, mgnt_network_info):
    json_group_table = return_group_table()

    json_group_table['flow-node-inventory:group'][0]['group-id'] = str(int(generate_group_table_id(slice_id)) + 1)
    json_group_table['flow-node-inventory:group'][0]['group-name'] = slice_id + '_slice-all_group_table'

    buckets_masters_array = []
    for index, master in enumerate(mgnt_network_info['vm_nodes']['masters']):
        json_bucket = return_bucket()
        json_bucket['bucket-id'] = index
        json_bucket['action'][0]['output-action']['output-node-connector'] = master['openflow_port']

        buckets_masters_array.append(json_bucket)

    buckets_workers_array = []
    for index2, worker in enumerate(mgnt_network_info['vm_nodes']['workers']):
        json_bucket = return_bucket()
        json_bucket['bucket-id'] = index2
        json_bucket['action'][0]['output-action']['output-node-connector'] = worker['openflow_port']

        buckets_workers_array.append(json_bucket)

    buckets_array = buckets_masters_array + buckets_workers_array

    json_group_table['flow-node-inventory:group'][0]['buckets']['bucket'] = buckets_array

    return json_group_table

def generate_group_masters(slice_id, mgnt_network_info):
    json_group_table = return_group_table()

    json_group_table['flow-node-inventory:group'][0]['group-id'] = str(int(generate_group_table_id(slice_id)) + 2)
    json_group_table['flow-node-inventory:group'][0]['group-name'] = slice_id + '_slice-masters_group_table'

    buckets_array = []
    for index, master in enumerate(mgnt_network_info['vm_nodes']['masters']):
        json_bucket = return_bucket()
        json_bucket['bucket-id'] = index
        json_bucket['action'][0]['output-action']['output-node-connector'] = master['openflow_port']

        buckets_array.append(json_bucket)

    json_group_table['flow-node-inventory:group'][0]['buckets']['bucket'] = buckets_array

    return json_group_table

def generate_group_workers(slice_id, data_network_info):
    json_group_table = return_group_table()

    json_group_table['flow-node-inventory:group'][0]['group-id'] = str(int(generate_group_table_id(slice_id)) + 3)
    json_group_table['flow-node-inventory:group'][0]['group-name'] = slice_id + '_slice-workers_group_table'

    buckets_array = []
    for index, worker in enumerate(data_network_info['vm_nodes']['workers']):
        json_bucket = return_bucket()
        json_bucket['bucket-id'] = index
        json_bucket['action'][0]['output-action']['output-node-connector'] = worker['openflow_port']

        buckets_array.append(json_bucket)

    json_group_table['flow-node-inventory:group'][0]['buckets']['bucket'] = buckets_array

    return json_group_table

def generate_opendaylight_json_group_tables_array(slice_id, mgnt_network_info, data_network_info):
    group_tables_array = []

    group_table_all = generate_group_all(slice_id, mgnt_network_info)

    group_table_masters = generate_group_masters(slice_id, mgnt_network_info)

    group_table_workers = generate_group_workers(slice_id, data_network_info)

    group_tables_array.extend([group_table_all, group_table_masters, group_table_workers])

    return group_tables_array

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

"""  FUNCIONES PARA CREAR FLOW DE LA RED ACCESS, cuando el switch funciona en modo OpenFlow-only (no existe un comportamiento en NORMAL) """

def get_access_vlan_id(slice_id):
    token = generate_token()

    r_access_net = requests.get('http://' + CONTROLLER_IP + ':' + NETWORK_API_PORT + '/v2.0/networks?name=' + slice_id + '_cluster_access_net', headers = { 'X-Auth-Token': token })
    r_dict_access_net = json.loads(r_access_net.text)
    access_net_vlan = str(r_dict_access_net['networks'][0]['provider:segmentation_id'])

    return access_net_vlan

def generate_access_flow_array(slice_id,mgnt_network_info):

    json_flows_array = []

    json_data = return_access_flow()

    json_data['flow'][0]['id'] = slice_id + '_slice-access_network-flow'
    json_data['flow'][0]['priority'] = '500'
    json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = get_access_vlan_id(slice_id)

    json_flows_array.append(json_data)

    return json_flows_array

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

""" FLOWS para redes MANAGEMENT y DATA """ 

def generate_mgnt_flow_type1_array(slice_id, mgnt_network_info):
    json_flows_array = []

    for index1, master_source in enumerate(mgnt_network_info['vm_nodes']['masters']):
        json_data = return_mgnt_flow_type1()

        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = mgnt_network_info['vlan_id']
        json_data['flow'][0]['match']['in-port'] = 'openflow:' + ODL_switch_id + ':' + master_source['openflow_port']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = master_source['mac']

        for index2, worker in enumerate(mgnt_network_info['vm_nodes']['workers']):
            json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-flow_' + str(5001 + index1*10 + index2)
            json_data['flow'][0]['priority'] = str(5001 + index1*10 + index2)

            json_data2 = copy.deepcopy(json_data)

            json_data2['flow'][0]['match']['ethernet-match']['ethernet-destination']['address'] = worker['mac']
            json_data2['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'] = worker['openflow_port']

            json_flows_array.append(json_data2)

        for index3, master_dst in enumerate(mgnt_network_info['vm_nodes']['masters']):
            if master_source['mac'] != master_dst['mac']:
                json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-flow_' + str(5501 + index1*10 + index3)
                json_data['flow'][0]['priority'] = str(5501 + index1*10 + index3)

                json_data3 = copy.deepcopy(json_data)

                json_data3['flow'][0]['match']['ethernet-match']['ethernet-destination']['address'] = master_dst['mac']
                json_data3['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'] = master_dst['openflow_port']

                json_flows_array.append(json_data3)

    return json_flows_array

def generate_mgnt_flow_type2_array(slice_id, mgnt_network_info):
    json_flows_array = []

    for index, master in enumerate(mgnt_network_info['vm_nodes']['masters']):
        json_data = return_mgnt_flow_type2()

        json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-flow_' + str(4001 + index)
        json_data['flow'][0]['priority'] = str(4001 + index)
        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = mgnt_network_info['vlan_id']
        json_data['flow'][0]['match']['in-port'] = 'openflow:' + ODL_switch_id + ':' + master['openflow_port']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = master['mac']
        json_data['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['group-action']['group'] = slice_id + '_slice-all_group_table'
        json_data['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['group-action']['group-id'] = str(int(generate_group_table_id(slice_id)) + 1)

        json_flows_array.append(json_data)

    return json_flows_array

def generate_mgnt_flow_type3_array(slice_id, mgnt_network_info):
    json_flows_array = []

    for index1, worker in enumerate(mgnt_network_info['vm_nodes']['workers']):
        json_data = return_mgnt_flow_type3()

        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = mgnt_network_info['vlan_id']
        json_data['flow'][0]['match']['in-port'] = 'openflow:' + ODL_switch_id + ':' + worker['openflow_port']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = worker['mac']

        for index2, master in enumerate(mgnt_network_info['vm_nodes']['masters']):
            json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-flow_' + str(3001 + index1*10 + index2)
            json_data['flow'][0]['priority'] = str(3001 + index1*10 + index2)

            json_data2 = copy.deepcopy(json_data)

            json_data2['flow'][0]['match']['ethernet-match']['ethernet-destination']['address'] = master['mac']
            json_data2['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'] = master['openflow_port']

            json_flows_array.append(json_data2)

    return json_flows_array

def generate_mgnt_flow_type4_array(slice_id, mgnt_network_info):
    json_flows_array = []

    for index, worker in enumerate(mgnt_network_info['vm_nodes']['workers']):
        json_data = return_mgnt_flow_type4()

        json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-flow_' + str(2001 + index)
        json_data['flow'][0]['priority'] = str(2001 + index)
        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = mgnt_network_info['vlan_id']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-destination']['address'] = worker['mac']
        
        json_flows_array.append(json_data)

    return json_flows_array

def generate_mgnt_flow_type5_array(slice_id, mgnt_network_info):
    json_flows_array = []

    for index, worker in enumerate(mgnt_network_info['vm_nodes']['workers']):
        json_data = return_mgnt_flow_type5()

        json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-flow_' + str(1001 + index)
        json_data['flow'][0]['priority'] = str(1001 + index)
        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = mgnt_network_info['vlan_id']
        json_data['flow'][0]['match']['in-port'] = 'openflow:' + ODL_switch_id + ':' + worker['openflow_port']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = worker['mac']
        json_data['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['group-action']['group'] = slice_id + '_slice-masters_group_table'
        json_data['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['group-action']['group-id'] = str(int(generate_group_table_id(slice_id)) + 2)

        json_flows_array.append(json_data)

    return json_flows_array

def generate_mgnt_flow_default_vlan_drop_array(slice_id, mgnt_network_info):
    json_flows_array = []

    json_data = return_default_vlan_drop_flow()

    json_data['flow'][0]['id'] = slice_id + '_slice-mgnt_network-drop'
    json_data['flow'][0]['priority'] = '999'
    json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = mgnt_network_info['vlan_id']

    json_flows_array.append(json_data)

    return json_flows_array

def generate_data_flow_type1_array(slice_id, data_network_info):
    json_flows_array = []

    for index1, worker_source in enumerate(data_network_info['vm_nodes']['workers']):
        json_data = return_data_flow_type1()

        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = data_network_info['vlan_id']
        json_data['flow'][0]['match']['in-port'] = 'openflow:' + ODL_switch_id + ':' + worker_source['openflow_port']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = worker_source['mac']

        for index2, worker_dest in enumerate(data_network_info['vm_nodes']['workers']):
            if worker_source['mac'] != worker_dest['mac']:
                json_data['flow'][0]['id'] = slice_id + '_slice-data_network-flow_' + str(9001 + index1*10 + index2)
                json_data['flow'][0]['priority'] = str(9001 + index1*10 + index2)

                json_data2 = copy.deepcopy(json_data)

                json_data2['flow'][0]['match']['ethernet-match']['ethernet-destination']['address'] = worker_dest['mac']
                json_data2['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector'] = worker_dest['openflow_port']

                json_flows_array.append(json_data2)

    return json_flows_array

def generate_data_flow_type2_array(slice_id, data_network_info):
    json_flows_array = []

    for index1, worker in enumerate(data_network_info['vm_nodes']['workers']):
        json_data = return_data_flow_type2()

        json_data['flow'][0]['id'] = slice_id + '_slice-data_network-flow_' + str(8001 + index1)
        json_data['flow'][0]['priority'] = str(8001 + index1)
        json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = data_network_info['vlan_id']
        json_data['flow'][0]['match']['in-port'] = 'openflow:' + ODL_switch_id + ':' + worker['openflow_port']
        json_data['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = worker['mac']
        json_data['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['group-action']['group'] = slice_id + '_slice-workers_group_table'
        json_data['flow'][0]['instructions']['instruction'][0]['apply-actions']['action'][0]['group-action']['group-id'] = str(int(generate_group_table_id(slice_id)) + 3)

        json_flows_array.append(json_data)

    return json_flows_array

def generate_data_flow_default_vlan_drop_array(slice_id, data_network_info):
    json_flows_array = []

    json_data = return_default_vlan_drop_flow()

    json_data['flow'][0]['id'] = slice_id + '_slice-data_network-drop'
    json_data['flow'][0]['priority'] = '998'
    json_data['flow'][0]['match']['vlan-match']['vlan-id']['vlan-id'] = data_network_info['vlan_id']

    json_flows_array.append(json_data)

    return json_flows_array

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

""" CONFIG ODL SECURITY """

def generate_opendaylight_json_flows_array(slice_id, mgnt_network_info, data_network_info):
    flows_array = []

    access_flow_array = generate_access_flow_array(slice_id, mgnt_network_info)

    mgnt_flow_default_vlan_drop_array = generate_mgnt_flow_default_vlan_drop_array(slice_id, mgnt_network_info)
    data_flow_default_vlan_drop_array = generate_data_flow_default_vlan_drop_array(slice_id, data_network_info)

    mgnt_flow_type1_array = generate_mgnt_flow_type1_array(slice_id, mgnt_network_info)
    mgnt_flow_type2_array = generate_mgnt_flow_type2_array(slice_id, mgnt_network_info)
    mgnt_flow_type3_array = generate_mgnt_flow_type3_array(slice_id, mgnt_network_info)
    mgnt_flow_type4_array = generate_mgnt_flow_type4_array(slice_id, mgnt_network_info)    
    mgnt_flow_type5_array = generate_mgnt_flow_type5_array(slice_id, mgnt_network_info)

    data_flow_type1_array = generate_data_flow_type1_array(slice_id, data_network_info)
    data_flow_type2_array = generate_data_flow_type2_array(slice_id, data_network_info)

    flows_array = access_flow_array + mgnt_flow_default_vlan_drop_array + data_flow_default_vlan_drop_array + mgnt_flow_type1_array + mgnt_flow_type2_array + mgnt_flow_type3_array + mgnt_flow_type4_array + mgnt_flow_type5_array + data_flow_type1_array + data_flow_type2_array

    return flows_array

""" APPLY OPENDAYLIGHT SECURITY """

@csrf_exempt
def apply_opendaylight_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        slice_id = json_req_body['slice_id']

        mgnt_network_info = json_req_body['management_network']

        data_network_info = json_req_body['data_network']

        group_tables_array = generate_opendaylight_json_group_tables_array(slice_id, mgnt_network_info, data_network_info)

        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        auth = HTTPBasicAuth(ODL_user, ODL_password)
        for group_table in group_tables_array:
            url = ODL_BASE_URL + '/restconf/config/opendaylight-inventory:nodes/node/openflow:' + ODL_switch_id + '/group/' + group_table['flow-node-inventory:group'][0]['group-id']

            r = requests.put(url, json = group_table, headers = headers, auth = auth)

        flows_array = generate_opendaylight_json_flows_array(slice_id, mgnt_network_info, data_network_info)

        headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' }
        auth = HTTPBasicAuth(ODL_user, ODL_password)
        for flow in flows_array:
            url = ODL_BASE_URL + '/restconf/config/opendaylight-inventory:nodes/node/openflow:' + ODL_switch_id + '/table/' + str(flow['flow'][0]['table_id']) + '/flow/' + flow['flow'][0]['id']

            r = requests.put(url, json = flow, headers = headers, auth = auth)

        json_response = json.dumps({"flows_array" : flows_array})
        return HttpResponse(json_response, content_type ="application/json")

""" REMOVE OPENDAYLIGHT SECURITY """

@csrf_exempt
def remove_opendaylight_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        slice_id = json_req_body['slice_id']

        mgnt_network_info = json_req_body['management_network']

        data_network_info = json_req_body['data_network']

        group_tables_array = generate_opendaylight_json_group_tables_array(slice_id, mgnt_network_info, data_network_info)

        auth = HTTPBasicAuth(ODL_user, ODL_password)
        for group_table in group_tables_array:
            url = ODL_BASE_URL + '/restconf/config/opendaylight-inventory:nodes/node/openflow:' + ODL_switch_id + '/group/' + group_table['flow-node-inventory:group'][0]['group-id']

            r = requests.delete(url, auth = auth)

        flows_array = generate_opendaylight_json_flows_array(slice_id, mgnt_network_info, data_network_info)

        auth = HTTPBasicAuth(ODL_user, ODL_password)
        for flow in flows_array:
            url = ODL_BASE_URL + '/restconf/config/opendaylight-inventory:nodes/node/openflow:' + ODL_switch_id + '/table/' + str(flow['flow'][0]['table_id']) + '/flow/' + flow['flow'][0]['id']

            r = requests.delete(url, auth = auth)

        return HttpResponse("Seguridad en OpenDaylight removida")

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

def get_slice_security_info(request):

    if request.method == 'GET':
        slice_id = request.GET['sliceid']

        r = requests.get('http://' + CYBERSECURITY_MODULE_IP + ':' + CYBERSECURITY_MODULE_PORT + "/cybersecurity/get-slice-security-info?sliceid=" + slice_id)

        return HttpResponse(r.text)

def get_all_slices_security_info(request):

    if request.method == 'GET':
        r = requests.get('http://' + CYBERSECURITY_MODULE_IP + ':' + CYBERSECURITY_MODULE_PORT + "/cybersecurity/get-all-slices-security-info")
        return HttpResponse(r.text)

def get_all_slices_security_info2(request):

    if request.method == 'GET':
        r = requests.get('http://' + CYBERSECURITY_MODULE_IP + ':' + CYBERSECURITY_MODULE_PORT + "/cybersecurity/get-all-slices-security-info2")
        return HttpResponse(r.text)

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""
