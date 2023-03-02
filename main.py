import discord
import mysql.connector
import os
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
import configparser
import logging
import logging.handlers

config = configparser.ConfigParser()
config.read('config.ini')

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
mydb = mysql.connector.connect(
  host=config.get('database', 'host'),
  user=config.get('database', 'user'),
  password=config.get('database', 'password'),
  database=config.get('database', 'database')
)

owners = config.get('Settings', 'Owners')
token = config.get('Settings', 'Token')
prefix = config.get('Settings', 'Prefix')

# Инициализация бота
intent = discord.Intents.all()
client = commands.Bot(intents=intent, command_prefix=prefix)

# Загрузка модулей из папки cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
          client.load_extension(f'cogs.{filename[:-3]}')
        except:
          print(f"Ошибка загрузки модуля {filename[:-3]}")

@client.event
async def on_ready():
    logging.info(f'{client.user.name} has connected to Discord!')

@client.command()
async def load(ctx, modul):
    if ctx.author.id in owners:
      try:
          client.load_extension(f"cogs.{modul}")
      except:
          await ctx.send("Ошибка при загрузке модуля")
    else:
        ctx.send("У вас не достаточно прав на данную комманду")
        print(f"Привышение полномочий со стороны пользователя {ctx.author.name} его id = {ctx.author.id}")
        print(f"попытка загрузить модуль {modul}")
        logging.warn(f'Нарушение: попытка загрузить модуль {modul} пользователем {ctx.author.name} его id = {ctx.author.id}')

@client.command()
async def unload(ctx, modul):
    if ctx.author.id in owners:
      try:
          client.unload_extension(f"cogs.{modul}")
      except:
          await ctx.send("Ошибка при выгрузке модуля")
    else:
        ctx.send("У вас не достаточно прав на данную комманду")
        print(f"Привышение полномочий со стороны пользователя {ctx.author.name} его id = {ctx.author.id}")
        print(f"попытка выгрузить модуль {modul}")
        logging.warn(f'Нарушение: попытка выгрузить модуль {modul} пользователем {ctx.author.name} его id = {ctx.author.id}')

@client.command()
async def reload(ctx, modul):
    if ctx.author.id in owners:
      try:
          client.reload_extension(f"cogs.{modul}")
      except:
          await ctx.send("Ошибка при перезарузке модуля")
    else:
        ctx.send("У вас не достаточно прав на данную комманду")
        print(f"Привышение полномочий со стороны пользователя {ctx.author.name} его id = {ctx.author.id}")
        print(f"попытка перезагрузить модуль {modul}")
        logging.warn(f'Нарушение: попытка перезагрузить модуль {modul} пользователем {ctx.author.name} его id = {ctx.author.id}')

client.run(token)