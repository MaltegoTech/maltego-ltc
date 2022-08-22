from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi


@registry.register_transform(display_name="Email addresses from Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves email address IOCs from Website',
                             output_entities=["maltego.EmailAddress"],
                             transform_set=IoCparser)
class WebsiteToIoCsEmail(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        for email in iocs['data']['EMAIL']:
            response.addEntity("maltego.EmailAddress", email)