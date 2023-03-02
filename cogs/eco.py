import discord
from datetime import datetime
from time import strftime
from discord.utils import get
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands
from globals import conf
from database import db

class eco(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # Собираем всех пользователей и записываем их в БД
        for guild in self.client.guilds:

            members_count_left = len(guild.members)
            member_counter = 0
            member_insert = []

            for member in guild.members:
                
                member_counter = member_counter + 1
                member_insert.append(f"('{member.id}', '{guild.id}')")
                
                # TODO: Transactions + Multiple insert maximum (research why mysql is so fucking disgustingly slow)
                if member_counter == 100 or member_counter == members_count_left:
                    db.query(f"INSERT IGNORE INTO eco (`member_id`, `guild_id`) VALUES " + ", ".join(member_insert))
                    members_count_left = members_count_left - member_counter
                    member_counter = 0
                    member_insert = []

        db.disconnect()

        members = db.query("SELECT * FROM member")
        print(members)

        members = db.query("SELECT * FROM member")
        print(members)

        db.disconnect()

        return
        

def setup(client):
	client.add_cog(eco(client))
	print("Ког eco работает")
