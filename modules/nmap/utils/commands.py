from nmap3.nmapparser import NmapCommandParser

COMMANDS = {
    # target can be subnet or DNS name or IP
    "{target} --top-ports {top_ports_scan_number}": NmapCommandParser(None).filter_top_ports,
    # target should be a subnet | List scan
    "{target} -sL": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name or IP | OS detection
    "{target} -O": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | All ports scan
    "{target} -p-": NmapCommandParser(None).filter_top_ports,
    # target should be DNS name or IP
    "{target} -sV": NmapCommandParser(None).filter_top_ports,
    # target should be an IP or DNS name | FIN scan (sending FIN TCP packet)
    "{target} -sF": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | Ping scan
    "{target} -sP": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | Syn scan
    "{target} -sS": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | UDP scan
    "{target} -sU": NmapCommandParser(None).filter_top_ports,
    # target should be a DNS name, IP or subnet | ARP discovery
    "{target} -PR": NmapCommandParser(None).filter_top_ports,
}

if __name__ == '__main__':
    print(NmapCommandParser.__dict__)
