from django.urls import path
from . import views

urlpatterns = [
    path('prueba', views.prueba, name='prueba'),
    path('apply-security', views.apply_security, name='apply_security'),
    path('remove-security', views.remove_security, name='remove_security'),
    path('get-slice-security-info', views.get_slice_security_info, name='get_slice_security_info'),
    path('get-all-slices-security-info', views.get_all_slices_security_info, name='get_all_slices_security_info'),
    path('get-all-slices-security-info2', views.get_all_slices_security_info2, name='get_all_slices_security_info2'),
]
