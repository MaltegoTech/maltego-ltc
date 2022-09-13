import os
import re

from maltego_trx.entities import IPAddress
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

from modules.nmap.extensions import nmap_registry, nmap_set
from modules.nmap.utils.commands import COMMANDS
from modules.nmap.utils.nmap_interaction import NmapOrchestrator
from modules.nmap.utils.toentities import dict_to_entities
from modules.nmap.config import TOP_PORT_SCAN_NUMBER

config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.py")

@nmap_registry.register_transform(display_name="Extract services", input_entity=IPAddress,
                                  description=f'Extract the services that NMAP added as properties',
                                  output_entities=["maltego.Service"],
                                  transform_set=nmap_set)
class IPToServices(DiscoverableTransform):

    service_reg = re.compile(r"^[a-z]{3,6}/\d+$")

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        for key, val in request.Properties.items():
            if cls.service_reg.match(key):
                port = key.split("/")[1]
                service_name, product, service_footprint = val.split('\n')
                ent = response.addEntity(type="maltego.Service", value=service_name)
                ent.addProperty(fieldName="port.number", displayName="Port", matchingRule="strict", value=port)
                ent.addProperty(fieldName="properties.service", displayName="Service", matchingRule="strict",
                                value=service_name)
                ent.addProperty(fieldName="product", displayName="product", matchingRule="strict", value=product)
                ent.addProperty(fieldName="banner.text", displayName="Service banner", matchingRule="strict", value="")
                ent.addProperty(fieldName="service_footprint", displayName="service_footprint", matchingRule="strict",
                                value=service_footprint)
