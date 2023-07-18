import glob
import importlib
import json
import logging
import os.path
import sys
from json import JSONDecodeError
from typing import Union, Set, List

from maltego_trx.handler import handle_run
from maltego_trx.registry import register_transform_classes
from maltego_trx.server import app as application

from extensions import registry

whitelist: Union[List, Set, None] = None

try:
    with open("config.json", "r") as config_json:
        config = json.load(config_json)
        whitelist: List[str] = config.get("activated_modules", [])
except (OSError, JSONDecodeError) as e:
    pass

for module in glob.glob("modules/**/transforms", recursive=True):
    module_name = module.split("/")[1]

    if whitelist and module_name not in whitelist:
        continue

    logging.info(f"Importing module {module}")
    module_py = module.replace(os.path.sep, ".")
    module_imp = importlib.import_module(module_py)

    register_transform_classes(module_imp)

registry.write_transforms_config(whitelist=whitelist)
registry.write_settings_config(whitelist=whitelist)

registry.write_local_mtz(command="./venv/bin/python3", whitelist=whitelist)
registry.write_module_mtzs(command="./venv/bin/python3", whitelist=whitelist)

if __name__ == "__main__":
    handle_run(__name__, sys.argv, application)
