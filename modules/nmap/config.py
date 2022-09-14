import os
import nmap3

# If the NMAP executable is not automatically found, you can override it here.
NMAP_EXECUTABLE = ""

# checking if we can run sudo commands
if os.getuid() == 0:
    SUDO = "sudo "
else:
    SUDO = ""

# The directory where the output of NMAP command will be cached
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache/")

# The maximum time we want to rely on a cached scan. If the XML file is older than this period of time, the XML will
# be deleted and the scan will be performed again, else we will simply reuse the results of the scan and not rerun the
# nmap scan. The format should be a number of seconds.
CACHE_SHELF_LIFE = 60 * 60 * 24

# The number of ports scanned when performing a top port scan (see "--top-ports" documentation here:
# https://nmap.org/book/port-scanning-options.html)
TOP_PORT_SCAN_NUMBER = 100

# You can specify a set of port to be scanned when running the "Scan set of ports (-p -A)" Transform
# You can represent them by listing them or using a hyphen to designate a range
# Documentation here: https://nmap.org/book/man-port-specification.html
SET_OF_PORTS_TO_SCAN = {
    "udp": "630-635",
    "tcp": "3306, 22",
    "sctp": "",
    "ip_protocol": "",
}

CONFIG_FILE_PATH = __file__

if __name__ == '__main__':
    print(CACHE_DIR)
