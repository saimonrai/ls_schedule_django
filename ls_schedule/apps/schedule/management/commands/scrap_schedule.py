#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from copy import deepcopy
import datetime
import logging

from django.core.management.base import NoArgsCommand
from django.db import transaction

from bs4 import BeautifulSoup
import requests

from ls_schedule.apps.groups.models import Group
from ls_schedule.apps.schedule.models import Schedule

__author__ = 'Saimon Rai'
__created__ = '3:19 PM 7/20/14'
__copyright__ = 'Copyright 2014 Poolsidelabs Inc.'

logger = logging.getLogger('management_commands')
SCHEDULE_WEBPAGE_URL = 'http://www.myrepublica.com/portal/index.php?action=pages&page_id=8'
TIME_FORMAT = '%H:%M'
TIME_FORMAT_1 = '%H.%M'


class Command(NoArgsCommand):
    @transaction.atomic
    def handle_noargs(self, **options):
        try:
            logger.info("Scraping myrepublica.com for new schedule...")
            html_doc = requests.get(SCHEDULE_WEBPAGE_URL, timeout=60).text
        except requests.RequestException as e:
            logger.error(e)
            return

        weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        weekdays = OrderedDict()
        for name in weekday_names:
            weekdays[name] = []

        groups = OrderedDict()
        groups['Group 1'] = deepcopy(weekdays)
        groups['Group 2'] = deepcopy(weekdays)
        groups['Group 3'] = deepcopy(weekdays)
        groups['Group 4'] = deepcopy(weekdays)
        groups['Group 5'] = deepcopy(weekdays)
        groups['Group 6'] = deepcopy(weekdays)
        groups['Group 7'] = deepcopy(weekdays)

        soup = BeautifulSoup(html_doc)
        # <table width="700" bordercolor="#999999" border="1" cellspacing="0" cellpadding="0">
        tables = soup.find_all("table", {'width': '700', 'bordercolor': '#999999', 'cellspacing': '0', 'cellpadding': '0'})
        if not tables:
            logger.error("Table containing schedule not found")

        table = tables[0]
        rows = table.findChildren(['tr'])
        rows = rows[1:]  # first row are weekday titles

        # print rows[0].prettify()

        for row in rows:
            cells = row.findChildren('td')
            cells = [cell for cell in cells if cell.getText().strip()]  # there are two empty columns in the table

            group_name = cells[0].getText().strip()  # the first column contains the group name
            logger.info("Group Name: %s", group_name)

            for index, cell in enumerate(cells[1:]):
                schedules = cell.getText().split('\n')
                schedules = filter(None, schedules)  # remove empty items, ex: [u'10:00-14:00', u'19:00-21:30', u'']

                weekday_name = weekday_names[index]

                print weekday_name, schedules

                for schedule in schedules:
                    schedule = schedule.strip()  # some entries have '&nbsp'

                    time_parts = schedule.split('-')  # 08:45-17:00
                    time_from, time_to = time_parts[0], time_parts[1]  # ['08:45', '17:00']

                    # Quick fix: python only accepts hour range from 0:23.
                    time_from = time_from.replace('24:', '00:')
                    time_to = time_to.replace('24:', '00:')

                    # some times use '.' instead of ':'
                    try:
                        start_time = datetime.datetime.strptime(time_from, TIME_FORMAT)
                    except ValueError:
                        start_time = datetime.datetime.strptime(time_from, TIME_FORMAT_1)
                    try:
                        end_time = datetime.datetime.strptime(time_to, TIME_FORMAT)
                    except ValueError:
                        end_time = datetime.datetime.strptime(time_to, TIME_FORMAT_1)

                    time_tuple = (start_time, end_time)

                    groups[group_name][weekday_name].append(time_tuple)

        # print json.dumps(groups, indent=4, cls=DjangoJSONEncoder)

        logger.info("Deleting old schedules...")
        Schedule.objects.all().delete()

        for group_name, weekdays in groups.items():
            group_obj = Group.objects.get(name=group_name)

            for weekday, schedules in weekdays.items():
                for (start_time, end_time) in schedules:
                    logger.info("Saving %s, %s, %s, %s", group_name, weekday, start_time, end_time)
                    Schedule(
                        group=group_obj,
                        weekday=Schedule.day_of_week_actual_value(weekday),
                        start_time=start_time,
                        end_time=end_time
                    ).save()

