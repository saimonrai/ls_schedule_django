#!/usr/bin/env python
import os
import logging

from django.core.management import BaseCommand

from ls_schedule.apps.base.utils import CSVFile
from ls_schedule.apps.groups.models import Group, Substation, Area

__author__ = 'Saimon Rai'
__copyright__ = 'Copyright 2013 Poolsidelabs Inc.'

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        dir = os.path.dirname(__file__)

        logger.info("Importing 'groups' data for areas inside kathmandu...")
        groups_csv_filepath = os.path.join(dir, '..', '..', '..', '..', '..', 'csv', 'areas_in_ktm.csv')
        groups_csv_filepath_nep = os.path.join(dir, '..', '..', '..', '..', '..', 'csv', 'areas_in_ktm_nep.csv')
        self.import_data(groups_csv_filepath, groups_csv_filepath_nep, in_ktm=True)

        logger.info("Importing 'groups' data for areas outside kathmandu...")
        groups_csv_filepath = os.path.join(dir, '..', '..', '..', '..', '..', 'csv', 'areas_out_ktm.csv')
        groups_csv_filepath_nep = os.path.join(dir, '..', '..', '..', '..', '..', 'csv', 'areas_out_ktm_nep.csv')
        self.import_data(groups_csv_filepath, groups_csv_filepath_nep, in_ktm=False)

    def import_data(self, groups_csv_filepath, groups_csv_filepath_nep, in_ktm=True):
        csv_file = CSVFile(groups_csv_filepath)
        csv_file_nep = CSVFile(groups_csv_filepath_nep)

        # remove the first entry which is the column containing 'substation' names
        group_names = csv_file.elements_by_row(0)[1:]
        group_names_nep = csv_file_nep.elements_by_row(0)[1:]

        # remove the first row which is the column containing 'group' names
        substation_names = csv_file.elements_by_column(0)[1:]
        substation_names_nep = csv_file_nep.elements_by_column(0)[1:]

        # save the group objects
        group_count = len(group_names)
        group_objs = []
        for i in range(group_count):
            group, created = Group.objects.get_or_create(name=group_names[i].strip(), name_nep=group_names_nep[i])
            group_objs.append(group)

        # save the substation objects
        substation_count = len(substation_names)
        substation_objs = []
        for i in range(substation_count):
            substation = Substation(name=substation_names[i], name_nep=substation_names_nep[i], in_ktm=in_ktm)
            substation.save()
            substation_objs.append(substation)

        # save the area objects
        for ss_index in range(1, substation_count+1):
            substation = substation_objs[ss_index - 1]

            for group_index in range(1, group_count+1):
                group = group_objs[group_index-1]

                # a single area field can contain multiple comma-separated entries
                area_names = csv_file.element(ss_index, group_index)
                area_names_nep = csv_file_nep.element(ss_index, group_index)
                if not area_names or not area_names_nep:
                    continue

                area_names_list = area_names.split(',')
                area_names_nep_list = area_names_nep.split(',')

                for name, name_nep in zip(area_names_list, area_names_nep_list):
                    Area(name=name.strip(), name_nep=name_nep.strip(),
                        group=group, substation=substation, in_ktm=in_ktm).save()

