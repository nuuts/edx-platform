"""
Tests for derived.py
"""

from unittest import TestCase
from openedx.core.lib.derived import derived, derive_settings, clear_for_tests


class TestDerivedSettings(TestCase):
    """
    Test settings that are derived from other settings.
    """
    def setUp(self):
        super(TestDerivedSettings, self).setUp()
        clear_for_tests()
        self.SIMPLE_VALUE = 'paneer'
        self.DERIVED_VALUE = lambda settings: 'mutter ' + settings.SIMPLE_VALUE
        self.ANOTHER_DERIVED_VALUE = lambda settings: settings.DERIVED_VALUE + ' with naan'
        self.UNREGISTERED_DERIVED_VALUE = lambda settings: settings.SIMPLE_VALUE + ' is cheese'
        derived('DERIVED_VALUE', 'ANOTHER_DERIVED_VALUE')
        self.DICT_VALUE = {}
        self.DICT_VALUE['test_key'] = lambda settings: self.DERIVED_VALUE * 3
        DERIVED_DICT_VALUE = {
            'getter': lambda settings: getattr(settings, 'DICT_VALUE')['test_key'],
            'setter': lambda settings, value: getattr(settings, 'DICT_VALUE').update({'test_key': value})
        }
        derived(DERIVED_DICT_VALUE)

    def test_derived_settings_are_derived(self):
        derive_settings(self)
        self.assertEqual(self.DERIVED_VALUE, 'mutter paneer')
        self.assertEqual(self.ANOTHER_DERIVED_VALUE, 'mutter paneer with naan')

    def test_unregistered_derived_settings(self):
        derive_settings(self)
        self.assertTrue(callable(self.UNREGISTERED_DERIVED_VALUE))

    def test_derived_settings_overridden(self):
        self.DERIVED_VALUE = 'aloo gobi'
        derive_settings(self)
        self.assertEqual(self.DERIVED_VALUE, 'aloo gobi')
        self.assertEqual(self.ANOTHER_DERIVED_VALUE, 'aloo gobi with naan')

    def test_derived_dict_settings(self):
        derive_settings(self)
        self.assertEqual(self.DICT_VALUE['test_key'], 'mutter paneermutter paneermutter paneer')
