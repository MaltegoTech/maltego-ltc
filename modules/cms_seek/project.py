from modules.cms_seek.extensions import cms_seek_registry

# Import your transforms here
from transforms import GreetPerson

if __name__ == "__main__":
    cms_seek_registry.write_local_mtz(command="./venv/bin/python3")
