#!/usr/bin/env python
import os
import logging
import datetime

from django.core.management import BaseCommand
from django.db import transaction

from ls_schedule.apps.base.utils import CSVFile
from ls_schedule.apps.groups.models import Group
from ls_schedule.apps.schedule.models import Schedule

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2013 Poolsidelabs Inc.'

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        if not Group.objects.all():
            logger.error("Groups are not installed. Exiting...")
            return

        logger.info("Deleting old schedules...")
        Schedule.objects.all().delete()

        logger.info("Importing 'schedule'...")

        dir = os.path.dirname(__file__)
        csv_filepath = os.path.join(dir, '..', '..', '..', '..', '..', 'csv', 'schedule.csv')
        csv_file = CSVFile(csv_filepath)

        # fetch the 1st column (which is the list of groups)
        group_names = csv_file.elements_by_column(0)[1:]
        group_objs = [Group.objects.get(name=group_name) for group_name in group_names]

        # fetch the 1st row (which is the list of weekdays)
        weekdays = csv_file.elements_by_row(0)[1:]

        time_format = '%H:%M'

        for row_index in range(1, len(group_objs) + 1):
            group_obj = group_objs[row_index-1]

            for column_index in range(1, len(weekdays) + 1):
                weekday = weekdays[column_index-1]

                logger.info("Importing schedule for %s on %s..." % (group_obj.name, weekday))

                times = csv_file.element(row_index, column_index)
                if times:
                    time_list = [time.strip() for time in times.split('\n')]  # time entries are separated by new line
                    for time in time_list:
                        time_from_to = time.split('-')  # 08:45-17:00
                        time_from, time_to = time_from_to[0], time_from_to[1]  # ['08:45', '17:00']

                        # Quick fix: python only accepts hour range from 0:23.
                        time_from = time_from.replace('24:', '00:')
                        time_to = time_to.replace('24:', '00:')

                        start_time = datetime.datetime.strptime(time_from, time_format)
                        end_time = datetime.datetime.strptime(time_to, time_format)

                        Schedule(
                            group=group_obj,
                            weekday=Schedule.day_of_week_actual_value(weekday),
                            start_time=start_time,
                            end_time=end_time
                        ).save()
