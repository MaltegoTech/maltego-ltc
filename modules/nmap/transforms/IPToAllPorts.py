import os

from maltego_trx.entities import Phrase, DNS, IPAddress
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.nmap.extensions import nmap_registry, nmap_set
from modules.nmap.utils.commands import COMMANDS
from modules.nmap.utils.nmap_interaction import NmapOrchestrator
from modules.nmap.utils.toentities import dict_to_entities
from modules.nmap.config import TOP_PORT_SCAN_NUMBER

config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")

# TODO check the description of all transforms
@nmap_registry.register_transform(display_name="To All Ports", input_entity=IPAddress,
                                  description=f'Scans for all ports from 1 to 65535. Command: "-p-"',
                                  output_entities=[IPAddress],
                                  transform_set=nmap_set)
class IPToAllPorts(DiscoverableTransform):
    # TODO TESTED
    CMD = "{target} -p-"
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        ipadd = request.Value
        parsing_function = COMMANDS[cls.CMD]
        cmd = cls.CMD.format(target=ipadd)
        cont = NmapOrchestrator.execute_command(cmd, parsing_function)
        dict_to_entities(cont, response)
