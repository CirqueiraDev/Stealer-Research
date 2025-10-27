from contextlib import suppress
import requests, platform, socket, getpass, psutil, zipfile
from datetime import datetime

def GetSystemInfos(zip_file):
    infos = False
    space = ' '

    def info():
        ip_info = ''
        with suppress(Exception):
            s = requests.get("https://ipwhois.app/json/").json()
            for i in s:
                len_i = len(i)
                pad = 20-len_i
                ip_info += f"    - {i}{space*pad}: {s[i]}\n"
            return ip_info
        return 'No IP infos.'

    IPinfos = info()

    cpu_count = psutil.cpu_count(logical=True)
    ram_total = round(psutil.virtual_memory().total / (1024**3), 2)
    disk_usage = psutil.disk_usage('/').percent

    net_info = ''
    with suppress(Exception):
        interfaces = psutil.net_if_addrs()
        max_len = max(len(i) for i in interfaces)

        for iface, addr_list in interfaces.items():
            for addr in addr_list:
                if addr.family == socket.AF_INET:
                    pad = max_len - len(iface)
                    net_info += f"    - {iface}{space * pad} : {addr.address}\n"

    system_infos = f"""
System info:
    - hostname      : {socket.gethostname()}
    - username      : {getpass.getuser()}
    - processor     : {platform.processor()}
    - machine       : {platform.machine()}
    - platform      : {platform.platform()}
    - system        : {platform.system()}
    - release       : {platform.release()}
    - version       : {platform.version()}
    - CPU cores     : {cpu_count}
    - RAM total(GB) : {ram_total}
    - Disk usage(%) : {disk_usage}
    - local IP      : {socket.gethostbyname(socket.gethostname())}

Network interfaces:
{net_info}
Public IP info:
{IPinfos}
"""
    
    zip_file.writestr(f"system_infos.txt", system_infos)
    return infos

with zipfile.ZipFile("systeminfoss.zip", "w") as zf:
    GetSystemInfos(zf)