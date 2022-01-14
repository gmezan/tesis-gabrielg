from .methods import *


def create_direct_port_request(mgnt_port_master_name, mgnt_net_id):
    json = return_create_direct_port()
    json['port']['name'] = mgnt_port_master_name
    json['port']['network_id'] = mgnt_net_id
    return json

def create_port_request(mgnt_port_master_name, mgnt_net_id):
    json = return_create_port()
    json['port']['name'] = mgnt_port_master_name
    json['port']['network_id'] = mgnt_net_id
    return json
