import re
import subprocess
import time
import requests

from requests.auth import HTTPBasicAuth


class URLPath:
    CHAMP_SELECT_SESSION = "/lol-champ-select/v1/session"
    LOBBY = "/lol-lobby/v2/lobby"
    POSITION = "/lol-lobby/v2/lobby/members/localMember/position-preferences"


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

    def change_position(self, first_position=None, second_position=None):
        available_position = ["TOP", "MIDDLE", "JUNGLE", "BOTTOM", "UTILITY", "FILL"]
        lobby_url = self.base_url + URLPath.LOBBY
        res = self.sess.get(lobby_url)
        my_lobby_info = res.json()["localMember"]
        prev_first_position = my_lobby_info["firstPositionPreference"]
        prev_second_position = my_lobby_info["secondPositionPreference"]
        position_url = self.base_url + URLPath.POSITION
        lobby_data = {
            "firstPreference": first_position
            if first_position in available_position
            else prev_first_position,
            "secondPreference": second_position
            if second_position in available_position
            else prev_second_position,
        }
        self.sess.put(position_url, json=lobby_data)

    def ban_pick_champion(self, champion_id, type="BAN"):
        url = self.base_url + URLPath.CHAMP_SELECT_SESSION
        self.sess.get(url)
