from modules.ghunt.extensions import ghunt_registry

# Import your transforms here
from transforms import ghuntFromDrive
from transforms import ghuntFromEmail
from transforms import ghuntToReviews

if __name__ == "__main__":
    ghunt_registry.write_transforms_config()
    ghunt_registry.write_settings_config()
    ghunt_registry.write_local_mtz(command="./venv/bin/python3")
