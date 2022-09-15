import os

from maltego_trx.entities import Phrase, DNS, IPAddress
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.nmap.extensions import nmap_registry, nmap_set
from modules.nmap.utils.commands import COMMANDS
from modules.nmap.utils.nmap_interaction import NmapOrchestrator
from modules.nmap.utils.toentities import dict_to_entities
from modules.nmap.config import SET_OF_PORTS_TO_SCAN, CONFIG_FILE_PATH

config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")


@nmap_registry.register_transform(display_name="Scan set of ports (-p -A)", input_entity="maltego.CIDR",
                                  description=f'Scans for a selection of ports. The set of ports can be changed in '
                                              f'{CONFIG_FILE_PATH}. Command: "-p -A"',
                                  output_entities=[IPAddress],
                                  transform_set=nmap_set)
class NetblockToSetOfPorts(DiscoverableTransform):
    CMD = "{target} -p {ports} -A"

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        ipadd = request.Value
        parsing_function = COMMANDS[cls.CMD]

        formatted_ports = NmapOrchestrator.get_formatted_ports()

        cmd = cls.CMD.format(target=ipadd, ports=formatted_ports)
        try:
            cont = NmapOrchestrator.execute_command(cmd, parsing_function)
        except Exception as e:
            response.addUIMessage(message=str(e), messageType='FatalError')
            return
        dict_to_entities(cont, response)
