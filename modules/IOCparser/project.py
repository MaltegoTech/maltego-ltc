from modules.IOCparser.extensions import iocparser_registry

# noinspection PyUnresolvedReferences
#from transforms import CisaCheckCVE

if __name__ == "__main__":
    iocparser_registry.write_transforms_config()
    iocparser_registry.write_settings_config()
    iocparser_registry.write_local_mtz(command="./venv/bin/python3")

