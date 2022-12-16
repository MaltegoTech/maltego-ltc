import re
import urllib.parse
import urllib3
import ipaddress

import validators

from modules.maltemate.extensions import maltemate_registry
from maltego_trx.entities import IPAddress, Phrase, Domain, URL, Hash
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform

RE_URL_DOMAIN = re.compile(r"[-a-z0-9()@:%_+.~#?&/=\[\]]*\[\.][-a-z0-9()@:%_+.~#?&/=]*", re.IGNORECASE)
RE_IP = re.compile(r"\b[\d]{1,3}\[?\.\]?[\d]{1,3}\[?\.\]?[\d]{1,3}\[?\.\]?[\d]{1,3}(:\d+)?\b")
RE_MD5 = re.compile(r"[A-Fa-f0-9]{32}")
RE_SHA256 = re.compile(r"[A-Fa-f0-9]{64}")


@registry.register_transform(display_name="To Refanged Domain/URL/IP", input_entity=Phrase,
                             description='Refangs the given Domain / URL / IP (ex: hxxps://google[.]com -> https://google.com)',
                             output_entities=[IPAddress, Domain, URL, Hash])
class PhraseDomainUrlIPToRefangedVersion(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        val = request.Value

        # removing the parenthesis from matches
        if val[0] == "(" and val[-1] == ")":
            val = val[1:-1]

        if RE_MD5.match(val) or RE_SHA256.match(val):
            response.addEntity(Hash, val)

        elif RE_IP.match(val):
            # removing the [.]
            val = val.replace("[.]", ".")
            # Maltego won't appreciate the port being included, we'll add it as a property instead
            port = ""
            if ":" in val:
                ip_val, port = val.split(":")
            else:
                ip_val = val
            # validating the IP address
            try:
                ipaddress.ip_address(ip_val)
                ent = response.addEntity(IPAddress, ip_val)
                if port:
                    ent.addProperty(fieldName="port", displayName="Port", value=port, matchingRule="strict")
            except Exception as e:
                response.addUIMessage(f"{val} maps to an invalid IP address: {ip_val}. Error: {e}",
                                      UIM_TYPES["partial"])

        elif RE_URL_DOMAIN.match(val):

            # removing the [.]
            val = val.replace("[.]", ".")
            # testing if it's a URL
            if "/" in val:
                if "[://]" in val:
                    val = val.replace("[://]", "://", 1)
                if "hxxp://" or "hxxps://" in val:
                    val = val.replace("hxxp", "http", 1)
                if not validators.url(val):
                    return
                ent = response.addEntity(URL, urllib3.get_host(val)[1])
                ent.addProperty(fieldName="url", displayName="URL", value=val, matchingRule="strict")
            else:
                if not validators.domain(val):
                    return
                ent = response.addEntity(Domain, val)

        else:
            response.addUIMessage(f"{val} didn't match any regex, is it really a defanged domain/urls/IP?",
                                  UIM_TYPES["partial"])

    @staticmethod
    def validate_domain(dom):
        hname = urllib.parse.urlparse(dom).hostname
        if not hname or not hname.isascii():
            return False
        else:
            return True


if __name__ == '__main__':
    print(PhraseDomainUrlIPToRefangedVersion.validate_domain("http://google.com"))
    print(PhraseDomainUrlIPToRefangedVersion.validate_domain("http://google.com/babylone.exe"))
    print(PhraseDomainUrlIPToRefangedVersion.validate_domain("http://google.coéém"))
    print(PhraseDomainUrlIPToRefangedVersion.validate_domain("(http://google.com)"))
    print(PhraseDomainUrlIPToRefangedVersion.validate_domain("143610035BAF04425847B007.mumbai-m.site"))

    DOM = "143610035BAF04425847B007.mumbai-m.site"
    ee = urllib.parse.urlparse(DOM)
    print(ee)
    ee = validators.domain(DOM)
    print(ee)

    print(RE_URL_DOMAIN.match("www.window5[.]win/update.aspx"))
    val = "www.window5[.]win/update.aspx"
    val = val.replace("[.]", ".")
    # testing if it's a URL
    if "/" in val:
        if "[://]" in val:
            val = val.replace("[://]", "://", 1)
        if "hxxp://" or "hxxps://" in val:
            val = val.replace("hxxp", "http", 1)

        eee = validators.url(val)
        aaa = urllib.parse.urlparse(val)
        if not validators.url(val):
            print("ÀÀÀÀ")
        print(val)
    else:
        if not validators.domain(val):
            print("BBBB")
        print(val)

