import discord
from datetime import datetime
from time import strftime
from discord.utils import get
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext import commands
import mysql.connector
from globals import conf

class eco(commands.Cog):
    def __init__(self, client):
        self.client = client

    

def setup(client):
	client.add_cog(eco(client))
	print("Ког eco работает")
