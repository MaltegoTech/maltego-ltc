from maltego_trx.entities import Domain
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from ..utils import punyapi

from modules.punycode.extensions import punycode_registry, punycode_set


@punycode_registry.register_transform(display_name="Punny Code to Unicode", input_entity="maltego.Domain",
                                   description='Returns a unicode domain',
                                   output_entities=["maltego.Domain"],
                                   transform_set=punycode_set)
class PunyCodeToUnicode(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        asciidomain = request.Value
        unicodedomain = punyapi.toUnicode(asciidomain)
        ent = response.addEntity(Domain, unicodedomain)
        #ent.addProperty(fieldName="domain", displayName="Domain", value=unicodedomain)
        ent.addProperty(fieldName="domain", displayName="domain", value=unicodedomain)
