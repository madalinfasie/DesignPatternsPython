"""
Implement a configuration class that acts as a singleton

To test that we use the same instance, the id function was used.
"""

from singleton_module import CONFIG
import singleton_module_user

print('INSIDE singleton_module_main - from module', id(CONFIG))
print('INSIDE singleton_module_main - from user', id(singleton_module_user.CONFIG))