from maltego_trx.entities import Domain
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from ..utils import punyapi

from modules.punycode.extensions import punycode_registry, punycode_set


@punycode_registry.register_transform(display_name="Unicode to Punny Code", input_entity="maltego.Domain",
                                   description='Returns a Unicode Phrase of punycode domains',
                                   output_entities=["maltego.Domain"],
                                   transform_set=punycode_set)
class UnicodeToPunycode(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        domain = request.Value
        punycodedomain = punyapi.toPunycode(domain)
        ent = response.addEntity(Domain, punycodedomain)
