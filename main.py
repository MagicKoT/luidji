import discord
from discord.ext import commands
from discord import app_commands
from database import db
import os
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from globals import conf, owners, token, prefix
import logging
import logging.handlers

# Создаем папку logs, если ее нет
if not os.path.exists('logs'):
    os.mkdir('logs')

# Устанавливаем конфигурацию логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(name)s %(message)s',
#     handlers=[
#         logging.FileHandler(f'logs/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log', encoding='utf-8')
#     ]
# )

# Инициализация бота
intent = discord.Intents.all()
client = commands.Bot(intents=intent, command_prefix=prefix)

# Загрузка модулей из папки cogs
async def initiate_modules():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await client.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print(f"Ошибка загрузки модуля {filename[:-3]}")
                print(e)


# Add the guild ids in which the slash command will appear. If it should be in all, remove the argument,
# but note that it will take some time (up to an hour) to register the command if it's for all guilds.

@client.event
async def on_ready():
    await initiate_modules()
    await client.tree.sync()

    logging.info(f'{client.user.name} has connected to Discord!')
    for guild in client.guilds:
        try:
            db.query(f"INSERT IGNORE INTO guild_config (guild_id) VALUES ({guild.id})")
        except:
            print(f"Ошибка при добавление или проверке сервера {guild.name} его id {guild.id}")
    db.disconnect()

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