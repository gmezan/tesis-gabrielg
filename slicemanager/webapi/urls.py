from django.urls import path
from . import views

urlpatterns = [
    path('handle-client-create-request', views.handle_client_create_request, name='handle_client_create_request'),
    path('handle-client-delete-request', views.handle_client_delete_request, name='handle_client_delete_request'),
    path('request-apply-security', views.request_apply_security, name='request_apply_security'),
    path('request-remove-security', views.request_remove_security, name='request_remove_security'),
    path('request-token', views.request_token, name='request_token'),
    path('create-security-group', views.create_sec_group, name='create_sec_group'),
    path('apply-openstack-security', views.apply_openstack_security, name='apply_openstack_security'),
    path('remove-openstack-security', views.remove_openstack_security, name='remove_openstack_security'),
    path('apply-opendaylight-security', views.apply_opendaylight_security, name='apply_opendaylight_security'),
    path('remove-opendaylight-security', views.remove_opendaylight_security, name='remove_opendaylight_security'),
    path('get-slice-security-info', views.get_slice_security_info, name='get_slice_security_info'),
    path('get-all-slices-security-info', views.get_all_slices_security_info, name='get_all_slices_security_info'),
    path('get-all-slices-security-info2', views.get_all_slices_security_info2, name='get_all_slices_security_info2'),
]
