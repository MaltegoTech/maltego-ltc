from maltego_trx.entities import Domain, WebTitle
from maltego_trx.transform import DiscoverableTransform
from maltego_trx.maltego import MaltegoTransform, MaltegoMsg
from extensions import registry
import dnstwist
import json

from modules.dnstwist.extensions import dnstwist_registry, dnstwist_set


def dns_twister(domain):
    data = dnstwist.run(domain=domain, registered=True, format='null')
    parsed_list = json.dumps(data, indent=4, sort_keys=True)
    parsed_json = json.loads(parsed_list)

    return parsed_json


@dnstwist_registry.register_transform(display_name="To Domains [DNSTwist]", input_entity="maltego.Domain",
                                      description='Searches for Cybersquatting Domains',
                                      output_entities=["maltego.WebTitle"],
                                      transform_set=dnstwist_set)
class ToRegisteredDomains(DiscoverableTransform):
    """
    Adds a note with the translation
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):

        orig_string = request.Value
        results = dns_twister(orig_string)

        for domain in results:
            if domain['domain']:

                if domain['fuzzer'] != "*original":

                    ent = response.addEntity("maltego.Domain", domain['domain'])
                    try:
                        ent.addProperty("dns_a", "IPv4", "strict", domain['dns_a'][0])
                    except KeyError:
                        pass
                    ent.addProperty("fuzzer", "Fuzzer Type", "loose", domain['fuzzer'])
