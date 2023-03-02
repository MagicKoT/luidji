import discord
import mysql.connector
import os
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from globals import conf, owners, token, prefix, host, user, password, database
import logging
import logging.handlers

# Создаем папку logs, если ее нет
if not os.path.exists('logs'):
    os.mkdir('logs')

# Устанавливаем конфигурацию логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[
        logging.FileHandler(f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log', encoding='utf-8')
    ]
)

# Подключение к базе данных MySQL
mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

# Инициализация бота
intent = discord.Intents.all()
client = commands.Bot(intents=intent, command_prefix=prefix)

# Загрузка модулей из папки cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
        try:
          client.load_extension(f'cogs.{filename[:-3]}')
        except:
          print(f"Ошибка загрузки модуля {filename[:-3]}")

@client.event
async def on_ready():
    logging.info(f'{client.user.name} has connected to Discord!')

def is_owner(ctx):
    return ctx.author.id in owners

@client.command()
@commands.check(is_owner)
async def load(ctx, modul):
    try:
          client.load_extension(f"cogs.{modul}")
          await ctx.message.add_reaction("✅")
    except:
          massage = ctx.send("Ошибка при загрузке модуля")
          await massage.add_reaction("❌")

@client.command()
@commands.check(is_owner)
async def unload(ctx, modul):
    try:
        client.unload_extension(f"cogs.{modul}")
        await ctx.message.add_reaction("✅")
    except:
        massage = ctx.send("Ошибка при выгрузке модуля")
        await massage.add_reaction("❌")

@client.command()
@commands.check(is_owner)
async def reload(ctx, modul):
    try:
        client.reload_extension(f"cogs.{modul}")
        await ctx.message.add_reaction("✅")
    except:
        massage = ctx.send("Ошибка при перезарузке модуля")
        await massage.add_reaction("❌")

client.run(token)