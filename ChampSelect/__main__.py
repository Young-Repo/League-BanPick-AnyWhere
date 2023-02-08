from ChampSelect.lcu_api import LCU_API


lcu = LCU_API()
lcu.print_connection_info()
lcu.make_lobby(420)
lcu.change_position("TOP", "JUNGLE")
