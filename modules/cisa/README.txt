display_name="CISA Check CVE Person",
input_entity="maltego.Phrase",
description="Retrieves CVEs know to CISA.",
output_entities=["maltego.CVE"],

CISA_CVES_JSON_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

Example: "CVE-2022-27924"