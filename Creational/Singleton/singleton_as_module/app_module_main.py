"""
We want to develop an app that has a single configuration file.
Make the configuration class a Singleton.

To test that we use the same instance, I used the id function.
"""

from singleton_module import CONFIG
import app_module

print(f"INSIDE {__name__} - from module", id(CONFIG))
print(f"INSIDE {__name__} - from user", id(app_module.CONFIG))
