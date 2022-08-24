from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi

@registry.register_transform(display_name="To IPs on Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves IPv4/v6 IOCs from Website',
                             output_entities=["maltego.IPv4", "maltego.IPv6"],
                             transform_set=IoCparser)
class WebsiteToIoCsIPAddresses(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        if iocs:
            for key in iocs['data']:
                for ipv4 in iocs['data']['IPv4']:
                    response.addEntity("maltego.IPv4Address", ipv4)
                for ipv6 in iocs['data']['IPv6']:
                    response.addEntity("maltego.IPv6Address", ipv6)
        else:
            response.addUIMessage("No indicator found on Website", UIM_INFORM)