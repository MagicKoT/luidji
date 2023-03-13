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

    


    # Предложенние (Нужно проверить)
    @commands.command()
    async def marry(self, ctx, member):
        if member.id != ctx.author.id:
            # def check_author(m):
            #     return m.channel == ctx.channel and m.author == ctx.author
            member = message.mentions
            guild = ctx.guild
            # Добавить проверку на пользователя
            # Если не указан, остановить выполнение задачи
            await ctx.send(f"""
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
                husband = GuildMember(author.id, ctx.guild.id)
                wife = GuildMember(message.member.id, ctx.guild.id)
                price = db.query(f"SELECT marryage_price FROM guild_config WHERE guild_id={ctx.guild.id}")
                author_bank = husband['bank']
                member_bank = wife['bank']
                marry_price = price[0]["marryage_price"]
                new_bal_a = author_bank - marry_price
                new_bal_m =member_bank - marry_price
                if author_bank <= marry_price or member_bank <= marry_price:
                    ctx.send("К сожалению у одного из вас не хватает баланса, для того чтоб сыграть свадьбу")
                else:
                    try:
                        db.query(f"INSERT INTO marryage (member_id, coupe_member_id, guild_id) VALUES ({member.id}, {message.author.id}, {guild.id})")
                        db.query(f"INSERT INTO marryage (member_id, coupe_member_id, guild_id) VALUES ({author.id}, {member.id}, {guild.id})")
                        db.query(f"UPDATE eco SET bank = {new_bal_a} WHERE member_id= {author.id} AND guild_id = {ctx.guild_id}")
                        db.query(f"UPDATE eco SET bank = {new_bal_m} WHERE member_id= {message.author.id} AND guild_id = {ctx.guild_id}")
                        return await ctx.send(f'''
                            {author.mention} сделал/а предложение для {member.mention}\n
                            На что получил/а положительный ответ \n
                            Поздравляем наших молодоженов {author.mention} и {member.mention}
                            ''')
                    except Exception as e:
                        print("Ошибка при внесение данных в БД")
                        print(e)
                        ctx.send("Произошла не извесная ошибка, обратитесь к администрации")
                
            elif message.content == str("Нет") or message.content == str("нет"):
                return await ctx.send(f'''
                    {author.mention} сделал/а предложение для {member.mention}\n
                    На что получил/а отрицательный ответ \n
                    Возможно в следуший раз между {author.mention} и {member.mention} что-то получится.
                    ''')
            else:
                await message.delete()
                return await ctx.send(f'{member.mention} Вы ответили не коректно, повторите попытку в следуший раз')
        else:
            ctx.send("Детектор ЧСВ не выдержал перегрузки и сгорел")
        

    @commands.command()
    async def divorce(self, ctx, member):
        if member.id != ctx.author.id:
            author = ctx.author
            db_coupe = db.query(f"SELECT coupe_member_id FROM marryage WHERE member_id={author.id}")
            coupe_id = db_coupe[0]["coupe_member_id"]
            if coupe_id != member.id:
                ctx.send("Вы не можете подать на развод с человеком, который не имеет отношение к вам")
                return
            else:
                def check_member(m):
                    return m.channel == ctx.channel and m.member == ctx.member
                try:
                    message = await self.client.wait_for('message', check=check_member, timeout=300)
                except asyncio.TimeoutError:
                    return await ctx.send(embed=discord.Embed(description=f"{author.mention} Время ожидания ответа вышло! \n Похоже что {member.mention} проигнорировал/а ваше предложение о разводе.\n Попробуйте позже или обратитесь в суд!"))
                if message.content == str("Да") or message.content == str("да"):
                    db.query(f"UPDATE marryage SET coupe_member_id = null WHERE member_id= {author.id} AND guild_id = {ctx.guild_id}")
                    db.query(f"UPDATE marryage SET coupe_member_id = null WHERE member_id= {member.id} AND guild_id = {ctx.guild_id}")
                    await ctx.send("")
                if message.content == str("Нет") or message.content == str("нет"):
                    await ctx.send("")

async def setup(client):
	await client.add_cog(marryage(client))
	print("Модуль marryage подключен и работает")