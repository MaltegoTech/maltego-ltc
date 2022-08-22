from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi

@registry.register_transform(display_name="Hashes from Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves Hash(md5,sha1,sha256) IOCs from Website',
                             output_entities=["maltgo.Hash"],
                             transform_set=IoCparser)

class WebsiteToIoCsHash(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        for key in iocs['data']:
                for sha2 in iocs['data']['FILE_HASH_SHA256']:
                    sha2 = response.addEntity("maltego.Hash", sha2)
                    sha2.addProperty(fieldName="type", displayName="Type",value="sha256")
                for sha1 in iocs['data']['FILE_HASH_SHA1']:
                    sha1 = response.addEntity("maltego.Hash", sha1)
                    sha1.addProperty(fieldName="type", displayName="Type",value="sha1")
                for md5 in iocs['data']['FILE_HASH_MD5']:
                    md5 = response.addEntity("maltego.Hash", md5)
                    md5.addProperty(fieldName="type", displayName="Type",value="md5")