"""
Implement a configuration class that acts as a singleton
"""

class SingletonMeta(type):
    _instance = None
    def __call__(self, *args, **kwargs):
        if not self.__class__._instance:
            self.__class__._instance = super().__call__(*args, **kwargs)

        return self.__class__._instance


class Config(metaclass=SingletonMeta):
    def __init__(self, path: str):
        self.path = path

    def get_config(self) -> dict:
        # Open the file from self.path and load the values into a dictionary
        return {
            'HEIGHT': 200,
            'WIDTH': 300
        }


c1 = Config()
c2 = Config()

print(c1 is c2)
