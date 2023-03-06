import discord
from discord.ext import commands
from datetime import datetime
from time import strftime
import time
import asyncio
from globals import conf, prefix
from database import db
from lib.bank import GuildMember


class marryage(commands.Cog):
    def __init__(self, client):
        self.client = client

    


    # Предложенние
    @commands.Cog.listener()
    async def on_message(self, ctx, message):
        if message.content.startswith(f'{prefix}marry'):
            # def check_author(m):
            #     return m.channel == ctx.channel and m.author == ctx.author
            member = #Придумать как получить упомянотого пользователя из сообшения
            # Добавить проверку на пользователя
            # Если не указан, остановить выполнение задачи
            msg = await ctx.send(f"""
            {member.mention}\n
            Пользователь {ctx.author.mention}. Делает вам предложение руки и сердца.\n
            {member.mention}каков будет ваш ответ?\n
            (Принимается ответ Да или Нет)
            """)
            author = ctx.author
            def check_member(m):
                return m.channel == ctx.channel and m.member == ctx.member
            try:
                message = await self.client.wait_for('message', check=check_member, timeout=300)
            except asyncio.TimeoutError:
                return await ctx.send(embed=discord.Embed(description=f"{author.mention} Время ожидания ответа вышло! \n Похоже что {member.mention} проигнорировал/а ваше предложение"))
            if message.content == str("Да") or message.content == str("да"):
                return await ctx.send(f'''
                    {author.mention} сделал/а предложение для {member.mention}\n
                    На что получил/а положительный ответ \n
                    Поздравляем наших молодоженов {author.mention} и {member.mention}
                    ''')
            elif message.content == str("Нет") or message.content == str("нет"):
                return await ctx.send(f'''
                    {author.mention} сделал/а предложение для {member.mention}\n
                    На что получил/а отрицательный ответ \n
                    Возможно в следуший раз между {author.mention} и {member.mention} что-то получится.
                    ''')
            else:
                await message.delete()
                return await ctx.send(f'{member.mention} Вы ответили не коректно, повторите попытку в следуший раз')

             

async def setup(client):
	await client.add_cog(marryage(client))
	print("Модуль marryage подключен и работает")