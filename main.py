import discord
from discord import app_commands

server_id = 1248346269051654195

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

client = MyClient()
client.run()

