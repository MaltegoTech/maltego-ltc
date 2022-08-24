import os.path
import logging
import configparser

BASE_DIR = os.path.dirname(__file__)
CONFIGFILE: str = 'config.ini'


def read_config_file(section, option):
    try:
        config = configparser.ConfigParser()
        config.read(CONFIGFILE)
        return config.get(section, option).strip('"')
    except:
        logging.warn(f"Could not find the section {section} {option} in config file {CONFIGFILE}")
