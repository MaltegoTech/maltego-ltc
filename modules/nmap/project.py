from modules.nmap.extensions import nmap_registry

# Import your transforms here
from transforms import GreetPerson

if __name__ == "__main__":
    nmap_registry.write_local_mtz(command="./venv/bin/python3")
