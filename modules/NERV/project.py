from modules.NERV.extensions import NERV_registry

# Import your transforms here
from transforms import ImageToPHash

if __name__ == "__main__":
    NERV_registry.write_local_mtz(command="./venv/bin/python3")
