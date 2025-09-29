import sys
import os
import time
import base64
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

file_path = "none"
command = "none"
commands = ["-enc", "-dec"]

colors = {
    "reset": "\033[0m",
    "rouge": "\033[31m",
    "bleu": "\033[34m"
}

# Closing
def close():
    print("\nFermeture du script dans 3 secondes")
    time.sleep(3)

# Configuration des couleurs du thème.
def dark_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    bg = "#2b2b2b"
    fg = "#ffffff"
    accent = "#3c3f41"

    root.configure(bg=bg)

    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TButton", background=accent, foreground=fg, padding=6)
    style.map("TButton",
              background=[("active", "#505354")],
              foreground=[("disabled", "#888888")])

    style.configure("TEntry", fieldbackground=accent, foreground=fg)

# Conversion Key -> Fernet Key
def password_to_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Encrypté un fichier
def encrypt_file(pwd):
    salt = os.urandom(16)
    print(f"{colors['bleu']}[INFO] Sel généré.{colors['reset']}")
    key = password_to_key(pwd, salt)
    print(f"{colors['bleu']}[INFO] Clé de cryptage générée.{colors['reset']}")
    fernet = Fernet(key)
    extension = os.path.splitext(file_path)[1]

    print(f"{colors['bleu']}[INFO] Lecture du fichier en cours...{colors['reset']}")
    with open(file_path, "rb") as f:
        data = f.read()
    
    print(f"{colors['bleu']}[INFO] Cryptage du fichier en cours...{colors['reset']}")
    encrypted = fernet.encrypt(data)

    print(f"{colors['bleu']}[INFO] Sauvegarde du fichier en cours...{colors['reset']}")
    with open(file_path.replace(extension, ".enc", 1), "wb") as f:
        f.write(extension.encode("utf-8").ljust(5, b"\x00") + salt + encrypted)
    print(f"{colors['bleu']}[INFO] Fichier sauvegardé.{colors['reset']}")
    close()

# Décrypté un fichier
def decrypt_file(pwd):
    try:
        print(f"{colors['bleu']}[INFO] Lecture du fichier.{colors['reset']}")
        with open(file_path, "rb") as f:
            data = f.read()

        extension = data[:5].decode("utf-8", errors="ignore").strip("\x00")
        print(f"{colors['bleu']}[INFO] Extension d'origine récupéré.{colors['reset']}")
        salt = data[5:21]
        print(f"{colors['bleu']}[INFO] Sel récupéré.{colors['reset']}")
        encrypted = data[21:]
        print(f"{colors['bleu']}[INFO] Fichier crypté récupéré.{colors['reset']}")
        key = password_to_key(pwd, salt)
        print(f"{colors['bleu']}[INFO] Clé de décryptage générée.{colors['reset']}")
        fernet = Fernet(key)

        print(f"{colors['bleu']}[INFO] Décryptage en cours...{colors['reset']}")
        decrypted = fernet.decrypt(encrypted)
        
        print(f"{colors['bleu']}[INFO] Sauvegarde du fichier en cours...{colors['reset']}")
        original_name = file_path.replace(".enc", extension)
        with open(original_name + "", "wb") as f:
            f.write(decrypted)
        print(f"{colors['bleu']}[INFO] Fichier sauvegardé.{colors['reset']}")
        close()
    except:
        print(f"{colors['rouge']}[ERROR] Clé incorrect.{colors['reset']}")
        close()

def confirm():
    pwd = entry.get()
    root.destroy()
    if command == "-enc":
        encrypt_file(pwd)
    elif command == "-dec":
        decrypt_file(pwd)
    else:
        print(f"{colors['rouge']}[ERROR] Impossible de confirmer.{colors['reset']}")
        close()

# Main
def main():
    global entry
    global root

    root = tk.Tk()
    pos_x = root.winfo_pointerx()
    pos_y = root.winfo_pointery()
    root.title("Encinc - Encryptor / Decryptor")
    root.geometry(f"400x50+{pos_x - 150}+{pos_y - 25}")
    
    dark_theme(root)

    # Widgets
    row = tk.Frame(root)
    row.pack(fill="x", padx=10, pady=(10, 5))

    label = tk.Label(row, text="Secret Key:")
    label.pack(side="left")

    entry = tk.Entry(row, show="*", width=30)
    entry.pack(side="left", padx=(8, 0), fill="x", expand=True)

    button = tk.Button(row, text="Confirm", command=confirm)
    button.pack(side="left")

    # Mainloop
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        command = sys.argv[1]
        file_path = sys.argv[2]
        if isinstance(file_path, str) and command in commands:
            main()
        else:
            print(f"{colors['rouge']}[ERROR] Commande inconnue ou fichier introuvable.{colors['reset']}")
            close()
    else:
        print(f"{colors['rouge']}[ERROR] Nombre d'argument insuffisant ou trop élevé.{colors['reset']}")
        close()
else:
    print(f"{colors['rouge']}[ERROR] Impossible d'importé ce script en tant que module.{colors['reset']}")
    close()