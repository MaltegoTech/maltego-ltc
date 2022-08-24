import requests

def getIOC(URL):
    api_url = "https://api.iocparser.com/url"
    payload = {"url": URL}
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", api_url, headers=headers, json=payload)
    if response.status_code == 204:  # Response no content
        return
    else:
        iocs = response.json()
        return iocs