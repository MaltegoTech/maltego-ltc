from modules.wigle.extensions import wigle_registry
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

@wigle_registry.register_transform(display_name="Phrase to SSID", input_entity="maltego.Phrase",
                             description='Returns an SSID entity from a Phrase',
                             output_entities=["maltego.network.SSID"])
class Phrase2SSID(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        ssid_phrase = request.Value
        response.addEntity("maltego.wirelessSSID", ssid_phrase)
