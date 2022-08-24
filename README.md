# Install

1. Install Python 3.7 or newer
2. Clone LTC to a local folder and change into the path 
```
git clone https://dw@dev.azure.com/MaltegoTech/support/_git/maltego-ltc
cd maltego-ltc
```

4. Install dependencies in virtualenv
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Update the path in the Config file

```shell
python3 project.py list
```

6. Import the Maltego Config file `local.mtz` into Maltego.

# Info
To recreate the `local.mtz` just run `python3 project.py list`

# Modules

We advise the following structure. In any case, the transforms **need** to be in a dir called `transforms`.

```
modules
└── <module_name>
    └── transforms
        └── <transform_name>.py
```

You can optionally specify a `whitelist` or `blacklist` in `project.py`. To disable them set them to `None`


## Create a module
To create a module 

1. use the python script `create_module.py`. The script needs following positional arguments: name author owner.

```shell
usage: create_module.py [-h] name author owner

positional arguments:
  name        The module name
  author      your email address, alias or Fullname
  owner       You, or the organization you write this module for
```

e.g.

```shell
python3 create_module.py my_module me@myself.com "Me Inc."
```

2. Edit in the top-level of the `extensions.py` file and add following lines:   
```
from modules.{name}.extensions import {name}_registry

registry.include_registry("{name}", {name}_registry
```

e.g. name = 'cisa'

```
from meta_registry import MetaRegistry
from modules.cisa.extensions import cisa_registry

registry = MetaRegistry()
registry.include_registry("cisa", cisa_registry)
```


