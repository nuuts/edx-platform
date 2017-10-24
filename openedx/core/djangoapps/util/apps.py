"""
Configuration for the openedx.core.djangoapps.util Django application
"""

from django.apps import AppConfig


class UtilConfig(AppConfig):
    """
    Let Django know that this is an app with management commands.
    """
    name = 'openedx.core.djangoapps.util'
    verbose_name = 'Open edX Utilities'
