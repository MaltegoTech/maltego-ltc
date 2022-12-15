from modules.wigle.extensions import wigle_registry

# noinspection PyUnresolvedReferences
from transforms import *

if __name__ == "__main__":
    wigle_registry.write_transforms_config()
    wigle_registry.write_settings_config()
    wigle_registry.write_local_mtz(command="./venv/bin/python3")
