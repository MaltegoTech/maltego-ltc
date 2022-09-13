from nmap3.nmapparser import NmapCommandParser

COMMANDS = {
    # target can be subnet or DNS name or IP | Done
    "{target} --top-ports {top_ports_scan_number}": NmapCommandParser(None).filter_top_ports,
    # target should be a subnet | List scan | Done
    "{target} -sL": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name or IP | OS detection | Done
    "{target} -O": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | All ports scan | Done
    "{target} -p-": NmapCommandParser(None).filter_top_ports,
    # target should be DNS name or IP | Probe open ports to determine service | Done
    "{target} -sV": NmapCommandParser(None).filter_top_ports,
    # target should be an IP or DNS name | FIN scan (sending FIN TCP packet) | Done
    "{target} -sF": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | Ping scan | Done
    "{target} -sP": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | Syn scan | Done
    "{target} -sS": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | UDP scan | Done
    "{target} -sU": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | ARP discovery | Done
    "{target} -PR": NmapCommandParser(None).filter_top_ports,
}

if __name__ == '__main__':
    print(NmapCommandParser.__dict__)
