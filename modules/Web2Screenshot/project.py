from modules.Web2Screenshot.extensions import Web2Screenshot_registry

# Import your transforms here
from transforms import GreetPerson

if __name__ == "__main__":
    Web2Screenshot_registry.write_local_mtz(command="./venv/bin/python3")
