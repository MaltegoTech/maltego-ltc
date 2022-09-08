import os
import nmap3

# If the NMAP executable is not automatically found, you can override it here.
NMAP_EXECUTABLE = ""

if not NMAP_EXECUTABLE:
    NMAP_EXECUTABLE = "nmap"

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
CACHE_SHELF_LIFE = 60*60*24


# The number of ports scanned when performing a top port scan (see "--top-ports" documentation here:
# https://nmap.org/book/port-scanning-options.html)
TOP_PORT_SCAN_NUMBER = 100

# TODO add a Transform that uses a parameter here, to allow you to scan a specific set of ports

if __name__ == '__main__':
    print(CACHE_DIR)