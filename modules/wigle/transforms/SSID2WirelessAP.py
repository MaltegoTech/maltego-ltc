from extensions import registry
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
from pygle import network

@registry.register_transform(display_name="to Wireless AP [wigle]", input_entity="maltego.wirelessSSID",
                             description='Returns access points matching an specific SSID.',
                             output_entities=["maltego.wirelessAP"])
class SSID2WirelessAP(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        ssid_name = request.Value
        list = network.search(freenet="false",paynet="false",ssid=ssid_name)
        for ap in list['results']:
            res = response.addEntity("maltego.wirelessAP", ap['netid'])
            res.addProperty("ssid","SSID","strict",ap['ssid'])
            res.addProperty("channels", "Channels", "loose", ap['channel'])
            res.addProperty("encryption", "Encryption", "loose", ap['encryption'])
            res.addProperty("type", "Type", "loose", ap['type'])
            res.addProperty("country", "Country", "loose", ap['country'])
            res.addProperty("latitude","Latitude","loose", ap['trilat'])
            res.addProperty("longitude","Longitude","loose", ap['trilong'])
            res.addProperty("city","City","loose", ap['city'])
            res.addProperty("street","Street","loose", ap['road'])
            res.addProperty("postalcode","Postal Code","loose", ap['postalcode'])
            res.addProperty("region","Region","loose", ap['region'])
            res.addProperty("firsttime","First time","loose", ap['firsttime'])
            res.addProperty("lasttime", "Last time", "loose", ap['lasttime'])

            # extract results
            #for ap in search['results']:
            #    net = ap['netid']
            #    response.addEntity("maltego.wirelessAP",net)
        # network.geocode(addresscode="London")
        # url = 'https://api.wigle.net/api/v2/file/upload'
        #wirelessAP = response.addEntity("maltego.wirelessAP", "9A:9B:CB:72:23:16")
        #wirelessAP.addProperty("ssid","SSID","strict",ssid_name)
        #wirelessAP.addProperty("latitude","Latitude","loose","38.951633")
        #wirelessAP.addProperty("longitude","Longitude","loose","-77.14462")
        #wirelessAP.setLinkLabel("Found in DD-MM-YYY")