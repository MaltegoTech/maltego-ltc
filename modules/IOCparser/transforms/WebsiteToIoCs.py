from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform
from modules.IOCparser.extensions import iocparser_registry as registry
from modules.IOCparser.extensions import iocparser_set as IoCparser

from ..utils import iocapi

@registry.register_transform(display_name="To all IoCs on Website [IoC-Parser]", input_entity="maltego.URL",
                             description='Retrieves IOCs from Website',
                             output_entities=["maltego.URL", "maltego.IPv4", "maltgo.Hash","maltego.IPv6","maltego.domain","maltego.EmailAddress","maltego.Filename"],
                             transform_set=IoCparser)
class WebsiteToIoCs(DiscoverableTransform):
    @classmethod
    def create_entities(cls,request: MaltegoMsg, response: MaltegoTransform):
        website = request.Value
        iocs = iocapi.getIOC(website)
        if iocs:
            for key in iocs['data']:
                    for domain in iocs['data']['DOMAIN']:
                        response.addEntity("maltego.Domain", domain)
                    for ipv4 in iocs['data']['IPv4']:
                        response.addEntity("maltego.IPv4Address", ipv4)
                    for ipv6 in iocs['data']['IPv6']:
                        response.addEntity("maltego.IPv6Address", ipv6)
                    for filename in iocs['data']['FILE_NAME']:
                        response.addEntity("maltego.Filename", filename)
                    for sha2 in iocs['data']['FILE_HASH_SHA256']:
                        ent = None
                        ent = response.addEntity("maltego.Hash", sha2)
                        ent.addProperty(fieldName="type", displayName="Type",value="sha256")
                    for sha1 in iocs['data']['FILE_HASH_SHA1']:
                        ent = None
                        ent = response.addEntity("maltego.Hash", sha1)
                        ent.addProperty(fieldName="type", displayName="Type",value="sha1")
                    for md5 in iocs['data']['FILE_HASH_MD5']:
                        ent = None
                        ent = response.addEntity("maltego.Hash", md5)
                        ent.addProperty(fieldName="type", displayName="Type",value="md5")
                    for cve in iocs['data']['CVE']:
                        response.addEntity("maltego.CVE", cve)
                    for email in iocs['data']['EMAIL']:
                        response.addEntity("maltego.EmailAddress", email)
                    for tactic in iocs['data']['MITRE_ATT&CK']:
                        response.addEntity("misp.AttackTechnique", tactic)
                    for url in iocs['data']['URL']:
                        ent = None
                        ent = response.addEntity("maltego.URL", url)
                        ent.addProperty(fieldName="url",displayName="URL",value=url)
        else:
            response.addUIMessage("No indicator found on Website", UIM_INFORM)