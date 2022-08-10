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

`python3 project.py list`

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