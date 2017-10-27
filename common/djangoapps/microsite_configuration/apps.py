
import logging
from django.apps import AppConfig
from microsite_configuration import microsite

log = logging.getLogger(__name__)


class MicrositeConfigurationConfig(AppConfig):
    name = 'common.djangoapps.microsite_configuration'
    verbose_name = "Microsite Configuration"

    def ready(self):
        # Mako requires the directories to be added after the django setup.
        microsite.enable_microsites(log)
