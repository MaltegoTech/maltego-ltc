#!python
import argparse
import logging
import os
import string
import sys


def sample_transform(name: str):
    return f"""from maltego_trx.entities import Phrase
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.{name}.extensions import {name}_registry, {name}_set


@{name}_registry.register_transform(display_name="Greet Person", input_entity="maltego.Phrase",
                                   description='Returns a Phrase greeting a Person on the Graph.',
                                   output_entities=["maltego.Phrase"],
                                   transform_set={name}_set)
class GreetPerson(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        person_name = request.Value

        response.addEntity(Phrase, f"Hi %s, nice to meet you!".format(person_name))
"""


def make_extensions_py(owner: str, author: str, name: str):
    return f"""from maltego_trx.decorator_registry import TransformRegistry, TransformSet

{name}_registry = TransformRegistry(
    owner="{owner}",
    author="{author}",
    host_url="https://localhost:8080",
    seed_ids=["{name}"],
)
{name}_set = TransformSet("{name}", "{name} Transforms")
"""


def make_project_py(name: str):
    content = f"""from modules.{name}.extensions import {name}_registry

# Import your transforms here
from transforms import GreetPerson

if __name__ == "__main__":
    {name}_registry.write_local_mtz(command="./venv/bin/python3")
"""

    return content


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("name", help="The module name")
    parser.add_argument("author", help="your email address, alias or Fullname")
    parser.add_argument("owner", help="You, or the organization you write this module for")

    args = parser.parse_args()

    name = args.name
    author = args.author
    owner = args.owner

    valid_chars = string.ascii_letters + string.digits + "_"
    for c in name:
        if c not in valid_chars:
            logging.error(f"Character '{c}' is forbidden. Only letters, digits and _ are allowed")
            sys.exit(1)

    try:
        os.makedirs(f"./modules/{name}")
        os.makedirs(f"./modules/{name}/transforms")
    except OSError:
        logging.error(f"Module {name} already exists")

    with open(f"./modules/{name}/extensions.py", "w+") as extensions_py:
        extensions_py.write(make_extensions_py(author, owner, name))

    with open(f"./modules/{name}/project.py", "w+") as project_py:
        project_py.write(make_project_py(name))

    with open(f"./modules/{name}/transforms/GreetPerson.py", "w+") as greet_person_py:
        greet_person_py.write(sample_transform(name))


    print("All Done!")
    print()

    print("Now, in the top-level extensions.py:")
    print("1. Import your registry:")
    print(f"from modules.{name}.extensions import {name}_registry")
    print(

    )
    print("2. Add your registry to the global registry")
    print(f'registry.include_registry("{name}", {name}_registry)')