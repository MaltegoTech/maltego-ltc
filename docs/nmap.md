# NMAP for Maltego

Harness the power of Nmap from Maltego! This integration uses the python3-nmap package to interact with Nmap.

## How to prepare your computer to use this integration
1. Install nmap. You can download it here: https://nmap.org/. Make sure that writing "nmap" in your terminal calls the nmap software. 
2. Install the required packages: pip install -r maltego-ltc/modules/nmap/requirements.txt

## Starting Maltego with administrator privilege
To fully enjoy nmap's capabilities, you will need to run nmap as an administrator. The problem is, Maltego will execute this integration which will execute nmap. All of this means: **you have to execute Maltego as root to fully enjoy this integration.**

## Config
A config file is available at maltego-ltc/modules/nmap/config.py

You can use it to:
- Override the path to the nmap executable (default is just calling "nmap")
- Change the cache folder. This integration caches nmap's output in a folder. Default is maltego-ltc/modules/nmap/cache/ but you can modify it if needed.
- Change the number of seconds a cached file is valid. When you run a scan through this integration, nmap's output is cached and will be reused until it expires (instead of running the scan again). You can choose the number of seconds it takes for a cached file to expire.
- When running a top ports scan, nmap will scan the n most popular ports. You can change n in the config file.
- When running "Scan set of ports (-p -A)" nmap will scan a specific set of ports. You can modify this set of ports according to your needs.
