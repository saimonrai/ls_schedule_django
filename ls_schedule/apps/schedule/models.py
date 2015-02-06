from collections import OrderedDict
import datetime

from django.db import models

from ls_schedule.apps.base.models import TimeStampedModel
from ls_schedule.apps.groups.models import Group

DAYS_OF_WEEK = (
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
)

class Schedule(TimeStampedModel):
    group = models.ForeignKey(Group)
    weekday = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return "%s (%s-%s) for %s" % (self.get_weekday_display(), self.start_time, self.end_time, self.group.name)

    @staticmethod
    def day_of_week_actual_value(day):
        days_of_week_swapped = {value: key for key, value in DAYS_OF_WEEK}
        return days_of_week_swapped[day]

    def to_dict(self):
        data = OrderedDict()
        data['group_id'] = self.group_id
        data['weekday'] = self.weekday

        time_format = '%H:%M'

        data['start_time'] = self.start_time.strftime(time_format)
        data['end_time'] = self.end_time.strftime(time_format)
        return data
