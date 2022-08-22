from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform
from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi


@registry.register_transform(display_name="Domains from Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves domain IOCs from Website',
                             output_entities=["maltego.domain"],
                             transform_set=IoCparser)
class WebsiteToIoCsDomain(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        for key in iocs['data']:
                for domain in iocs['data']['DOMAIN']:
                    response.addEntity("maltego.Domain", domain)