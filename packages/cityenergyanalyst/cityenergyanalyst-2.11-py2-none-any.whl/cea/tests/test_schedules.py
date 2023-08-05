"""
This module contains unit tests for the schedules used by the CEA. The schedule code is tested against data in the
file `test_schedules.config` that can be created by running this file. Note, however, that this will overwrite the
test data - you should only do this if you are sure that the new data is correct.
"""

import os
import unittest
import pandas as pd
import json
import ConfigParser
from cea.inputlocator import ReferenceCaseOpenLocator
from cea.datamanagement.data_helper import calculate_average_multiuse
from cea.datamanagement.data_helper import correct_archetype_areas
from cea.datamanagement.data_helper import get_database
from cea.demand.occupancy_model import calc_schedules
from cea.demand.occupancy_model import schedule_maker
from cea.globalvar import GlobalVariables
import cea.config
from cea.demand.building_properties import BuildingProperties

REFERENCE_TIME = 3456


class TestBuildingPreprocessing(unittest.TestCase):
    def test_mixed_use_archetype_values(self):
        # test if a sample mixed use building gets standard results
        locator = ReferenceCaseOpenLocator()
        config = ConfigParser.SafeConfigParser()
        config.read(get_test_config_path())

        calculated_results = calculate_test_mixed_use_archetype_values_results(locator).to_dict()

        # compare to reference values
        expected_results = json.loads(config.get('test_mixed_use_archetype_values', 'expected_results'))
        for column, rows in expected_results.items():
            self.assertIn(column, calculated_results)
            for building, value in rows.items():
                self.assertIn(building, calculated_results[column])
                self.assertAlmostEqual(value, calculated_results[column][building], 4)

        architecture_DB = get_database(locator.get_archetypes_properties('CH'), 'ARCHITECTURE')
        architecture_DB['Code'] = architecture_DB.apply(lambda x: x['building_use'] + str(x['year_start']) +
                                                                  str(x['year_end']) + x['standard'], axis=1)

        self.assertEqual(correct_archetype_areas(
            prop_architecture_df=pd.DataFrame(
                data=[['B1', 0.5, 0.5, 0.0, 2006, 2020, 'C'], ['B2', 0.2, 0.8, 0.0, 1000, 1920, 'R']],
                columns=['Name', 'SERVERROOM', 'PARKING', 'Hs', 'year_start', 'year_end', 'standard']),
            architecture_DB=architecture_DB,
            list_uses=['SERVERROOM', 'PARKING']),
            ([0.5, 0.2], [0.5, 0.2], [0.95, 0.9200000000000002]))


class TestScheduleCreation(unittest.TestCase):
    def test_mixed_use_schedules(self):
        locator = ReferenceCaseOpenLocator()
        config = cea.config.Configuration(cea.config.DEFAULT_CONFIG)
        config.scenario = locator.scenario
        stochastic_occupancy = config.demand.use_stochastic_occupancy
        gv = GlobalVariables()
        gv.config = config


        date = pd.date_range(gv.date_start, periods=8760, freq='H')

        building_properties = BuildingProperties(locator, False, 'CH', False)
        bpr = building_properties['B01']
        list_uses = ['OFFICE', 'INDUSTRIAL']
        bpr.occupancy = {'OFFICE': 0.5, 'INDUSTRIAL': 0.5}

        # calculate schedules
        archetype_schedules, archetype_values = schedule_maker('CH', date, locator, list_uses)
        calculated_schedules = calc_schedules(list_uses, archetype_schedules, bpr, archetype_values,
                                              stochastic_occupancy)

        config = ConfigParser.SafeConfigParser()
        config.read(get_test_config_path())
        reference_results = json.loads(config.get('test_mixed_use_schedules', 'reference_results'))

        for schedule in reference_results:
            self.assertAlmostEqual(calculated_schedules[schedule][REFERENCE_TIME], reference_results[schedule],
                                   places=4, msg="Schedule '%s' at time %s, %f != %f" % (
                schedule, str(REFERENCE_TIME), calculated_schedules[schedule][
                    REFERENCE_TIME],
                reference_results[schedule]))


def get_test_config_path():
    """return the path to the test data configuration file (``cea/tests/test_schedules.config``)"""
    return os.path.join(os.path.dirname(__file__), 'test_schedules.config')


def calculate_test_mixed_use_archetype_values_results(locator):
    """calculate the results for the test - refactored, so we can also use it to write the results to the
    config file."""
    office_occ = float(pd.read_excel(locator.get_archetypes_schedules('CH'), 'OFFICE').T['density'].values[:1][0])
    gym_occ = float(pd.read_excel(locator.get_archetypes_schedules('CH'), 'GYM').T['density'].values[:1][0])
    calculated_results = calculate_average_multiuse(
        properties_df=pd.DataFrame(data=[['B1', 0.5, 0.5, 0.0, 0.0], ['B2', 0.25, 0.75, 0.0, 0.0]],
                                   columns=['Name', 'OFFICE', 'GYM', 'X_ghp', 'El_Wm2']),
        occupant_densities={'OFFICE': 1 / office_occ, 'GYM': 1 / gym_occ},
        list_uses=['OFFICE', 'GYM'],
        properties_DB=pd.read_excel(locator.get_archetypes_properties('CH'), 'INTERNAL_LOADS')).set_index('Name')
    return calculated_results


def create_test_data():
    """Create test data to compare against - run this the first time you make changes that affect the results. Note,
    this will overwrite the previous test data."""
    test_config = ConfigParser.SafeConfigParser()
    test_config.read(get_test_config_path())
    if not test_config.has_section('test_mixed_use_archetype_values'):
        test_config.add_section('test_mixed_use_archetype_values')
    locator = ReferenceCaseOpenLocator()
    expected_results = calculate_test_mixed_use_archetype_values_results(locator)
    test_config.set('test_mixed_use_archetype_values', 'expected_results', expected_results.to_json())

    config = cea.config.Configuration(cea.config.DEFAULT_CONFIG)
    gv = GlobalVariables()
    gv.config = config
    locator = ReferenceCaseOpenLocator()

    # calculate schedules
    building_properties = BuildingProperties(locator, False, 'CH', False)
    bpr = building_properties['B01']
    list_uses = ['OFFICE', 'INDUSTRIAL']
    bpr.occupancy = {'OFFICE': 0.5, 'INDUSTRIAL': 0.5}
    gv = GlobalVariables()
    date = pd.date_range(gv.date_start, periods=8760, freq='H')
    archetype_schedules, archetype_values = schedule_maker('CH', date, locator, list_uses)
    stochastic_occupancy = config.demand.use_stochastic_occupancy
    calculated_schedules = calc_schedules(list_uses, archetype_schedules, bpr, archetype_values,
                                          stochastic_occupancy)
    if not test_config.has_section('test_mixed_use_schedules'):
        test_config.add_section('test_mixed_use_schedules')
    test_config.set('test_mixed_use_schedules', 'reference_results', json.dumps(
        {schedule: calculated_schedules[schedule][REFERENCE_TIME] for schedule in calculated_schedules.keys()}))

    with open(get_test_config_path(), 'w') as f:
        test_config.write(f)


if __name__ == '__main__':
    create_test_data()
