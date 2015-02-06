from collections import OrderedDict
from django.db import models

from ls_schedule.apps.base.models import TimeStampedModel


class Group(TimeStampedModel):
    name = models.CharField(max_length=512, unique=True)
    name_nep = models.CharField(max_length=512, unique=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.name_nep)

    def to_dict(self):
        data = OrderedDict()
        data['id'] = self.id
        data['name'] = self.name
        data['name_nep'] = self.name_nep
        return data


class Substation(TimeStampedModel):
    name = models.CharField(max_length=512, unique=True)
    name_nep = models.CharField(max_length=512, unique=True)
    in_ktm = models.BooleanField(default=True, verbose_name="Whether the substation is inside Kathmandu")

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.name_nep)

    def to_dict(self):
        data = OrderedDict()
        data['id'] = self.id
        data['name'] = self.name
        data['name_nep'] = self.name_nep
        data['in_ktm'] = self.in_ktm
        return data


class Area(TimeStampedModel):
    name = models.CharField(max_length=512)
    name_nep = models.CharField(max_length=512)
    group = models.ForeignKey(Group)
    substation = models.ForeignKey(Substation)
    in_ktm = models.BooleanField(default=True, verbose_name="Whether the area is inside Kathmandu")

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.name_nep)

    def to_dict(self):
        data = OrderedDict()
        data['id'] = self.id
        data['name'] = self.name
        data['name_nep'] = self.name_nep
        data['group_id'] = self.group_id
        data['substation_id'] = self.substation_id
        data['in_ktm'] = self.in_ktm
        return data
