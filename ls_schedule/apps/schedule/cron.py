#!/usr/bin/env python
from django.core.management import call_command

import kronos

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2014 Poolsidelabs Inc.'


# @kronos.register('0 */3 * * *')  # Every 3 hours
# def check_for_new_schedule():
#     call_command('check_for_new_schedule')


@kronos.register('0 */3 * * *')  # Every 3 hours
def scrap_schedule():
    call_command('scrap_schedule')