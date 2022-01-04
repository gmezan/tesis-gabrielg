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
    return { "port": { "name": "", "network_id": "", "binding:vnic_type": "normal" } }

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

