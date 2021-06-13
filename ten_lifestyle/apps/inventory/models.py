from django.db import models


class Inventory(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=2000, blank=False, null=False)
    remaining_count = models.IntegerField(blank=False, null=False)
    expiration_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def inventory_name(self):
        return '{}'.format(self.title)

