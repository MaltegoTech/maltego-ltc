from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi


#print(getIOC("https://blog.talosintelligence.com/2020/10/lemon-duck-brings-cryptocurrency-miners.html","URL"))

@registry.register_transform(display_name="To TTP on Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves Behavioural Indicators (TTPs ) from a Website',
                             output_entities=["maltego.Filename"],
                             transform_set=IoCparser)
class WebsiteToIoCsTTP(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        if iocs:
            for tactic in iocs['data']['MITRE_ATT&CK']:
                response.addEntity("misp.AttackTechnique", tactic)
        else:
            response.addUIMessage("No indicator found on Website", UIM_INFORM)