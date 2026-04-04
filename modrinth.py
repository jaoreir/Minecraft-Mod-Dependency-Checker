import requests
from rich import print as rprint

import utils

URL = "https://api.modrinth.com/v2/project/"


def fetch_mod_info(info_dict, mod_id):
    if not mod_id:
        utils.logerr("No mod id!")
        return

    print(f"Fetching info for {mod_id}...")
    r = requests.get(URL + mod_id)
    if r.status_code != 200:
        utils.logerr(f'HTTP {r.status_code} when fetching info for mod "{mod_id}"!')
        return
    print("OK")
    j = r.json()
    info_dict[mod_id] = j


def fetch_mod_list_info(mod_list):
    info_dict = {}
    for mod_id in mod_list:
        fetch_mod_info(info_dict, mod_id)
    rprint(info_dict)
