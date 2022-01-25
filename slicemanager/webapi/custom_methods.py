import requests
import json
from .configuration import COMPUTE_API_PORT,CONTROLLER_IP

def get_vm_hostname(name, token):
    r_worker = requests.get('http://' + CONTROLLER_IP + ':' + COMPUTE_API_PORT + '/v2.1/servers/detail?name=' + name, headers = { 'X-Auth-Token': token })
    r_dict_worker = json.loads(r_worker.text)
    return r_dict_worker['servers'][0]['OS-EXT-SRV-ATTR:host']