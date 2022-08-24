import sys
import json
import os.path
import subprocess
import urllib
from pprint import pprint
from typing import TypedDict, Optional, List, Union
from urllib.parse import ParseResult

from parser import ParserError

from ..config import BASE_DIR, read_config_file


class CMSeekResult(TypedDict, total=False):
    cms_id: str
    cms_name: str
    cms_url: str
    detection_param: str
    last_scanned: str
    url: str


class WordPressCMSeekResult(CMSeekResult):
    wp_vuln_count: int
    wp_changelog_file: str
    wp_version: str
    wp_users: List[str]
    wpvulndb_url: str
    wp_plugins: List[str]
    wp_uploads_directory: str


def split_csv_string(csv_string: str) -> List[str]:
    items = csv_string.split(",")
    items.remove("")
    return items


class CMSeekService:
    @staticmethod
    def run(url: str) -> Optional[Union[CMSeekResult, WordPressCMSeekResult]]:
        # to handle all forms or urls, let's parse it
        parsed_url = urllib.parse.urlparse(url)

        # if the hostname is "", it couldn't be parsed
        if parsed_url.hostname == "":
            raise ParserError(f"Could not parse url '{url}'")

        # CMSeeK command for a single url
        cmd = f"{sys.executable} cmseek.py --follow-redirect --batch -u {parsed_url.hostname}"

        # Execute the command in a shell, wait for it to finish
        CMSEEK_DIR = read_config_file("CMSeeK", "InstallPath")
        subprocess.Popen(cmd.split(" "),
            stdout = subprocess.PIPE, stderr = subprocess.PIPE,
            cwd = CMSEEK_DIR).communicate()

        # this is where the cms.json for a give host would be written
        result_json_path = os.path.join(CMSEEK_DIR, "Result", parsed_url.hostname, "cms.json")

        # we'll load it into a dict and return it
        if os.path.isfile(result_json_path):
            with open(result_json_path) as cms_json:
                result = json.load(cms_json)

                # if it's WordPress, we can parse the csv lists as python lists
                if result['cms_id'] == "wp":
                    result['wp_users'] = split_csv_string(result.get('wp_users', ''))
                    result['wp_plugins'] = split_csv_string(result.get('wp_plugins', ''))

                return result


if __name__ == '__main__':
    cmseek_result = CMSeekService.run("https://hotelhelga.com/")
    pprint(cmseek_result)
