from django.db import models


class Members(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    surname = models.CharField(max_length=255, blank=False, null=False)
    booking_count = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    @property
    def employee_name(self):
        return '{}'.format(self.name)
