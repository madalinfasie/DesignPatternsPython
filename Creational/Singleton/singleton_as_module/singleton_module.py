class ConfigSingleton:
    def __init__(self, path: str):
        self.path = path

    def get_config(self) -> dict:
        # Open the file from self.path and load the values into a dictionary
        return {"HEIGHT": 200, "WIDTH": 300}


CONFIG = ConfigSingleton("path/to/config/file.json")
print(f"INSIDE {__name__}", id(CONFIG))
