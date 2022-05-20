from extensions import registry
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_PARTIAL, UIM_FATAL
from maltego_trx.transform import DiscoverableTransform
from scripts.helpers import check_cve


@registry.register_transform(display_name="Greet Person", input_entity="maltego.Phrase",
                             description='Returns a Phrase greeting a Person on the Graph.',
                             output_entities=["maltego.Phrase"])
class CisaCheckCVE(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        cve_id = request.Value
        results = check_cve(cve_id)

        if results:
            if "Server Error" not in results:
                exploit = response.addEntity("my.Exploit", results['vulnerabilityName'])
                exploit.addProperty(fieldName="cveID", displayName="CVE ID", matchingRule="loose", value=results['cveID'])
                exploit.addProperty(fieldName="vendorProject", displayName="Vendor", matchingRule="loose", value=results['vendorProject'])
                exploit.addProperty(fieldName="product", displayName="Property", matchingRule="loose", value=results['product'])
                exploit.addProperty(fieldName="dateAdded", displayName="Date Added", matchingRule="loose", value=results['dateAdded'])
                exploit.addProperty(fieldName="shortDescription", displayName="Description", matchingRule="loose", value=results['shortDescription'])
                exploit.addProperty(fieldName="requiredAction", displayName="Action", matchingRule="loose", value=results['requiredAction'])
                exploit.addProperty(fieldName="dueDate", displayName="Due Date", matchingRule="loose", value=results['dueDate'])
            else:
                response.addUIMessage(message=results, messageType=UIM_FATAL)
        else:
            response.addUIMessage(message="CVE Not Found", messageType=UIM_PARTIAL)