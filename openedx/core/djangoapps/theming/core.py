"""
Core logic for Comprehensive Theming.
"""
from logging import getLogger

from django.conf import settings
from path import Path as path

from .helpers import get_themes

logger = getLogger(__name__)  # pylint: disable=invalid-name


def enable_theming():
    """
    Add directories and relevant paths to settings for comprehensive theming.
    """
    # Add Mako template paths to settings for comprehensive theming.
    for theme in get_themes():
        if theme.themes_base_dir not in settings.MAKO_TEMPLATES['main']:
            settings.MAKO_TEMPLATES['main'].insert(0, theme.themes_base_dir)

    # Add locale paths to settings for comprehensive theming.
    theme_locale_paths = settings.COMPREHENSIVE_THEME_LOCALE_PATHS
    for locale_path in theme_locale_paths:
        settings.LOCALE_PATHS += (path(locale_path), )  # pylint: disable=no-member
