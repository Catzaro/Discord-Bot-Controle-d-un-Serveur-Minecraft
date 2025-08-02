# 🤖 Bot Discord – Contrôle de serveur Minecraft

Ce bot Discord permet de démarrer, arrêter et redémarrer un **serveur Minecraft local** via des réactions emoji ou des commandes texte. Il utilise RCON pour interagir avec le serveur.
La partie création de server minecraft n'est pas comprise dans les explication. Personnellement j'ai créé ce bot pour avoir une alternative a aternos ou autres hébergeur. Je recommande d'avoir une bonne config
IL FAUT METTRE LES FICHIERS DANS LE DOSSIER DU SERVER MINECRAFT

---

## 🚀 Fonctionnalités

- ✅ Démarrer / arrêter / redémarrer le serveur via réactions
- 📢 Envoyer un message dans le chat Minecraft (`!msg`)
- 👥 Afficher les joueurs connectés (`!players`)
- 🔁 Statut automatique (en ligne / hors ligne) dans le statut Discord
- 🔒 Configuration via fichier `.env`

---

## 🧩 Prérequis

- Python 3.8+
- Un serveur Minecraft avec **RCON activé** (`enable-rcon=true` dans `server.properties`)
- Un script `.bat` pour démarrer le serveur localement
- Un bot Discord avec son token (rendez-vous sur : https://discord.com/developers/applications)

---
## 🤖 Création du Bot Discord

1. Créer l'application

Va sur discord.com/developers/applications
Clique sur "New Application", donne-lui un nom, puis clique sur "Create"

2. Activer les intents nécessaires

Dans l'onglet "Bot", active :
✅ SERVER MEMBERS INTENT
✅ MESSAGE CONTENT INTENT

⚠️ Ces options sont nécessaires pour que le bot lise les messages et interagisse avec les membres.

3. Copier le token du bot

Clique sur "Reset Token" si besoin
Clique sur "Copy" pour récupérer le token
Colle-le dans le fichier .env à la racine de ton projet : DISCORD_TOKEN=ton_token_ici

## 📩 Inviter le bot sur ton serveur
1. Générer le lien d'invitation
Va dans "OAuth2" > "URL Generator"

Coche :

✅ bot

✅ applications.commands

En bas, dans "Bot Permissions", coche :

✅ Send Messages

✅ Read Message History

✅ Add Reactions

✅ Manage Messages

2. Inviter le bot
Copie le lien généré tout en bas

Ouvre ce lien dans ton navigateur et choisis ton serveur

Clique sur "Autoriser"
---

## 🛠️ Installation

- Installe les dépendances
Le bot nécessite quelques bibliothèques Python.
entrez cela dans l'invite de commande : "pip install discord.py mcrcon psutil"

- Crée un fichier avec le nom .env dans le dossier du projet avec ce contenu (à adapter) :
DISCORD_TOKEN=TON_TOKEN_DISCORD
RCON_PASSWORD=TON_MOT_DE_PASSE_RCON
MINECRAFT_HOST=127.0.0.1
SERVER_BAT_PATH=C:\chemin\vers\run.bat
DISCORD_CHANNEL_ID=123456789012345678

- Démarre le bot et tu n'a plus qu'a
