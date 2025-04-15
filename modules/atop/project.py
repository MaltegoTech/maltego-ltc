from modules.atop.extensions import atop_registry

if __name__ == "__main__":
    atop_registry.write_settings_config()
    atop_registry.write_transforms_config()
    atop_registry.write_local_mtz(command="./venv/bin/python3")
