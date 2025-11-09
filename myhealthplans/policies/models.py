from  myhealthplans.storages_backends import R2PublicStorage
from myhealthplans.const import R2_PUBLIC_URL
from .mixins import R2PublicURLMixin
from django.db import models

class Policy(R2PublicURLMixin,models.Model):
    name = models.CharField(max_length=255)
    policy_name = models.CharField(max_length=255)
    policy_type = models.CharField(max_length=255)
    dob = models.DateField()
    policy_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    sum_assured = models.DecimalField(max_digits=12, decimal_places=2)
    details = models.TextField(blank=True, null=True)

    aadhar = models.FileField(upload_to='documents/aadhar/', storage=R2PublicStorage(), null=True, blank=True)
    pan = models.FileField(upload_to='documents/pan/', storage=R2PublicStorage(), null=True, blank=True)
    document = models.FileField(upload_to='documents/policies/', storage=R2PublicStorage(), null=True, blank=True)

    aadhar_public_url = models.URLField(blank=True, null=True)
    pan_public_url = models.URLField(blank=True, null=True)
    document_public_url = models.URLField(blank=True, null=True)

    # Map your files to their public URL fields
    file_url_map = {
        "aadhar": ("aadhar_public_url", "documents/aadhar/"),
        "pan": ("pan_public_url", "documents/pan/"),
        "document": ("document_public_url", "documents/policies/"),
    }


    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.policy_name} - {self.name}"

