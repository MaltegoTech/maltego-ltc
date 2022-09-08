import os
import shlex
import base64
import logging
import datetime
import subprocess
from xml.etree import ElementTree as ET

from modules.nmap.config import CACHE_DIR, CACHE_SHELF_LIFE, NMAP_EXECUTABLE, SUDO

log = logging.getLogger(__name__)


class NmapOrchestrator:
    @classmethod
    def _run_command(cls, cmd, timeout=None):
        """

        Args:
            cmd (str): the command to be run
            timeout (int): number of seconds for timeout

        Returns: the raw XML from NMAP (bytes)

        """
        args = shlex.split(cmd)
        sub_proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, errs = sub_proc.communicate(timeout=timeout)
        except Exception as e:
            sub_proc.kill()
            # See: https://github.com/nmap/nmap/issues/1764
            if "Assertion `htn.toclock_running == true' failed." in e:
                log.critical("Command failed. PLEASE RERUN")
            raise (e)
        else:
            if 0 != sub_proc.returncode:
                raise Exception('Error during command: "' + ' '.join(args) + '"\n\n' + errs.decode('utf8'))

            NmapOrchestrator._cache_output(cmd, output)
            # remember the output is bytes
            return output

    @classmethod
    def _parse_xml(cls, parsing_function, output):
        """
        Parses the XML output of nmap.
        Args:
            # parsing_function (str): we're using the parsing function from nmap3, a method name from
            # nmap3.nmapparser.NmapCommandParser should be supplied.
            parsing_function (Callable[[bytes], Dict]): a parsing function taking in raw binary XML and outputting a dict should be
            supplied.
            output (bytes): the raw XML output of the NMAP command

        Returns:
            dict
        """
        output = output.decode('utf8').strip()
        try:
            output = ET.fromstring(output)
        except Exception as e:
            raise Exception(f"Couldn't parse XML output from NMAP: {e}")

        res = parsing_function(output)
        return res

    @classmethod
    def _cache_output(cls, cmd, output):
        """

        Args:
            cmd (str):
            output (bytes):

        Returns:

        """
        filepath = cls._get_cached_file_path(cmd)
        log.info(f"Caching results from '{cmd}' at {filepath}")
        if os.path.exists(filepath):
            log.info(f"Overwriting file at {filepath}")
        with open(filepath, "wb") as f:
            f.write(output)

    @classmethod
    def _get_cached_file_path(cls, cmd):
        # we remove the
        cmd = cmd[1:-2]
        # no need to include the creation date, we can get that from the OS
        filename = base64.b64encode(cmd.encode('ascii')).decode("ascii") + ".xml"
        return os.path.join(CACHE_DIR, filename)

    @classmethod
    def execute_command(cls, cmd, parsing_function):
        """

        Args:
            cmd (str): the command that will be run, without the nmap. If the command you want to run
            is "nmap localhost -sV", the cmd arg should be: "localhost -sV"
            parsing_function (Callable[[bytes], Dict]):

        Returns:

        """
        # TODO handle exception that could arise
        # TODO handle exception for lack of ROOT
        cmd = SUDO + NMAP_EXECUTABLE + " " + cmd + " -oX -"
        fp = cls._get_cached_file_path(cmd)

        cont = b""
        if os.path.exists(fp):
            log.info(f"Cache file for '{cmd}' exists!")
            # Note: os.path.getctime only gives us the creation times on Windows, on Linux and others, we will most
            # likely get the last modification time. But that works as well, since we simply open the file, we don't
            # modify it.
            mod_time = os.path.getctime(fp)
            if datetime.datetime.now().timestamp() - mod_time < CACHE_SHELF_LIFE:
                log.info(f"Dating from "
                         f"{str(datetime.datetime.fromtimestamp(mod_time)).split('.')[0]}. "
                         f"Using it instead of running another scan.")
                with open(fp, "rb") as f:
                    cont = f.read()
            else:
                log.info(f"Cache file for '{cmd}' is expired. Deleting {fp} and running the scan.")
                try:
                    os.remove(fp)
                except Exception as e:
                    log.error(f"Error when removing {fp}: {e}")
        else:
            log.info(f"Cache file for '{cmd}' does not exists. Running the scan.")
        if not cont:
            cont = cls._run_command(cmd)
        return cls._parse_xml(parsing_function=parsing_function, output=cont)


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # NmapOrchestrator._cache_output("dazdazdazda8888z", b"dadaadaz")
    from modules.nmap.utils.commands import COMMANDS

    # CMD = "{target} --top-ports {top_ports_scan_number}"
    # command = CMD.format(target="scanme.nmap.Org", top_ports_scan_number="100")
    # command = "{target} --top-ports {top_ports_scan_number}".format(target="192.168.1.0/24",
    #                                                                 top_ports_scan_number="100")
    # parsing_func = COMMANDS[CMD]

    # CMD = "{target} -sL"
    # command = CMD.format(target="192.168.1.38")
    # command = CMD.format(target="192.168.1.1/24")
    # parsing_func = COMMANDS[CMD]

    # CMD = "{target} -O"
    # command = CMD.format(target="192.168.1.39")
    # parsing_func = COMMANDS[CMD]

    # CMD = "{target} -p-"
    # command = CMD.format(target="192.168.1.0/24")
    # parsing_func = COMMANDS[CMD]
    #
    # CMD = "{target} -sV"
    # command = CMD.format(target="scanme.nmap.org")
    # parsing_func = COMMANDS[CMD]
    #
    # CMD = "{target} -sF"
    # command = CMD.format(target="scanme.nmap.Org")
    # parsing_func = COMMANDS[CMD]
    #
    # CMD = "{target} -sP"
    # command = CMD.format(target="192.168.1.0/24")
    # parsing_func = COMMANDS[CMD]
    #
    # CMD = "{target} -sS"
    # command = CMD.format(target="192.168.1.38")
    # parsing_func = COMMANDS[CMD]
    #
    # CMD = "{target} -sU"
    # command = CMD.format(target="192.168.1.38")
    # parsing_func = COMMANDS[CMD]

    # CMD = "{target} -sU"
    # command = CMD.format(target="192.168.1.38")
    # parsing_func = COMMANDS[CMD]

    CMD = "{target} -p-"
    command = CMD.format(target="192.168.1.0/24")
    parsing_func = COMMANDS[CMD]

    ee = NmapOrchestrator.execute_command(cmd=command, parsing_function=parsing_func)

    import json

    print(json.dumps(ee, indent=4))

    from modules.nmap.utils.toentities import parse_properties

    for key, properties in ee.items():
        # parse_properties(properties=properties, ip=key, response="response", dns_name=dns_name)
        parse_properties(properties=properties, ip=key, response="response", dns_name="")
