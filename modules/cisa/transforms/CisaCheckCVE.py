from typing import TypedDict

import requests
from cachetools import cached, TTLCache
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform, UIM_INFORM
from maltego_trx.transform import DiscoverableTransform

from modules.cisa.extensions import cisa_registry
from modules.cisa.extensions import cisa_set

CISA_CVES_JSON_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


class CisaCve(TypedDict):
    cveID: str
    vendorProject: str
    product: str
    vulnerabilityName: str
    dateAdded: str
    shortDescription: str
    requiredAction: str
    dueDate: str
    notes: str


@cached(cache=TTLCache(maxsize=1, ttl=3600))
def get_cisa_cves() -> dict[str, CisaCve]:
    data = requests.get(CISA_CVES_JSON_URL)

    if data.status_code != 200:
        return {}

    json_data = data.json()

    return {cve["cveID"]: cve for cve in json_data["vulnerabilities"]}


@cisa_registry.register_transform(
    display_name="CISA Check CVE Person",
    input_entity="maltego.Phrase",
    description="Retrieves CVEs know to CISA.",
    output_entities=["maltego.CVE"],
    transform_set=cisa_set,
)
class CisaCheckCVE(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        cve_id = request.Value

        cve: CisaCve = get_cisa_cves().get(cve_id)

        if not cve:
            response.addUIMessage(f"CVE {cve_id} not found", UIM_INFORM)
            return

        exploit = response.addEntity("maltego.CVE", cve['vulnerabilityName'])

        properties = (
            ("text", "CVE", "loose", cve["cveID"]),
            ("vendorProject", "Vendor", "loose", cve["vendorProject"]),
            ("product", "Property", "loose", cve["product"]),
            ("dateAdded", "Date Added", "loose", cve["dateAdded"]),
            ("shortDescription", "Description", "loose", cve["shortDescription"]),
            ("requiredAction", "Action", "loose", cve["requiredAction"]),
            ("dueDate", "Due Date", "loose", cve["dueDate"]),
        )

        for prop in properties:
            exploit.addProperty(
                fieldName=prop[0],
                displayName=prop[1],
                matchingRule=prop[2],
                value=prop[3],
            )

        notes = cve.get("notes")
        if notes:
            exploit.addDisplayInformation(notes, "Notes")
