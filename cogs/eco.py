import discord
from datetime import datetime
from time import strftime
import time
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
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        now = int(time.time())
        if before.channel is None and after.channel is not None:
            channel_id = after.channel.id
            guild_id = after.channel.guild.id
            # Подключаемся к базе данных
            db.init()

            # Проверяем, есть ли пользователь в базе данных
            result = db.query(f"SELECT * FROM voice_state WHERE id = {member.id}")

            # Если пользователь есть в базе данных, обновляем данные о времени подключения и канале
            if result:
                db.query(f"UPDATE voice_state SET con_time = {int(time.time())}, guild_id = {member.guild.id}, last_channel_id = {after.channel.id} WHERE id = {member.id}")
            # Если пользователь не найден, добавляем его в базу данных
            else:
                db.query(f"INSERT INTO voice_state (id, con_time, dis_time, guild_id, last_channel_id) VALUES ({member.id}, {int(time.time())}, 0, {member.guild.id}, {after.channel.id})")
                db.disconnect()

        elif before.channel is not None and after.channel is None:
            channel_id = before.channel.id
            guild_id = before.channel.guild.id
            # Подключаемся к базе данных
            db.init()
            result = db.query(f"SELECT con_time, last_channel_id FROM voice_state WHERE user_id = {member.id} AND guild_id = {member.guild.id} ORDER BY con_time DESC LIMIT 1")
            if result:
                con_time, last_channel_id = result[0]
                channel_duration = now - con_time
                rval = channel_duration / 60
                val = round(rval)
                # подсчет времени проведенного в войсе и внесение данные а БД + внесение валюты за активность в войсе
                db.query(f"UPDATE voice_state SET dis_time = {now}, last_channel_id = {before.channel.id}, duration = {channel_duration} WHERE user_id = {member.id} AND guild_id = {member.guild.id} AND con_time = {con_time}")
                db.query(f"UPDATE eco SET bank = {val} WHERE user_id = {member.id} AND guild_id = {guild_id}")
                db.disconnect()
            else:
                print("Произошла ошибка, пользователь или сервер на котором он, не соответствуют данным из БД")
            
        
        else:
            print(f"{member.name} перешел с канала {before.channel.name} на канал {after.channel.name}")
         

def setup(client):
	client.add_cog(eco(client))
	print("Модуль eco подключен и работает")
