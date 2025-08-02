import discord
import os
import subprocess
import psutil
import time
import signal
import asyncio
import socket
from discord.ext import commands
from mcrcon import MCRcon  # 📦 pip install mcrcon
from dotenv import load_dotenv
load_dotenv()
# ─────────────── CONFIGURATION DU BOT ─────────────── #

intents = discord.Intents.default()
intents.reactions = True
intents.guilds = True
intents.members = True
intents.message_content = True  # 🔥 Requis pour lire les messages

bot = commands.Bot(command_prefix="!", intents=intents)

# ─────────────── CONFIGURATION DU SERVEUR MINECRAFT ─────────────── #

HOST = os.getenv("MINECRAFT_HOST")  # ⚠️ Adresse IP locale ou publique du PC hébergeant le serveur
MINECRAFT_PORT = 25565  # Port du serveur Minecraft (à adapter si besoin)
RCON_PORT = 25575  # Port RCON défini dans server.properties
PASSWORD = os.getenv("RCON_PASSWORD")  # ⚠️ À sécuriser avec un fichier .env
SERVER_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # ID du salon Discord où apparaissent les contrôles
CONTROL_MESSAGE_ID = None  # Stockera dynamiquement l’ID du message de contrôle
SERVER_BAT_PATH = os.getenv("SERVER_BAT_PATH")

# ─────────────── FONCTIONS SERVEUR ─────────────── #

async def start_server():
    """Lance le serveur Minecraft via un script .bat."""
    try:
        # 📁 Remplace ce chemin par le chemin réel de ton script de lancement
        subprocess.Popen([SERVER_BAT_PATH], shell=True)
        print("✅ Serveur démarré.")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage : {e}")

async def stop_server():
    """Arrête proprement le serveur via RCON, puis termine le processus Java si nécessaire."""
    try:
        with MCRcon(HOST, PASSWORD, RCON_PORT) as mcr:
            response = mcr.command("stop")
            print(f"🛑 Serveur arrêté. Réponse : {response}")
    except Exception as e:
        print(f"❌ Erreur de connexion RCON : {e}")
        return

    await asyncio.sleep(15)  # Temps d'attente pour l'arrêt propre

    # Vérifie si un processus Java (Minecraft) est encore actif
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] and 'java' in proc.info['name'].lower():
            if any("minecraft" in str(arg).lower() for arg in proc.info['cmdline']):
                print(f"⚠️ Le processus Minecraft (PID {proc.pid}) est toujours actif. On le termine.")
                try:
                    os.kill(proc.pid, signal.SIGTERM)
                    print("✅ Processus Java terminé.")
                except Exception as e:
                    print(f"❌ Impossible de tuer le processus Java : {e}")
                break
    else:
        print("✅ Aucun processus Minecraft détecté.")

async def restart_server():
    """Redémarre le serveur."""
    try:
        await stop_server()
        await asyncio.sleep(5)
        await start_server()
        print("✅ Serveur redémarré.")
    except Exception as e:
        print(f"❌ Erreur lors du redémarrage : {e}")

async def check_server_status():
    """Met à jour le statut du bot Discord en fonction de l'état du serveur Minecraft."""
    while True:
        status = await is_server_online()
        activity = discord.Game("🟢 Serveur en ligne" if status else "🔴 Serveur hors ligne")
        await bot.change_presence(activity=activity)
        await asyncio.sleep(30)

async def is_server_online():
    """Teste la connectivité au serveur Minecraft."""
    try:
        with socket.create_connection((HOST, MINECRAFT_PORT), timeout=3):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

# ─────────────── ÉVÉNEMENTS DU BOT ─────────────── #

@bot.event
async def on_ready():
    global CONTROL_MESSAGE_ID
    print(f"✅ {bot.user} est connecté !")
    bot.loop.create_task(check_server_status())

    channel = bot.get_channel(SERVER_CHANNEL_ID)
    if channel is None:
        print("⚠️ Channel introuvable.")
        return

    try:
        await channel.purge()
        print("🗑️ Messages précédents supprimés.")
    except Exception as e:
        print(f"⚠️ Erreur de suppression : {e}")

    message = await channel.send(
        "🔧 **Contrôles du serveur Minecraft** :\n\n"
        "✅ Démarrer le serveur\n"
        "❌ Arrêter le serveur\n"
        "🔄 Redémarrer le serveur\n\n"
        "Réagissez avec un emoji pour interagir."
    )

    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await message.add_reaction("🔄")

    CONTROL_MESSAGE_ID = message.id
    print("📌 Message de contrôle en place.")

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user or CONTROL_MESSAGE_ID is None or reaction.message.id != CONTROL_MESSAGE_ID:
        return

    if reaction.emoji == "✅":
        await reaction.message.channel.send("✅ Démarrage du serveur...", delete_after=10)
        await start_server()
    elif reaction.emoji == "❌":
        await reaction.message.channel.send("🛑 Arrêt du serveur...", delete_after=5)
        await stop_server()
    elif reaction.emoji == "🔄":
        await reaction.message.channel.send("⏳ Redémarrage du serveur...", delete_after=10)
        await restart_server()

    try:
        await reaction.remove(user)
    except discord.Forbidden:
        pass

# ─────────────── COMMANDES TEXTUELLES ─────────────── #

@bot.command()
async def hello(ctx):
    await ctx.send("Salut ! Je suis en ligne. 😊")

@bot.command()
async def msg(ctx, *, message: str):
    """Envoie un message dans le chat Minecraft via RCON."""
    try:
        with MCRcon(HOST, PASSWORD, RCON_PORT) as mcr:
            mcr.command(f"say {message}")
            await ctx.send(f"📢 Message envoyé : {message}")
    except Exception as e:
        print(f"❌ Erreur RCON : {e}")
        await ctx.send("❌ Échec de l'envoi.")

@bot.command()
async def players(ctx):
    """Affiche les joueurs actuellement connectés."""
    try:
        with MCRcon(HOST, PASSWORD, RCON_PORT) as mcr:
            response = mcr.command("list")
            players_online = response.split(": ")[-1]
            await ctx.send(f"🟢 Joueurs en ligne : {players_online}")
    except Exception as e:
        await ctx.send("❌ Impossible de récupérer la liste.")
        print(f"Erreur : {e}")

# ─────────────── DÉMARRAGE DU BOT ─────────────── #

# 🔒 Sécurité : Utilise un fichier .env ou une variable d’environnement pour le token !
bot.run(os.getenv("DISCORD_TOKEN"))
