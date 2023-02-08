import re
import subprocess
import time
import requests

from requests.auth import HTTPBasicAuth


class URLPath:
    CHAMP_SELECT_SESSION = "/lol-champ-select/v1/session"
    LOBBY = "/lol-lobby/v2/lobby"


class LCU_API:
    WMIC_QUERY = "wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline"
    PORT_PREFIX = "--app-port="
    AUTH_PREFIX = "--remoting-auth-token="

    def __init__(self):
        wmic_result = subprocess.getoutput(self.WMIC_QUERY)
        self._port = re.findall(f"{self.PORT_PREFIX}([0-9]*)", wmic_result)[0]
        self._auth = re.findall(f"{self.AUTH_PREFIX}([\w-]*)", wmic_result)[0]
        self.base_url = f"https://127.0.0.1:{self._port}"
        self.sess = requests.Session()
        self.sess.auth = HTTPBasicAuth("riot", self._auth)
        self.sess.verify = False

    def print_connection_info(self):
        print(self._auth)
        print(self._port)

    def make_lobby(self, queue_id=420):
        """
        TODO: fill queue id
        420 : SOLO_RANK
        XXX : NORMAL_RIFT
        XXX : ARAM
        """
        url = self.base_url + URLPath.LOBBY
        lobby_data = {
            "queueId": queue_id,
        }
        self.sess.post(url, json=lobby_data)

    def ban_pick_champion(self, champion_id, type="BAN"):
        url = self.base_url + URLPath.CHAMP_SELECT_SESSION
        self.sess.get(url)
