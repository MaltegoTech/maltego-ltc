from modules.dnstwist.extensions import dnstwist_registry

# Import your transforms here
from transforms import ToRegisteredDomains

if __name__ == "__main__":
    dnstwist_registry.write_transforms_config()
    dnstwist_registry.write_settings_config()
    dnstwist_registry.write_local_mtz(command="./venv/bin/python3")

