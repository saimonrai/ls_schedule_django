#!/usr/bin/env python
from django.conf.urls import patterns, url

import ls_schedule.apps.groups.views as group_views
import ls_schedule.apps.schedule.views as schedule_views

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2013 Poolsidelabs Inc.'


urlpatterns = patterns("",
    # {%url "api:groups" %}
    url(regex=r'groups/$',
        view=group_views.GroupsReadView.as_view(),
        name='groups'),

    # {%url "api:schedule" %}
    url(regex=r'groups/schedule/$',
        view=schedule_views.ScheduleReadView.as_view(),
        name='schedule'),
)