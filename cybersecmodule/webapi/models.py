from django.db import models

# Create your models here.

class Slicehpc(models.Model):
    #slice_id = models.CharField(max_length=200, primary_key=True)
    slice_identifier = models.CharField(max_length=200)
    security_status = models.CharField(max_length=200, null=True)
    security_request_body = models.CharField(max_length=2000, null=True)
    openstack_security_rules = models.CharField(max_length=2000, null=True)
    opendaylight_security_rules = models.CharField(max_length=2000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.slice_identifier