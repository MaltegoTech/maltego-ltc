from modules.maltemate.extensions import maltemate_registry

# noinspection PyUnresolvedReferences
from transforms import *

if __name__ == "__main__":
    maltemate_registry.write_transforms_config()
    maltemate_registry.write_settings_config()
    maltemate_registry.write_local_mtz(command="./venv/bin/python3")
