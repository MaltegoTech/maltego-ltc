from extensions import registry
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

@registry.register_transform(display_name="Phrase to SSID", input_entity="maltego.Phrase",
                             description='Returns an SSID entity from a Phrase',
                             output_entities=["maltego.network.SSID"])
class Phrase2GenSSID(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        ssid_phrase = request.Value
        ssid_common = { "guest", "office","staff","corporate" }
        for ssid_list in ssid_common:
            ssid_name = ssid_phrase + "-" + ssid_list
            response.addEntity("maltego.wirelessSSID", ssid_name)
