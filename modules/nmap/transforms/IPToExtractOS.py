import os
import re

from maltego_trx.entities import IPAddress, Phrase
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.nmap.extensions import nmap_registry, nmap_set
from modules.nmap.utils.commands import COMMANDS
from modules.nmap.utils.nmap_interaction import NmapOrchestrator
from modules.nmap.utils.toentities import dict_to_entities
from modules.nmap.config import TOP_PORT_SCAN_NUMBER

config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")

@nmap_registry.register_transform(display_name="Extract OS", input_entity=IPAddress,
                                  description=f'Extract the operating system that NMAP added as properties',
                                  output_entities=[Phrase],
                                  transform_set=nmap_set)
class IPToExtractOS(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        if "Operating_system" in request.Properties:
            response.addEntity(type=Phrase, value=request.Properties["Operating_system"])

