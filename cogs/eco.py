import discord
from datetime import datetime
from time import strftime
import time
from discord.utils import get
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from discord.ext import commands
from globals import conf
from database import db
from lib.bank import GuildMember


class eco(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.slash = SlashCommand(self.client, override_type=True)


    # Функция запроса баланса с базы данных, требует тестирования и проверки на коректность использование ctx в разных функциях
    def balance(self, ctx):
        member_id = ctx.author.id
        db.query(f"SELECT bank FROM eco WHERE member_id={member_id} AND guild_id{ctx.guild.id}")
        balance = db.cursor.fetchone()[0]["bank"]
        return balance


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

    
    # @cog_ext.cog_slash(name="transfer",
    #     description="Передать валюту другому участнику.",
    #     options=[
    #         create_option(
    #             name="пользователь",
    #             description="Упомяните пользователя, которому вы хотите передать валюту.",
    #             option_type=6,
    #             required=True
    #         ),
    #         create_option(
    #             name="количество",
    #             description="Количество валюты для передачи.",
    #             option_type=4,
    #             required=True
    #         )
    #     ])
    # async def transfer(self, ctx: SlashContext, пользователь, количество):
    #     # Проверяем, что пользователь существует и ввод корректен
    #     if пользователь is None:
    #         await ctx.send("Вы не упомянули пользователя.")
    #         return
    #     if not isinstance(количество, int) or количество <= 0:
    #         await ctx.send("Вы ввели некорректное количество валюты.")
    #         return
    #     SlashCommand.bulk_upsert_commands(commands)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        guild_member = GuildMember(message.author, message.guild)
        print(guild_member.balance)

        # Создаем контекстное меню, которое будет вызываться по правой кнопке мыши на сообщении
        ctx_menu = discord.ui.ContextMenu()

        # Добавляем команду "My Command" в контекстное меню
        async def transfer(interaction: discord.Interaction):
            await interaction.response.send_message("Вызвана команда передачи баланса!")

        ctx_menu.command(transfer, "Передать баланс")

        # Привязываем контекстное меню к сообщению
        await message.create_context_menu(ctx_menu)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        now = time.time()
        if before.channel is None and after.channel is not None:
            channel_id = after.channel.id
            guild_id = after.channel.guild.id
            # Проверяем, есть ли пользователь в базе данных
            result = db.query(f"SELECT * FROM voice_state WHERE member_id = {member.id} AND guild_id = {guild_id}")

            # Если пользователь есть в базе данных, обновляем данные о времени подключения и канале
            if result:
                db.query(f"UPDATE voice_state SET con_time = {int(time.time())}, guild_id = {member.guild.id}, last_channel_id = {after.channel.id} WHERE member_id = {member.id}")
                db.disconnect()
            # Если пользователь не найден, добавляем его в базу данных
            else:
                db.query(f"INSERT INTO voice_state (member_id, con_time, guild_id, last_channel_id) VALUES ({member.id}, {int(time.time())}, {member.guild.id}, {after.channel.id})")
                db.disconnect()

        elif before.channel is not None and after.channel is None:
            channel_id = before.channel.id
            guild_id = before.channel.guild.id
            guild = before.channel.guild
            # Подключаемся к базе данных
            db.init()
            result = db.query(f"SELECT con_time, voice_active FROM voice_state WHERE member_id = {member.id} AND guild_id = {member.guild.id}")
            if result:
                config_bank = db.query(f"SELECT cof_bal FROM guild_config WHERE guild_id = {guild.id}")
                if len(config_bank) == 0:
                    try:
                        db.query(f"INSERT IGNORE INTO guild_config (guild_id) VALUES ({guild.id})")
                        cof = 1
                        db.disconnect()
                    except:
                        print(f"Ошибка при добавление или проверке сервера {guild.name} его id {guild.id}")
                else:
                    cof = config_bank[0]["cof_bal"]
                con_time, voice_activ = result[0].values()
                channel_duration = now - con_time
                if voice_activ is not None:
                    va = voice_activ + channel_duration
                else:
                    va = channel_duration
                rval = (channel_duration * cof) / 60
                val = round(rval)
                bal = db.query(f"SELECT bank FROM eco WHERE member_id = {member.id} AND guild_id = {guild_id}")
                corect_bal = bal[0]["bank"]
                if corect_bal is None:
                    new_bal = val
                elif corect_bal is not None:
                    new_bal = corect_bal + val
                else:
                    print(f"ошибка запроса баланса пользователя {member.name} на сервер {guild.name}")
                    return
                # подсчет времени проведенного в войсе и внесение данные а БД + внесение валюты за активность в войсе
                db.query(f"UPDATE voice_state SET dis_time = {now}, last_channel_id = {before.channel.id}, voice_active = {va} WHERE member_id= {member.id} AND guild_id = {member.guild.id} AND con_time = {con_time}")
                db.query(f"UPDATE eco SET bank = {new_bal} WHERE member_id= {member.id} AND guild_id = {guild_id}")
                db.disconnect()
            else:
                print("Произошла ошибка, пользователь или сервер на котором он, не соответствуют данным из БД")
            
        
        else:
            if before.channel.id == after.channel.id:
                return
            else:
                print(f"{member.name} перешел с канала {before.channel.name} на канал {after.channel.name}")
         

def setup(client):
	client.add_cog(eco(client))
	print("Модуль eco подключен и работает")
