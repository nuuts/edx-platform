"""
Allows the registration of Django/Python settings that are derived from other settings
via callable methods/lambdas. The derivation time can be controlled to happen after all
other settings have been set. The derived setting can also be overridden by setting the
derived setting to an actual value.
"""
import six

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
        if isinstance(setting_name, six.string_types):
            # For a simple attribute, the getter and setter are simply getattr and setattr.
            setting = getattr(module, setting_name)
            if callable(setting):
                setting_val = setting(module)
                setattr(module, setting_name, setting_val)
        elif isinstance(setting_name, dict):
            # To allow more complex values such as values of dictionary with a particular key,
            # you can write your own getter and setter and register them as dictionary.
            # A dictionary setting is expected to have two keys - 'getter' and 'setter'.
            # The 'getter' value is a callable that gets the derived value from the module.
            # The 'setter' value is a callable that sets the derived value into the module.
            getter = setting_name['getter']
            setting = getter(module)
            if callable(setting):
                setting_val = setting(module)
                setter = setting_name['setter']
                setter(module, setting_val)

def clear_for_tests():
    """
    Clears all settings to be derived. For tests only.
    """
    global __DERIVED
    __DERIVED = []