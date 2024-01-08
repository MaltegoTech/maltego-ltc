
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from modules.atop.extensions import atop_registry, atop_set
from modules.atop.transforms.Util import Util

@atop_registry.register_transform(display_name="Scan for TON telephone number (+888)", input_entity="maltego.PhoneNumberMobile",
                                   description="Return the owner of the NFT and his details and related assets",
                                   output_entities=["maltego.Unknown"],
                                   transform_set=atop_set)
class AtopByMobile(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        if not Util.check_format(request.Value):
            response.addUIMessage("The Input is not a valid TON number, it should start with +888")
            return
        else:
            util = Util()
            util.create_atop_entities(request.Value, response)

