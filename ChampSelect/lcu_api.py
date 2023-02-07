import re
import subprocess


class LCU_API:
    WMIC_QUERY = "wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline"
    PORT_PREFIX = "--app-port="
    AUTH_PREFIX = "--remoting-auth-token="

    def __init__(self):
        wmic_result = subprocess.getoutput(self.WMIC_QUERY)
        port_index_start, port_index_end = re.search(
            f"{self.PORT_PREFIX}([0-9]*)", wmic_result
        ).span()
        auth_index_start, auth_index_end = re.search(
            f"{self.AUTH_PREFIX}([\w-]*)", wmic_result
        ).span()

        self._port = wmic_result[
            port_index_start + len(self.PORT_PREFIX) : port_index_end
        ]
        self._auth = wmic_result[
            auth_index_start + len(self.AUTH_PREFIX) : auth_index_end
        ]

    def print_connection_info(self):
        print(self._auth)
        print(self._port)
