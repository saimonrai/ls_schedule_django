from django.views.generic import View

from ls_schedule.apps.base.http import JSONResponse
from ls_schedule.apps.schedule.models import Schedule


class ScheduleReadView(View):

    def get(self, request, *args, **kwargs):
        data = [s.to_dict() for s in Schedule.objects.all()]
        return JSONResponse(request, data)



