<div align="center">
  <h1>Stealer-Research</h1>
  <p>These tools collect sensitive data and can be abused. Use this repository ONLY for legitimate security research, authorized auditing, or educational study. Do NOT use for activities that violate privacy or the law.</p>
</div>

<br>

## Legal Notice ‼
> The **creator is not responsible** for any misuse of this repository; **all responsibilities** and **damages** caused by creating and distributing malware are entirely the **user's responsibility.**

---

## Stealer Functions

### `roblox_cookies.py`
Searches for Roblox session cookies (`.ROBLOSECURITY`) across multiple browsers, tries them against the Roblox API to retrieve account data, and writes found accounts into a file inside a ZIP.

### `browser_steal.py`
Scans browser profiles to extract extensions, saved passwords, cookies, history, downloads and card data; decrypts when needed and writes those items to files inside a ZIP.

### `discord_token.py`
Searches for Discord tokens in local browser/client files and databases, validates those tokens with the Discord API, collects account details (username, id, billing, Nitro, etc.), and records them to a file.

### `interesting_files.py`
Searches user folders (Desktop, Downloads, Documents, Recent, etc.) for files with keyword names related to accounts, wallets, keys, backups, and copies those files into an **“Interesting Files”** folder inside the ZIP.

### `Anti_VM_Debug.py`
Runs anti-analysis checks: detects active debuggers, reverse-engineering processes, usernames/hosts/HWIDs associated with virtual machines or analysis environments, and returns `true` if signs of VM/debugging are found.
