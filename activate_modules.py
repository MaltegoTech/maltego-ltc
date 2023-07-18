#!/usr/bin/python3
import json
from json import JSONDecodeError
from typing import List

import inquirer

from extensions import registry

try:
    with open("config.json", "r") as config_json:
        config = json.load(config_json)
        activated_modules: List[str] = config.get("activated_modules", [])
except (OSError, JSONDecodeError) as e:
    config = {}
    activated_modules = []

choices = [
    (f"{k} [by {v.author}, {v.owner}]", k)
    for k, v in registry.registries.items()
]

questions = [
    inquirer.Checkbox(
        'modules',
        message="What modules do you want to activate?",
        choices=choices,
        default=activated_modules,
    )
]

answers = inquirer.prompt(questions)
if updated_activated_modules := answers.get('modules'):
    print(f"Activated modules: {', '.join(updated_activated_modules)}")

    with open("config.json", "w") as config_json:
        json.dump(
            {
                **config,
                **{"activated_modules": updated_activated_modules}
            },
            config_json,
            indent=2)
