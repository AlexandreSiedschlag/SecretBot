import discord
import json
from discord import app_commands
from raid_helper import RaidHelper
from mover import Mover

def load_that_shit():
    with open('token.json') as f:
        data = json.load(f)
    return data

TOKEN = load_that_shit()["token"]
SERVER_ID = load_that_shit()["server_id"]

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # Nós usamos isso para o bot não sincronizar os comandos mais de uma vez
        self.table_message = None

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados
            await tree.sync(guild=discord.Object(id=SERVER_ID))  # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Entramos como {self.user}.")

client = Client()
tree = app_commands.CommandTree(client)

# Adiciona os comandos ao CommandTree
RaidHelper.ping(tree, SERVER_ID, client)
Mover.move(tree, SERVER_ID)
Mover.move_reacted(tree, SERVER_ID, client)

client.run(TOKEN)
