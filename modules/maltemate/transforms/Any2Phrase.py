from extensions import registry
from maltego_trx.entities import Phrase
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform

from maltego_trx.transform import DiscoverableTransform

@registry.register_transform(display_name="Person to Phrase", input_entity="maltego.Unknown",
                             description='Returns a Phrase from any entity',
                             output_entities=["maltego.Phrase"])
class Any2Phrase(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        response.addEntity(Phrase, f"\"{request.Value}\"")
