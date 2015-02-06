from collections import OrderedDict
from django.views.generic import View

from ls_schedule.apps.base.http import JSONResponse
from .models import Group, Substation, Area


class GroupsReadView(View):

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        substations = Substation.objects.all()
        areas = Area.objects.all()

        data = OrderedDict()
        data['groups'] = [g.to_dict() for g in groups]
        data['substations'] = [s.to_dict() for s in substations]
        data['areas'] = [a.to_dict() for a in areas]

        return JSONResponse(request, data)


