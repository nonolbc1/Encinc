# Encinc

Encinc est un outil de chiffrement et déchiffrement de fichiers pour Windows.  
Deux versions sont installé :

- **Encinc.exe** : version sans console (utilisation via clic droit / menu contextuel Windows).  
- **Encinc_console.exe** : version avec console (utilisation via terminal).  

---

## 🔐 Chiffrement

### ➤ Avec Encinc.exe (sans console)
1. Faites **clic droit** sur le fichier à chiffrer.  
2. Sélectionnez **Encrypt**.
3. Marquez une **clé de chiffrement**.
3. Le fichier chiffré sera créé avec l’extension `.enc`.  

---

### ➤ Avec Encinc_console.exe (console)
Ouvrez un terminal (CMD ou PowerShell) et tapez :

```bash
Encinc_console -enc monfichier.txt
```

👉 Résultat : un fichier `monfichier.enc` sera généré.

---

## 🔐 Déchiffrement

### ➤ Avec Encinc.exe (sans console)
1. Faites **clic droit** sur un fichier .enc
2. Sélectionnez **Decrypt**.
3. Marquez la même **clé de chiffrement** anciennement utiliser.
3. Le fichier original sera restauré.  

---

### ➤ Avec Encinc_console.exe (console)
Ouvrez un terminal (CMD ou PowerShell) et tapez :

```bash
Encinc_console -dec monfichier.enc
```

👉 Résultat : le fichier `monfichier.txt` sera restauré.

---

## 📌 Remarque

- Encinc est conçu pour être simple : soit via **clic droit**, soit via **ligne de commande**.
- Les deux versions sont installées, mais une seule est recommandée selon votre usage.