from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from webapi.models import Slicehpc

import requests
import json
import copy

SLICE_MANAGER_IP = '10.0.0.1'
SLICE_MANAGER_PORT = '8000'

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

def prueba(request):
    return HttpResponse("OK")

""" APPLY SECURITY """

@csrf_exempt
def apply_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        r1 = requests.post('http://' + SLICE_MANAGER_IP + ':' + SLICE_MANAGER_PORT + "/slicemanager/apply-openstack-security", json = json_req_body)

        r2 = requests.post('http://' + SLICE_MANAGER_IP + ':' + SLICE_MANAGER_PORT + "/slicemanager/apply-opendaylight-security", json = json_req_body)

        slice_exists = Slicehpc.objects.filter(slice_identifier=json_req_body['slice_id']).exists()
        if slice_exists == True:

            slice_by_identifier = Slicehpc.objects.get(slice_identifier=json_req_body['slice_id'])
            slice_by_identifier.security_status='enabled_updated'
            slice_by_identifier.security_request_body = str(json_req_body)
            slice_by_identifier.openstack_security_rules=r1.text
            slice_by_identifier.opendaylight_security_rules=r2.text
            slice_by_identifier.save()
        else:

            slice_entry = Slicehpc(slice_identifier=json_req_body['slice_id'],security_status='enabled',security_request_body=str(json_req_body),openstack_security_rules=r1.text,opendaylight_security_rules=r2.text)
            slice_entry.save()

    return HttpResponse('Seguridad aplicada en el slice HPC: ' + json_req_body['slice_id'])

""" REMOVE SECURITY """

@csrf_exempt
def remove_security(request):

    if request.method == 'POST':

        json_req_body = json.loads(request.body)

        r1 = requests.post('http://' + SLICE_MANAGER_IP + ':' + SLICE_MANAGER_PORT + "/slicemanager/remove-openstack-security", json = json_req_body)

        r2 = requests.post('http://' + SLICE_MANAGER_IP + ':' + SLICE_MANAGER_PORT + "/slicemanager/remove-opendaylight-security", json = json_req_body)

        slice_by_identifier = Slicehpc.objects.get(slice_identifier=json_req_body['slice_id'])
        slice_by_identifier.security_status='disabled'
        slice_by_identifier.security_request_body = str(json_req_body)
        slice_by_identifier.openstack_security_rules=''
        slice_by_identifier.opendaylight_security_rules=''
        slice_by_identifier.save()

    return HttpResponse('Seguridad removida en el slice HPC: ' + json_req_body['slice_id'])

"""
=====================================================================================
=====================================================================================
=====================================================================================
"""

""" GET SLICE SECURITY INFO """

def get_slice_security_info(request):

    if request.method == 'GET':
        slice_id = request.GET['sliceid']
        slice_by_identifier = Slicehpc.objects.get(slice_identifier=slice_id)
        slice_identifier = slice_by_identifier.slice_identifier
        security_status = slice_by_identifier.security_status
        security_request_body = slice_by_identifier.security_request_body
        openstack_security_rules = slice_by_identifier.openstack_security_rules
        opendaylight_security_rules = slice_by_identifier.opendaylight_security_rules
        result = {
            "slice_identifier" : slice_identifier,
            "security_status" : security_status,
            "security_request_body" : security_request_body,
            "openstack_security_rules" : openstack_security_rules,
            "opendaylight_security_rules" : opendaylight_security_rules
        }
        print(result)
        return HttpResponse('<b>Slice ID</b>: ' + result['slice_identifier'] + '<br/><br/><b>Security status</b>: ' + result['security_status'] + '<br/><br/><b>Security request body</b>: ' + result['security_request_body'] + '<br/><br/><b>OpenStack security rules</b>: ' + result['openstack_security_rules'] + '<br/><br/><b>OpenDaylight security rules</b>: ' + result['opendaylight_security_rules'])

""" GET ALL SLICES SECURITY INFO """

def get_all_slices_security_info(request):

    if request.method == 'GET':

        slices = Slicehpc.objects.all()

        slices_array = []
        for slicehpc in slices:
            slice_identifier = slicehpc.slice_identifier
            security_status = slicehpc.security_status
            security_request_body = slice_by_identifier.security_request_body
            openstack_security_rules = slicehpc.openstack_security_rules
            opendaylight_security_rules = slicehpc.opendaylight_security_rules

            slice_dict = {
                "slice_identifier" : slice_identifier,
                "security_status" : security_status,
                "security_request_body" : security_request_body,
                "openstack_security_rules" : openstack_security_rules,
                "opendaylight_security_rules" : opendaylight_security_rules
            }

            slices_array.append(slice_dict)

        print(slices_array)
        return HttpResponse(slices_array)

""" GET ALL SLICES SECURITY INFO 2 """

def get_all_slices_security_info2(request):

    slices = Slicehpc.objects.all()
    return render(request, 'slices.html', {'slices':slices})