from modules.cisa.extensions import cisa_registry

# noinspection PyUnresolvedReferences
from transforms import CisaCheckCVE

if __name__ == "__main__":
    cisa_registry.write_transforms_config()
    cisa_registry.write_settings_config()
    cisa_registry.write_local_mtz(command="./venv/bin/python3")
