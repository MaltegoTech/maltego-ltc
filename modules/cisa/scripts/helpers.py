# This file contains the logic for the CISA Transforms

import requests
from scripts.constants import JSON_FEED


def check_cve(input_cve):

    data = requests.get(JSON_FEED)

    if data.status_code == 200:
        parsed = data.json()

        for vulnerability in parsed['vulnerabilities']:
            if vulnerability['cveID'] == input_cve:
                return vulnerability
            else:
                pass
    else:
        return "Server Error {}".format(data.status_code)
