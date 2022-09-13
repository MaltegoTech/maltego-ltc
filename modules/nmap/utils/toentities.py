import logging

from maltego_trx.entities import Phrase, DNS, IPAddress
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.overlays import OverlayType, OverlayPosition

log = logging.getLogger(__name__)


def dict_to_entities(cont: dict, response: MaltegoTransform, dns_name: str = ""):
    """

    Args:
        cont (dict): the output of the parsing function. The Entities will automatically be added by this function.
        response (MaltegoTransform):
        dns_name (str):
    Returns:
        None.
    """
    # General behavior:
    """
    Input -> Output
    
    Netblock -> IPs with info in property
    DNS name -> DNS name with info in property. Problem is that we only get the IP returned > overrid with a parameter
    IP -> IP with info in property
    
    """
    # remove stats and runtimes sections
    stats = cont.pop("stats")
    runtime = cont.pop("runtime")

    if len(cont.keys()) == 0:
        log.warning("Note: Host seems down!")

    for key, properties in cont.items():
        parse_properties(properties=properties, ip=key, response=response, dns_name=dns_name)


def parse_properties(properties: dict, ip: str, response: MaltegoTransform, dns_name: str):
    osmatch = properties.pop("osmatch")
    ports = properties.pop("ports")
    hostname = properties.pop("hostname")
    macaddress = properties.pop("macaddress")
    state = properties.pop("state")

    # to avoid outputting Entities with no info
    if osmatch == {} and ports == [] and hostname == [] and macaddress is None:
        if state == {}:
            return
        else:
            if state["state"] == "unknown" or state["state"] == "down":
                return

    if dns_name:
        ent = response.addEntity(DNS, dns_name)
        ent.addProperty("ipv4", "ipv4", "loose", ip)
    else:
        ent = response.addEntity(IPAddress, ip)

    # let's add an overlay to signal that the IP is up
    ent.addOverlay(propertyName='#00db3b', position=OverlayPosition.NORTH_WEST, overlayType=OverlayType.COLOUR)

    # ports
    for p in ports:
        name = f'{p["protocol"].lower()}/{p["portid"]}'
        if 'service' in p:
            service_name = ""
            if 'name' in p['service']:
                service_name = f"{p['service']['name']}"
            service_name += "\n"
            if 'product' in p['service']:
                service_name += f"product:{p['service']['product']}"
            service_name += "\n"
            if 'servicefp' in p['service']:
                service_name += f"service_footprint:{p['service']['servicefp']}"
        else:
            service_name = 'unknown\n\n'
        ent.addProperty(name, name, "loose", service_name)

    # hostname
    for i, h in enumerate(hostname):
        # in case there are several hostnames
        # ent.addProperty(f"hostname_{i}", f"hostname_{i}", "loose", f'{h["name"]} (Type: {h["type"]})')
        ent.addProperty(f"hostname_{i} ({h['type']})", f"hostname_{i} ({h['type']})", "loose", h["name"])

    # mac address
    if macaddress is not None:
        # ent.addProperty("mac_address", "mac_address", "loose", macaddress[0]['addr'])
        ent.addProperty("mac_address", "mac_address", "loose", macaddress['addr'])
        if "vendor" in macaddress:
            ent.addProperty("mac_address_vendor", "mac_address_vendor", "loose", macaddress['vendor'])

    # OS match
    if osmatch:
        # TODO add a Transform to extract the OS
        ent.addProperty("Operating_system", "Operating_system", "loose", osmatch[0]["name"])
        ent.addProperty("OS_accuracy", "OS_accuracy", "loose", osmatch[0]["accuracy"])
        # TODO add a Transform to extract the CPE
        ent.addProperty("CPE_OS", "CPE_OS", "loose", osmatch[0]["cpe"])
