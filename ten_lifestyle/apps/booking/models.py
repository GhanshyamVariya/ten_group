from django.db import models

from ten_lifestyle.apps.inventory.models import Inventory
from ten_lifestyle.apps.member.models import Members


class Bookings(models.Model):
    member = models.ForeignKey(Members, models.DO_NOTHING, related_name='member_book')
    inventory = models.ForeignKey(Inventory, models.DO_NOTHING, related_name='inventory_book')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def book_info(self):
        return '{}'.format(self.member.name)
