import requests

def getIOC(URL):
    api_url = "https://api.iocparser.com/url"
    payload = {"url": URL}
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", api_url, headers=headers, json=payload)
    iocs = response.json()
    return iocs