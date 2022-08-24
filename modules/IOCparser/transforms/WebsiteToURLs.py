from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform
from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi

@registry.register_transform(display_name="To URLs on Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves IOCs from Website',
                             output_entities=["maltego.URL", "maltego.IPv4", "maltgo.Hash","maltego.IPv6","maltego.domain","maltego.EmailAddress","maltego.Filename"],
                             transform_set=IoCparser)
class WebsiteToURLs(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        if iocs:
            for key in iocs['data']:
                    for url in iocs['data']['URL']:
                        ent = response.addEntity("maltego.URL", url)
                        ent.addProperty(fieldName="url",displayName="URL",value=url)
        else:
            response.addUIMessage("No indicator found on Website", UIM_INFORM)