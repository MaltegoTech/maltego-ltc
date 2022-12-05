from modules.punycode.extensions import punycode_registry

# Import your transforms here
from transforms import PunyCodeToUnicode

if __name__ == "__main__":
    punycode_registry.write_transforms_config()
    punycode_registry.write_settings_config()
    punycode_registry.write_local_mtz(command="./venv/bin/python3")
