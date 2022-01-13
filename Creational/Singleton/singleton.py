"""
We want to develop an app that has a single configuration file.
Make the configuration class a Singleton.

To test that we use the same instance, I used the id function.
"""

class SingletonMeta(type):
    _instance = None
    def __call__(self, *args, **kwargs):
        if not self.__class__._instance:
            self.__class__._instance = super().__call__(*args, **kwargs)

        return self.__class__._instance


class ConfigSingleton(metaclass=SingletonMeta):
    def __init__(self, path: str):
        self.path = path

    def get_config(self) -> dict:
        # Open the file from self.path and load the values into a dictionary
        return {
            'HEIGHT': 200,
            'WIDTH': 300
        }


config_app1 = ConfigSingleton('path/to/config.json')
config_app2 = ConfigSingleton('path/to/config.json')

print(config_app1 is config_app2)
