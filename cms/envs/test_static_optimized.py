"""
Settings used when generating static assets for use in tests.

For example, Bok Choy uses two different settings files:
1. test_static_optimized is used when invoking collectstatic
2. bok_choy is used when running CMS and LMS

Note: it isn't possible to have a single settings file, because Django doesn't
support both generating static assets to a directory and also serving static
from the same directory.
"""

# Start with the common settings
from .common import *  # pylint: disable=wildcard-import, unused-wildcard-import
from openedx.core.djangoapps.theming.helpers_dirs import (
    get_theme_base_dirs_from_settings,
    enable_theming_with_settings
)

# Use an in-memory database since this settings file is only used for updating assets
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'ATOMIC_REQUESTS': True,
    },

}

######################### PIPELINE ####################################

# Use RequireJS optimized storage
STATICFILES_STORAGE = 'openedx.core.lib.django_require.staticstorage.OptimizedCachedRequireJsStorage'

# Revert to the default set of finders as we don't want to dynamically pick up files from the pipeline
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'openedx.core.lib.xblock_pipeline.finder.XBlockPipelineFinder',
]

# Redirect to the test_root folder within the repo
TEST_ROOT = REPO_ROOT / "test_root"
LOG_DIR = (TEST_ROOT / "log").abspath()

# Store the static files under test root so that they don't overwrite existing static assets
STATIC_ROOT = (TEST_ROOT / "staticfiles" / "cms").abspath()
WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = STATIC_ROOT / "webpack-stats.json"

# Disable uglify when tests are running (used by build.js).
# 1. Uglify is by far the slowest part of the build process
# 2. Having full source code makes debugging tests easier for developers
os.environ['REQUIRE_BUILD_PROFILE_OPTIMIZE'] = 'none'

########################## Comprehensive Theming  #######################

# Set up comprehensive theming after all other settings have been set to avoid
# modifying paths before ENABLE_COMPREHENSIVE_THEMING has its final value.
if ENABLE_COMPREHENSIVE_THEMING:
    LOCALE_PATHS = enable_theming_with_settings(
        MAKO_TEMPLATES['main'],
        get_theme_base_dirs_from_settings(COMPREHENSIVE_THEME_DIRS),
        LOCALE_PATHS,
        COMPREHENSIVE_THEME_LOCALE_PATHS
    )
