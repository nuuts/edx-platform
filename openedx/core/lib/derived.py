"""
Allows the registration of Django/Python settings that are derived from other settings
via callable methods/lambdas. The derivation time can be controlled to happen after all
other settings have been set. The derived setting can also be overridden by setting the
derived setting to an actual value.
"""

import logging
log = logging.getLogger(__name__)

# Global list holding all settings which will be derived.
__DERIVED = []

def derived(*settings):
    """
    Registers settings which are derived from other settings.
    Can be called multiple times to add more derived settings to the list.

    Params:
        - settings (list): List of setting names to register.
    """
    __DERIVED.extend(settings)


def derive_settings(module):
    """
    Derives all registered settings and sets them onto a particular module.
    Skips deriving settings that are set to a value.

    Params:
        - module (module): Module to which the derived settings will be added.
    """
    for setting_name in __DERIVED:
        try:
            setting = getattr(module, setting_name)
        except ValueError:
            log.warning("Derived setting '%s' was not found - ignoring.", setting_name)
            continue
        if callable(setting):
            setting_val = setting(module)
            setattr(module, setting_name, setting_val)
            log.info("Setting '%s' to derived value '%s' in module '%s'", setting_name, setting_val, module)
