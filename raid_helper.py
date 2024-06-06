import discord
from discord import app_commands

class RaidHelper:
    main_classes = {
        "🛡️ Maintank": [],
        "⚔️ Offtank": [],
        "🩺 Mainhealer": [],
        "🔮 Shadowcaller": [],
        "💀 Silence": [],
        "🌿 Raizhealer": [],
        "🏹 Scout": []
    }

    dps_classes = {
        "👾 Pirquito": [],
        "🌟 Uvofrio": [],
        "🐻 Besta": [],
        "🐉 Fulgurante": []
    }

    support_classes = {
        "🗡️ Quebrarreinos": [],
        "🧙 Caça Espiritos": []
    }

    emoji_to_class = {
        "🛡️": "🛡️ Maintank",
        "⚔️": "⚔️ Offtank",
        "🩺": "🩺 Mainhealer",
        "🔮": "🔮 Shadowcaller",
        "💀": "💀 Silence",
        "🌿": "🌿 Raizhealer",
        "👾": "👾 Pirquito",
        "🌟": "🌟 Uvofrio",
        "🐻": "🐻 Besta",
        "🐉": "🐉 Fulgurante",
        "🏹": "🏹 Scout",
        "🗡️": "🗡️ Quebrarreinos",
        "🧙": "🧙 Caça Espiritos"
    }

    @staticmethod
    def find_user_class(user_display_name):
        for role, users in RaidHelper.main_classes.items():
            if user_display_name in users:
                return role
        for role, users in RaidHelper.dps_classes.items():
            if user_display_name in users:
                return role
        for role, users in RaidHelper.support_classes.items():
            if user_display_name in users:
                return role
        return None

    @staticmethod
    def ping(tree, server_id, client):
        @tree.command(guild=discord.Object(id=server_id), name='ping', description='Cria uma mensagem com uma tabela de funções')
        async def ping(interaction: discord.Interaction):
            embed = discord.Embed(title="AVAZINHA 8.1 PRA CANSAR VOCÊS", color=discord.Color.green())  # Alterar a cor aqui
            embed.add_field(name="Event Info:", value="06/06/2024 Calendar\n21:45 - None", inline=False)
            embed.add_field(name="Description:", value="DPS ARMA MINIMA 8.3 EQUIVALENTE...", inline=False)

            embed.add_field(name="Main Classes", value="\u200b", inline=False)
            for role, users in RaidHelper.main_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)
            
            embed.add_field(name="\u200b", value="\u200b", inline=False)  # Espaço extra para separação
            embed.add_field(name="DPS's", value="\u200b", inline=False)
            for role, users in RaidHelper.dps_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)
            
            embed.add_field(name="\u200b", value="\u200b", inline=False)  # Espaço extra para separação
            embed.add_field(name="Supports", value="\u200b", inline=False)
            for role, users in RaidHelper.support_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)

            await interaction.response.send_message(embed=embed)
            table_message = await interaction.original_response()

            reactions = ["🛡️", "⚔️", "🩺", "🔮", "🗡️", "💀", "🐉", "🌿", "👾", "🌟", "🐻", "🏹", "🧙"]
            for reaction in reactions:
                await table_message.add_reaction(reaction)

            client.table_message = table_message

        @client.event
        async def on_raw_reaction_add(payload):
            if client.table_message is None or payload.message_id != client.table_message.id:
                return

            guild = client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            if user.bot:
                return

            class_selected = RaidHelper.emoji_to_class.get(str(payload.emoji))
            if class_selected:
                current_class = RaidHelper.find_user_class(user.display_name)
                if current_class:
                    if current_class in RaidHelper.main_classes:
                        RaidHelper.main_classes[current_class].remove(user.display_name)
                    elif current_class in RaidHelper.dps_classes:
                        RaidHelper.dps_classes[current_class].remove(user.display_name)
                    elif current_class in RaidHelper.support_classes:
                        RaidHelper.support_classes[current_class].remove(user.display_name)
                    old_emoji = [emoji for emoji, cls in RaidHelper.emoji_to_class.items() if cls == current_class][0]
                    await client.table_message.remove_reaction(old_emoji, user)
                
                if class_selected in RaidHelper.main_classes:
                    RaidHelper.main_classes[class_selected].append(user.display_name)
                elif class_selected in RaidHelper.dps_classes:
                    RaidHelper.dps_classes[class_selected].append(user.display_name)
                elif class_selected in RaidHelper.support_classes:
                    RaidHelper.support_classes[class_selected].append(user.display_name)
            
            embed = discord.Embed(title="AVAZINHA 8.1 PRA CANSAR VOCÊS", color=discord.Color.green())  # Alterar a cor aqui
            embed.add_field(name="Event Info:", value="06/06/2024 Calendar\n21:45 - None", inline=False)
            embed.add_field(name="Description:", value="DPS ARMA MINIMA 8.3 EQUIVALENTE...", inline=False)
            
            embed.add_field(name="Main Classes", value="\u200b", inline=False)
            for role, users in RaidHelper.main_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)
            
            embed.add_field(name="DPS's", value="\u200b", inline=False)
            for role, users in RaidHelper.dps_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)
            
            embed.add_field(name="Supports", value="\u200b", inline=False)
            for role, users in RaidHelper.support_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)

            await client.table_message.edit(embed=embed)

        @client.event
        async def on_raw_reaction_remove(payload):
            if client.table_message is None or payload.message_id != client.table_message.id:
                return

            guild = client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            if user.bot:
                return

            class_selected = RaidHelper.emoji_to_class.get(str(payload.emoji))
            if class_selected:
                if user.display_name in RaidHelper.main_classes.get(class_selected, []):
                    RaidHelper.main_classes[class_selected].remove(user.display_name)
                elif user.display_name in RaidHelper.dps_classes.get(class_selected, []):
                    RaidHelper.dps_classes[class_selected].remove(user.display_name)
                elif user.display_name in RaidHelper.support_classes.get(class_selected, []):
                    RaidHelper.support_classes[class_selected].remove(user.display_name)
            
            embed = discord.Embed(title="AVAZINHA 8.1 PRA CANSAR VOCÊS", color=discord.Color.green())  # Alterar a cor aqui
            embed.add_field(name="Event Info:", value="06/06/2024 Calendar\n21:45 - None", inline=False)
            embed.add_field(name="Description:", value="DPS ARMA MINIMA 8.3 EQUIVALENTE...", inline=False)
            
            embed.add_field(name="Main Classes", value="\u200b", inline=False)
            for role, users in RaidHelper.main_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)
            
            embed.add_field(name="DPS's", value="\u200b", inline=False)
            for role, users in RaidHelper.dps_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)
            
            embed.add_field(name="Supports", value="\u200b", inline=False)
            for role, users in RaidHelper.support_classes.items():
                embed.add_field(name=role, value="\n".join(users) if users else "", inline=True)

            await client.table_message.edit(embed=embed)
