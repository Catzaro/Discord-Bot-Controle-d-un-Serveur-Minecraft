# 🤖 Bot Discord – Contrôle de serveur Minecraft

Ce bot Discord permet de démarrer, arrêter et redémarrer un **serveur Minecraft local** via des réactions emoji ou des commandes texte. Il utilise RCON pour interagir avec le serveur.

> ⚠️ La création du serveur Minecraft n'est pas expliquée ici. Ce bot est une alternative à Aternos ou autres hébergeurs. Il est recommandé d'avoir une bonne configuration.
>  
> 📁 **Place tous les fichiers du bot dans le dossier du serveur Minecraft.**

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
- Un bot Discord avec son token ([Créer une application Discord](https://discord.com/developers/applications))

---

## 🛠️ Installation

1. **Installer les dépendances**

Ouvre l'invite de commande et exécute :

```bash
pip install discord.py mcrcon psutil
```

2. **Créer le fichier `.env`**

Dans le dossier du projet, crée un fichier nommé `.env` avec ce contenu (à adapter) :

```
DISCORD_TOKEN=TON_TOKEN_DISCORD
RCON_PASSWORD=TON_MOT_DE_PASSE_RCON
MINECRAFT_HOST=127.0.0.1
SERVER_BAT_PATH=C:\chemin\vers\run.bat
DISCORD_CHANNEL_ID=123456789012345678
```

---

## 🤖 Création du Bot Discord

1. **Créer l'application**

   - Va sur [discord.com/developers/applications](https://discord.com/developers/applications)
   - Clique sur "New Application", donne-lui un nom, puis clique sur "Create"

2. **Activer les intents nécessaires**

   Dans l'onglet "Bot", active :
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

   > Ces options sont nécessaires pour que le bot lise les messages et interagisse avec les membres.

3. **Copier le token du bot**

   - Clique sur "Reset Token" si besoin
   - Clique sur "Copy" pour récupérer le token
   - Colle-le dans le fichier `.env` :  
     `DISCORD_TOKEN=ton_token_ici`

---

## 📩 Inviter le bot sur ton serveur

1. **Générer le lien d'invitation**

   - Va dans "OAuth2" > "URL Generator"
   - Coche :
     - ✅ bot
     - ✅ applications.commands
   - En bas, dans "Bot Permissions", coche :
     - ✅ Send Messages
     - ✅ Read Message History
     - ✅ Add Reactions
     - ✅ Manage Messages

2. **Inviter le bot**

   - Copie le lien généré tout en bas dans "Generated URL"
   - Ouvre ce lien dans ton navigateur et choisis ton serveur
   - Clique sur "Autoriser"

---

## 🔎 Obtenir l'ID du salon Discord

Le bot a besoin de l'ID du salon où il enverra les contrôles.

1. Dans Discord, fais un clic droit sur le salon prévu pour le bot  
   > ⚠️ Tous les messages dans ce salon seront supprimés à chaque démarrage du bot.

2. Tu obtiendras une URL comme :  
   `https://discord.com/channels/557999937405048484/123456789012345678`

3. Copie la série de chiffres à la fin (l'ID du salon).

4. Colle cet ID dans ton fichier `.env` :  
   `DISCORD_CHANNEL_ID=123456789012345678`

---

## ✅ Démarrer le bot

Tu n'as plus qu'à le démarrer !
