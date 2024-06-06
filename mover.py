import discord
from discord import app_commands
from raid_helper import RaidHelper

class Mover:
    @staticmethod
    def move(tree, server_id):
        @tree.command(guild=discord.Object(id=server_id), name='move', description='Move todos os membros de um canal de voz para outro')
        async def move_all(interaction: discord.Interaction, from_channel: discord.VoiceChannel, to_channel: discord.VoiceChannel):
            for member in from_channel.members:
                await member.move_to(to_channel)
            await interaction.response.send_message(f"Todos os membros foram movidos de {from_channel.name} para {to_channel.name}", ephemeral=True)

    @staticmethod
    def move_reacted(tree, server_id, client):
        @tree.command(guild=discord.Object(id=server_id), name='move_reacted', description='Move todos os membros que reagiram na tabela de funções para outro canal de voz')
        async def move_reacted(interaction: discord.Interaction, from_channel: discord.VoiceChannel, to_channel: discord.VoiceChannel):
            if client.table_message is None:
                await interaction.response.send_message("A tabela de funções não foi encontrada.", ephemeral=True)
                return

            moved_members = []
            for member in from_channel.members:
                user_display_name = member.display_name
                if (RaidHelper.find_user_class(user_display_name) is not None):
                    await member.move_to(to_channel)
                    moved_members.append(user_display_name)
                    
            moved_members_str = "\n".join(moved_members) if moved_members else "Nenhum membro com reação foi encontrado."
            await interaction.response.send_message(f"Os seguintes membros foram movidos de {from_channel.name} para {to_channel.name}:\n{moved_members_str}", ephemeral=True)
