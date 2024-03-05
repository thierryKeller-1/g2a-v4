from toolkits.constants import PROJECT_FOLDER_PATH
from toolkits.file_manager import read_json_file, write_json_file


IP_STATUS_FILE = f"{PROJECT_FOLDER_PATH}/configs/ip_status.json"

def get_status(key:str=None) -> None:
    global IP_STATUS_FILE
    if key:
       return read_json_file(IP_STATUS_FILE, key)
    return read_json_file(IP_STATUS_FILE)

def set_status(key:str, value:object) -> None:
    global IP_STATUS_FILE
    current_status = read_json_file(IP_STATUS_FILE)
    try:
        current_status[key] = value
        write_json_file(IP_STATUS_FILE, current_status)
    except:
        print("\t Cannot change IP status")