import os.path

import nmap3

from modules.nmap.config import NMAP_EXECUTABLE

NMAP_PATH = NMAP_EXECUTABLE

if NMAP_EXECUTABLE == "":
    NMAP_PATH = nmap3.get_nmap_path()

# TODO this will give errors if people don't install NMAP, even though they don't plan to use it.
# call this as a function in the Transforms
if NMAP_PATH == '' and os.path.exists(NMAP_PATH):
    raise Exception("Couldn't find nmap path, please install it: https://nmap.org/")
