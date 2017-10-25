"""
Tests for derived.py
"""

from unittest import TestCase
from openedx.core.lib.derived import derived, derive_settings

class TestDerivedSettings(TestCase):
    """
    Test settings that are derived from other settings.
    """
    def setUp(self):
        super(TestDerivedSettings, self).setUp()
        self.SIMPLE_VALUE = 'paneer'
        self.DERIVED_VALUE = lambda settings: 'mutter ' + settings.SIMPLE_VALUE
        self.ANOTHER_DERIVED_VALUE = lambda settings: settings.DERIVED_VALUE + ' with naan'
        self.UNREGISTERED_DERIVED_VALUE = lambda settings: settings.SIMPLE_VALUE + ' is cheese'
        derived('DERIVED_VALUE', 'ANOTHER_DERIVED_VALUE')

    def test_derived_settings_are_derived(self):
        derive_settings(self)
        self.assertEqual(self.DERIVED_VALUE, 'mutter paneer')
        self.assertEqual(self.ANOTHER_DERIVED_VALUE, 'mutter paneer with naan')

    def test_unregistered_derived_settings(self):
        derive_settings(self)
        self.assertEqual(self.DERIVED_VALUE, 'mutter paneer')
        self.assertTrue(callable(self.UNREGISTERED_DERIVED_VALUE))

    def test_derived_settings_overridden(self):
        self.DERIVED_VALUE = 'aloo gobi'
        derive_settings(self)
        self.assertEqual(self.DERIVED_VALUE, 'aloo gobi')
        self.assertEqual(self.ANOTHER_DERIVED_VALUE, 'aloo gobi with naan')
