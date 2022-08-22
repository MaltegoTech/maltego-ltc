from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform
from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi

@registry.register_transform(display_name="IoCs from Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves IOCs from Website',
                             output_entities=["maltego.URL", "maltego.IPv4", "maltgo.Hash","maltego.IPv6","maltego.domain","maltego.EmailAddress","malformity.Filename"],
                             transform_set=IoCparser)
class WebsiteToIoCs(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        for key in iocs['data']:
                for domain in iocs['data']['DOMAIN']:
                    response.addEntity("maltego.Domain", domain)
                for ipv4 in iocs['data']['IPv4']:
                    response.addEntity("maltego.IPv4Address", ipv4)
                for ipv6 in iocs['data']['IPv6']:
                    response.addEntity("maltego.IPv6Address", ipv6)
                for filename in iocs['data']['FILE_NAME']:
                    response.addEntity("malformity.Filename", filename)
                for sha2 in iocs['data']['FILE_HASH_SHA256']:
                    sha2 = response.addEntity("maltego.Hash", sha2)
                    sha2.addProperty(fieldName="type", displayName="Type",value="sha256")
                for sha1 in iocs['data']['FILE_HASH_SHA1']:
                    sha1 = response.addEntity("maltego.Hash", sha1)
                    sha1.addProperty(fieldName="type", displayName="Type",value="sha1")
                for md5 in iocs['data']['FILE_HASH_MD5']:
                    md5 = response.addEntity("maltego.Hash", md5)
                    md5.addProperty(fieldName="type", displayName="Type",value="md5")
                for cve in iocs['data']['CVE']:
                    response.addEntity("maltego.CVE", cve)
                for email in iocs['data']['EMAIL']:
                    response.addEntity("maltego.EmailAddress", email)