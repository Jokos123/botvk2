import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time
import os.path
import sqlite3
import asyncio
import json
import requests
import jishaku
import wikipedia
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rodinadb:nbsGK02riO3PkygA@cluster0.cdvgc.mongodb.net/rodina?retryWrites=true&w=majority")
db = cluster["rodina"]
nel = db["nel"]
mess = db["mess"]
quest = db["quest"]
gquest = db["gquest"]
voise = db["voise"]
questik = db["questik"]

global tens
tens = [ ]

def addbt(member: discord.Member, arg : int):
  if nel.count_documents({"id": member.id}) == 0:
    nel.insert_one({"guild": member.guild.id, "id": member.id, "nel": arg})
    return arg
  else:
    bal = arg + nel.find_one({"id": member.id})["nel"]
    nel.update_one({"id": member.id}, {"$set": {"nel": bal}})
    return bal

def rebt(member: discord.Member, arg : int):
  bal = nel.find_one({"id": member.id})["nel"] - arg
  nel.update_one({"id": member.id}, {"$set": {"nel": bal}})
  return bal

def proverka(member, stv : int):
  if nel.count_documents({"id": member.id}) == 0:
    return 0

  else:
    if nel.find_one({"id": member.id})["nel"] < stv:
      return 0
    else:
      return 1

def proc(args):
  s = 0
  if args >= 10 and args <= 30:
    s = 1
  elif args > 30 and args <= 70: 
    s = 2
  elif args > 70 and args <= 70: 
    s = 3
  elif args > 70 and args <= 90: 
    s = 4
  elif args > 90 and args <= 170: 
    s = 7
  elif args > 170: 
    s = 10

  return s


class econom(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prev = []
        
    @commands.command()
    async def topcoins(self, ctx):
      nel = db["nel"]
      zb = 0

      m = [ ]
      m2 = [ ]
      m3 = [ ]
      c = [ ]
      c2 = [ ]
      cz = [ ]
      cz2 = [ ]
      fr = 0
      zb = 70
      for i in nel.find({"guild": ctx.guild.id}):
        mname = discord.utils.get(ctx.guild.members, id = i["id"])
        if mname == None:
          continue
        m.append(i["nel"])
        cz.append(mname.name)

        nel = i["nel"]

        c.append(f'**Коинов:** `{nel}`')
        fr += 1
        if fr >= 70:
          break
      
      m2 = m
      m3 = m
      c2 = c
      cz2 = cz
      t = sorted(m)[::-1]

      frf = 0
      frfz = 0
      stra = 1
      zbs = zb//10
      if zbs == 0:
        zbs = 1
      embed = discord.Embed(title = f'Таблица лидеров', description = None, colour = 0x09F2C8)
      for v in t:
        frfz += 1
        frf += 1
        f = m2.index(v)
        if frf == 1:
          frs = f'🥇 1. {cz[f]}'
        elif frf == 2:
          frs = f'🥈 2. {cz[f]}'
        elif frf == 3:
          frs = f'🥉 3. {cz[f]}'
        else:
          frs = f'{frf}. {cz[f]}'
        embed.add_field(name = frs, value = c[f], inline = False)
        c.remove(c[f])
        cz.remove(cz[f])
        m2.remove(m2[f])
        if frfz == 10:
          frfz = 0
          break     

      mes = await ctx.send(embed = embed)
    
    @commands.command()
    async def coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 822900692104249425:
            return

      if member == None:
        member = ctx.author

      if nel.count_documents({"id": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'Никнейм: {member.mention}\nКоины: `0`', colour = 0x09F2C8))

      else:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'Никнейм: {member.mention}\nКоины: `{nel.find_one({"id": member.id})["nel"]}`', colour = 0x09F2C8))

    @commands.command()
    @commands.has_any_role(id, id, id, '★ Управляющий сервером ★')
    async def addcoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 822900692104249425:
            return

      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**Укажите пользователя**', colour = 0x09F2C8), delete_after = 7)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{member.mention}, укажите кол-во добавляемых коинов**', colour = 0x09F2C8), delete_after = 7)

      if nel.count_documents({"id": member.id}) == 0:
        a = addbt(member, amount)
        await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, вы добавили пользователю {member.mention} `{amount}` коинов.\nЕго баланс: `{a}` коинов**', colour = 0x09F2C8))
      else:
        a = addbt(member, amount)
        channel = self.client.get_channel(823584143072952380)
        await channel.send(embed = discord.Embed(title = 'Выдача', description = f'**Модератор {ctx.author.mention} выдал коинов пользователю {member.mention} в размере `{amount}`**', colour = 0x27f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, вы добавили пользователю {member.mention} `{amount}` коинов.\nЕго баланс: `{a}` коинов**', colour = 0x09F2C8), delete_after = 10)

    @commands.command()
    @commands.has_any_role(id, id, id, '★ Управляющий сервером ★')
    async def removecoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 822900692104249425:
            return

      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, укажите пользователя**', colour = 0x09F2C8), delete_after = 7)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, укажите кол-во убираемых коинов**', colour = 0x09F2C8), delete_after = 7)
      
      a = proverka(member, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, пользователь не имеет такого кол-ва коинов!**', colour = 0x09F2C8))
      else:
        bal = rebt(member, amount)
        channel = self.client.get_channel(823584143072952380)
        await channel.send(embed = discord.Embed(title = 'Снятие', description = f'**Модератор {ctx.author.mention} снял коинов пользователю {member.mention} в размере `{amount}`**', colour = 0x27f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, вы удалили у пользователя {member.mention} `{amount}` коинов.\nЕго баланс: `{bal}` коинов**', colour = 0x09F2C8), delete_after = 10)    

    @commands.command()
    async def pay(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 822900692104249425:
            return

      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, укажите пользователя**', colour = 0x09F2C8), delete_after = 7)
      
      if member == ctx.author or member.bot:
        return

      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, укажите сумму монет которую нужно передать!**', colour = 0x09F2C8), delete_after = 7)

      if amount <= 0:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, указан неверный аргумент!**', colour = 0x09F2C8), delete_after = 7)


      a = proverka(ctx.author, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, Вы не можете передать такую сумму!**', colour = 0x09F2C8))

      else:
        bal = addbt(member, amount)
        bal2 = rebt(ctx.author, amount)
        channel = self.client.get_channel(823584143072952380)
        await channel.send(embed = discord.Embed(title = 'Перевод', description = f'**Пользователь {ctx.author.mention}, передал Коины пользователю {member.mention} в размере `{amount}`**', colour = 0x27f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, Вы передали пользователю {member.mention} `{amount}` коинов.\nЕго баланс: `{bal}` коинов\nВаш баланс: `{bal2}` коинов**', colour = 0x09F2C8))
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def casino(self, ctx, amount : int = None):
      if not ctx.guild.id == 822900692104249425:
            return

      if not ctx.channel.id == 823583370458038302:
        await ctx.message.delete()
        return await ctx.send(embed = discord.Embed(description = f'**Команда `/casino` доступна только в канале <#823583370458038302>**', colour = 0x09F2C8), delete_after = 7)
        
      if amount == None:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, укажите кол-во коинов которое необходимо поставить!**', colour = 0x09F2C8))

      if amount <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, неверный аргумент!**', colour = 0x09F2C8))

      a = proverka(ctx.author, amount)
      if a == 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, Вы не можете сделать такую ставку!**', colour = 0x09F2C8))
      else:
        await ctx.send(embed = discord.Embed(title = f'Central district || nelegals', description = f'**{ctx.author.mention}, Отдохни минутку и получешь результат!**', colour = 0x09F2C8))
        a = random.randint(1, 2)
        if a == 1:
          await asyncio.sleep(7)
          bal = rebt(ctx.author, amount)
          await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, к сожалению, вы проиграли!\nТеперь Ваш баланс составляет: `{bal}` коинов!**', colour = 0xff0000))
        if a == 2:
          amount *= 1
          await asyncio.sleep(7)
          f = amount
          bal = addbt(ctx.author, f)
          return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{ctx.author.mention}, Вам повезло, вы удвоили свою ставку!!\nТеперь Ваш баланс составляет: `{bal}` коинов!**', colour = 0x27f20a))

    @commands.command()
    @commands.has_any_role(id, id, id, '★ Управляющий сервером ★')
    async def reset_nel(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 822900692104249425:
            return

      if not member:
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя!```', delete_after = 7)

      if ctx.author.top_role.position <= member.top_role.position:
        return

      if nel.count_documents({"id": member.id}) != 0:
        nel.update_one({"id": member.id}, {"$set": {"nel": 0}})
      else:
        pass
      channel = self.client.get_channel(823584143072952380)
      await channel.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил Коины пользователю {member.mention}!**', colour = 0x27f20a, timestamp = ctx.message.created_at))
      return await ctx.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил Коины пользователю {member.mention}!**', colour = 0x27f20a), delete_after = 10)      
            
    @commands.Cog.listener()
    async def on_message(self, ctx):
      if mess.count_documents({"id": ctx.author.id}) == 0:
        mess.insert_one({"id": ctx.author.id, "messages": 0, "vsv": 0})
        a = mess.find_one({"id": ctx.author.id})["messages"]
        mess.update_one({"id": ctx.author.id}, {"$set": {"messages": a + 1}})
      else:
        a = mess.find_one({"id": ctx.author.id})["messages"]
        mess.update_one({"id": ctx.author.id}, {"$set": {"messages": a + 1}})

      st = 0
      if len(list(ctx.content)) >= 1:
        msgs = mess.find_one({"id": ctx.author.id})["messages"]
        if msgs == 300:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 300 сообщений!`\n🎉Вам добавлен бонус в размере 7 коинов <3**', colour = discord.Colour.blue()))
          st += 7
        if msgs == 600:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 600 сообщений!`\n🎉Вам добавлен бонус в размере 7 коинов <3**', colour = discord.Colour.blue()))
          st += 7     
        if msgs == 900:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 900 сообщений!`\n🎉Вам добавлен бонус в размере 7 коинов <3**', colour = discord.Colour.blue()))
          st += 7
        if msgs == 1500:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 1500 сообщений!`\n🎉Вам добавлен бонус в размере 7 коинов <3**', colour = discord.Colour.blue()))
          st += 7
        if msgs == 2500:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 2500 сообщений!`\n🎉Вам добавлен бонус в размере 7 коинов <3**', colour = discord.Colour.blue()))
          st += 7
        if msgs == 5000:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 5000 сообщений!`\n🎉Вам добавлен бонус в размере 7 коинов <3**', colour = discord.Colour.blue()))
          st += 7

        if st > 0:
          addbt(ctx.author, st)

    @commands.command(aliases = ["messages", "сообщения"])
    async def __message(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 822900692104249425:
        return

      if member == None:
        member = ctx.author

      if mess.count_documents({"id": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'Никнейм: {member.mention}\nСообщений: `0`', colour = 0x09F2C8))

      else:
        return await ctx.send(embed = discord.Embed(title = f'Central district || nelegals', description = f'Никнейм: {member.mention}\nСообщений: `{mess.find_one({"id": member.id})["messages"]}`', colour = 0x09F2C8))

    @commands.command()
    async def achive(self, ctx):
      if not ctx.guild.id == 822900692104249425:
        return

      if mess.count_documents({"id": ctx.author.id}) == 0:
        return await ctx.send(f'{ctx.author.mention}, эй друг, попробуй ещё раз!')

      achive = []
      msgs = mess.find_one({"id": ctx.author.id})["messages"]
      if msgs >= 300:
        achive.append('[✅] Написать `300` сообщений\n')
      else:
        achive.append('[❌] Написать `300` сообщений\n')
      if msgs >= 600:
        achive.append('[✅] Написать `600` сообщений\n')
      else:
        achive.append('[❌] Написать `600` сообщений\n')
      if msgs >= 900:
        achive.append('[✅] Написать `900` сообщений\n')
      else:
        achive.append('[❌] Написать `900` сообщений\n')
      if msgs >= 1500:
        achive.append('[✅] Написать `1500` сообщений\n')
      else:
        achive.append('[❌] Написать `1500` сообщений\n')
      if msgs >= 2500:
        achive.append('[✅] Написать `2500` сообщений\n')
      else:
        achive.append('[❌] Написать `2500` сообщений\n')
      if msgs >= 5000:
        achive.append('[✅] Написать `5000` сообщений\n')
      else:
        achive.append('[❌] Написать `5000` сообщений\n')

      voice = []
      voiss = mess.find_one({"id": ctx.author.id})["vsv"]
      if voiss >= 10800:
        voice.append('[✅] Просидеть `3` часа в голосовом канале\n')
      else:
        voice.append('[❌] Просидеть `3` часа в голосовом канале\n')
      if voiss >= 25200:
        voice.append('[✅] Просидеть `7` часов в голосовом канале\n')
      else:
        voice.append('[❌] Просидеть `7` часов в голосовом канале\n')
      if voiss >= 54000:
        voice.append('[✅] Просидеть `15` часов в голосовом канале\n')
      else:
        voice.append('[❌] Просидеть `15` часов в голосовом канале\n')
      if voiss >= 72000:
        voice.append('[✅] Просидеть `20` часов в голосовом канале\n')
      else:
        voice.append('[❌] Просидеть `20` часов в голосовом канале\n')
      if voiss >= 108000:
        voice.append('[✅] Просидеть `30` часов в голосовом канале\n')
      else:
        voice.append('[❌] Просидеть `30` часов в голосовом канале\n')
      if voiss >= 126000:
        voice.append('[✅] Просидеть `35` часов в голосовом канале\n')
      else:
        voice.append('[❌] Просидеть `35` часов в голосовом канале\n')

      str_a = ''.join(achive)
      str_v = ''.join(voice)
      embed = discord.Embed(title = f"`💰 Ачивки пользователя {ctx.author.name}`", colour = discord.Colour.blue())
      embed.add_field(name = '♦ Сообщения:', value = f'{str_a}')
      embed.add_field(name = '♦ Голосовой чат:', value = f'{str_v}')
      embed.set_footer(text = 'Support Team by Jokos', icon_url = ctx.guild.icon_url)
      await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def createquest(self, ctx):
        m = await ctx.send("**`Напишите в чат описание:`**")
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            msg = await self.client.wait_for('message', check = check, timeout= 30.0)
        except TimeoutError:
            await ctx.message.delete()
            return await m.delete()
        else:
            await msg.delete()
            await m.edit(content = f'`[CREATE_QUEST]` `Создание quest. Укажите несколько аргументов написав их в чат`\n1.`Описание:` {msg.content}')
            m1 = await ctx.send("**`Напишите в чат сколько будет выдано коинов:`**")
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            try:
                msg1 = await self.client.wait_for('message', check = check, timeout= 30.0)
            except TimeoutError:
                await ctx.message.delete()
                return await m1.delete()
            else:
                await msg1.delete()
                await m1.delete()
                await m.edit(content = f'`[CREATE_QUEST]` `Создание quest. Укажите несколько аргументов написав их в чат`\n1.`Описание:` {msg.content}\n2.`Коинов:` {msg1.content}')
                m2 = await ctx.send("**`Напишите в чат до сколько можно будет выполнить квест(Пример: 23.03-19:00)`**")
                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author
                try:
                    msg2 = await self.client.wait_for('message', check = check, timeout= 30.0)
                except TimeoutError:
                    await ctx.message.delete()
                    return await m2.delete()
                else:
                    await msg2.delete()
                    await m2.delete()
                    await m.edit(content = f'`[CREATE_QUEST]` `Создание quest. Укажите несколько аргументов написав их в чат`\n1.`Описание:` {msg.content}\n2.`Коинов:` {msg1.content}\n3.`Време:` {msg2.content}')
                    m3 = await ctx.send("**`Напишите в чат Title")
                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author
                    try:
                        msg3 = await self.client.wait_for('message', check = check, timeout= 30.0)
                    except TimeoutError:
                        await ctx.message.delete()
                        return await m3.delete()
                    else:
                        await msg3.delete()
                        await m3.delete()
                        await m.edit(content = f'`[CREATE_QUEST]` `Создание quest. Укажите несколько аргументов написав их в чат`\n1.`Описание:` {msg.content}\n2.`Коинов:` {msg1.content}\n3.`Време:` {msg2.content}\n4.`Title`: {msg3.content}')
                        m4 = await ctx.send("**`Подтвердите ваши действия(+/-)`**")
                        def check(m):
                            return m.channel == ctx.channel and m.author == ctx.author
                        try:
                            msg4 = await self.client.wait_for('message', check = check, timeout= 30.0)
                        except TimeoutError:
                            await ctx.message.delete()
                            return await m4.delete()
                        else:
                            if msg4.content == "+":
                                await msg4.delete()
                                await m4.delete()
                                await m.edit(content = f'`[CREATEFAM]` `квест успешно зарегистрирована.` \n1.`Описание:` {msg.content}\n2.`Коинов:` {msg1.content}\n3.`Време:` {msg2.content}')
                                questik.update_one({"guild": ctx.guild.id}, {"$set": {"quest": msg.content, "coin": msg1.content, "time": msg2.content, "title": msg3.content, "zakritq": 0}})
                                channel = self.client.get_channel(822938428147499038)
                                await channel.send('@everyone', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'{ctx.author.mention}`, выдал новое ежедневное задание. Чтобы посмотреть его пропишите в чат /quest`', colour = 0x09F2C8))
                            else:
                                return

    @commands.command()
    async def quest(self, ctx):
        if questik.count_documents({"zakritq": 1}):
          await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'Эй, щас квеста нет, иди чуть позже напиши :(', colour = 0x09F2C8))
          return
        if quest.count_documents({"id": ctx.author.id}) == 0:
            quest.insert_one({"id": ctx.author.id, "vzal_quest": 1, "questcompit": 0})
            embed = discord.Embed(description = f'Привет, ты начал выполнять квест {questik.find_one({"guild": ctx.guild.id})["title"]}. Ну тогда читай его ниже!\n\n```{questik.find_one({"guild": ctx.guild.id})["quest"]}\n\nНаграда:{questik.find_one({"guild": ctx.guild.id})["coin"]}\nКвест выполнить можно до {questik.find_one({"guild": ctx.guild.id})["time"]}```\n\n**Если вы выполнии квест, то пропишите /questcompit(писать надо в дискорде Нелегалов)**', colour = discord.Colour.blue())
            embed.set_author(name='Central district || nelegals', icon_url= 'https://i.imgur.com/s5CvtOT.png')
            embed.set_footer(text = f'Support Team by Jokos', icon_url = 'https://i.imgur.com/s5CvtOT.png')
            await ctx.author.send(embed = embed)
            await ctx.send(f'{ctx.author.mention}, я тебе отправил квест в лс!')
            return
        if quest.count_documents({"id": ctx.author.id, "vzal_quest": 1, "questcompit": 0}):
            await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'Вы и так уже взяли квест `{questik.find_one({"guild": ctx.guild.id})["title"]}`, для начало выполните этот квест!\nЯ тебе повторно отправил в личку квест!', colour = 0x09F2C8))
            embed = discord.Embed(description = f'```{questik.find_one({"guild": ctx.guild.id})["quest"]}\n\nНаграда:{questik.find_one({"guild": ctx.guild.id})["coin"]}\nКвест выполнить можно до {questik.find_one({"guild": ctx.guild.id})["time"]}```\n\n**Если вы выполнии квест, то пропишите /questcompit(писать надо в дискорде Нелегалов)**', colour = discord.Colour.blue())
            embed.set_author(name='Central district || nelegals', icon_url= 'https://i.imgur.com/s5CvtOT.png')
            embed.set_footer(text = f'Support Team by Jokos', icon_url = 'https://i.imgur.com/s5CvtOT.png')
            await ctx.author.send(embed = embed)
            return
        if quest.count_documents({"id": ctx.author.id, "vzal_quest": 1, "questcompit": 1}):
        	await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'Вы и так уже выполнили квест `{questik.find_one({"guild": ctx.guild.id})["title"]}`!\nОжидайте следующий квест.', colour = 0x09F2C8))
        	return
        

    @commands.command()
    async def questcompit(self, ctx):
      if questik.count_documents({"zakritq": 1}):
        await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'Эй, щас квеста нет, иди чуть позже напиши :(', colour = 0x09F2C8))
        return

      if quest.count_documents({"id": ctx.author.id, "vzal_quest": 1, "questcompit": 1}):
    	  await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'Вы и так уже выполнили квест `{questik.find_one({"guild": ctx.guild.id})["title"]}`!\nОжидайте следующий квест.', colour = 0x09F2C8))
    	  return

      if quest.count_documents({"id": ctx.author.id}) == 0:
    	  await ctx.send(f'{ctx.author.mention}', embed = discord.Embed(title = 'Central district || nelegals', icon_url='https://i.imgur.com/h0pansM.png', description = f'Эй, ты ещё не взял квест `{questik.find_one({"guild": ctx.guild.id})["title"]}`, пропиши /quest чтобы принять квест!.', colour = 0x09F2C8))
    	  return


      if quest.count_documents({"id": ctx.author.id, "vzal_quest": 1, "questcompit": 0}):
          embed = discord.Embed(description = f'Привет, ты уже выполнил квест? Ну тогда заполни форму ниже и отправь в чат!\n\n```1. Ваш ник(анг):\n2. Статистика аккаунта:\n3. Доказательства выполнения квеста:```', colour = discord.Colour.blue())
          embed.set_author(name='Central district || nelegals', icon_url= 'https://i.imgur.com/s5CvtOT.png')
          embed.set_footer(text = f'Support Team by Jokos', icon_url = 'https://i.imgur.com/s5CvtOT.png')
          m = await ctx.send(embed = embed)
          def check(m):
        	  return m.channel == ctx.channel and m.author == ctx.author
          try:
        	  msg = await self.client.wait_for('message', check = check, timeout= 999.0)
          except TimeoutError:
        	  await ctx.message.delete()
        	  return await m.delete()
          else:
        	  await msg.delete()
        	  await m.delete()
        	  quest.update_one({"id": ctx.author.id}, {"$set": {"vzal_quest": 1, "questcompit": 1}})
        	  await ctx.send(f'{ctx.author.mention}, ваша заявка была отправлена, ожидайте одобрение. Если ваша заявка будет одобрена, вам бот в лс отпишет!', delete_after = 10)
        	  channel = self.client.get_channel(823908750385610812)
        	  await ctx.send("+")
        	  await channel.send(embed = discord.Embed(description = f'```{msg.content}```\n\nЕсли заявка одобрена пропишите /quitquest {ctx.author.id}', colour = 0x27f20a, timestamp = ctx.message.created_at))

    @commands.command()
    @commands.has_any_role(id, id, id, '★ Управляющий сервером ★')
    async def quitquest(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 822900692104249425:
        return

      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**Укажите пользователя**', colour = 0x09F2C8), delete_after = 7)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'**{member.mention}, укажите кол-во добавляемых коинов**', colour = 0x09F2C8), delete_after = 7)

      if nel.count_documents({"id": member.id}) == 0:
        a = addbt(member, amount)
        await member.send(f"Ваша заявка была одобрена, вам были начислены коины!")
      else:
        a = addbt(member, amount)
        await member.send(f"Ваша заявка была одобрена, вам были начислены коины!")

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command()
    async def ящик(self, ctx):
      ag = random.choices([1, 2, 3, 4, 5, 6], weights=[35, 15, 10, 5, 0.05, 0.01])[0]
      embed = discord.Embed(title = "Вскрытие сундучка", description = f"{ctx.author.mention} **Пожалуйста подождите на вскрытие ящик пандоры понадобится время\n`Ящика пандоры откроется через 10 секунд!`**", Colour = 0xFB9E14)
      await ctx.send(embed = embed, delete_after = 10.0)
      await asyncio.sleep(10.0)
      if ag == 1:
        e = discord.Embed(title = "📦 Вскрытие ящика пандоры 📦", description = f"{ctx.author.mention} **я успешно выскрыл ящик пандоры и вот что от туда выпало!\nВаш приз: 1 коин в дискорде**", Colour = 0xFB9E14)
        await ctx.send(embed = e)
        a = nel.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["nel"]
        nel.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"nel": a + 1}})
      elif ag == 2:
        e = discord.Embed(title = "📦 Вскрытие ящика пандоры 📦", description = f"{ctx.author.mention} **я успешно выскрыл ящик пандоры и вот что от туда выпало!\nВаш приз: 2 коина в дискорде**", Colour = 0xFB9E14)
        await ctx.send(embed = e)
        a = nel.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["nel"]
        nel.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"nel": a + 2}})
      elif ag == 3:
        e = discord.Embed(title = "📦 Вскрытие ящика пандоры 📦", description = f"{ctx.author.mention} **я успешно выскрыл ящик пандоры и вот что от туда выпало!\nВаш приз: 3 коина в дискорде**", Colour = 0xFB9E14)
        await ctx.send(embed = e)
        a = nel.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["nel"]
        nel.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"nel": a + 3}})
      elif ag == 4:
        e = discord.Embed(title = "📦 Вскрытие ящика пандоры 📦", description = f"{ctx.author.mention} **я успешно выскрыл ящик пандоры и вот что от туда выпало!\nВаш приз: 4 коина в дискорде**", Colour = 0xFB9E14)
        await ctx.send(embed = e)
        a = nel.find_one({"id": ctx.author.id, "guild": ctx.guild.id})["nel"]
        nel.update_one({"id": ctx.author.id, "guild": ctx.guild.id}, {"$set": {"nel": a + 4}})
      elif ag == 5:
        e = discord.Embed(title = "📦 Вскрытие ящика пандоры 📦", description = f"{ctx.author.mention} **я успешно выскрыл ящик пандоры и вот что от туда выпало!\nВаш приз: личная роль в дискорде!\n\nЧтобы получить свою роль от пиши vk.com/jokos2**", Colour = 0xFB9E14)
        await ctx.send(embed = e)
      elif ag == 6:
        e = discord.Embed(title = "📦 Вскрытие ящика пандоры 📦", description = f"{ctx.author.mention} **я успешно выскрыл ящик пандоры и вот что от туда выпало!\nВаш приз: любой скин на сервере!\n\nЧтобы получить свою роль от пиши vk.com/jokos2**", Colour = 0xFB9E14)
        await ctx.send(embed = e)

    @commands.command()
    async def wiki(self, ctx, *, text = None):

      if text == None:
        return await ctx.send(embed = discord.Embed(description = f'**❌ {ctx.author.mention}, укажите что нужно искать.**'), delete_after = 5) 

      msg = await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.mention}, начинаю загружать информацию, немного подождите.**', Colour = discord.Colour.gold()))
      wikipedia.set_lang("ru")
      new_page = wikipedia.page(text)
      summ = wikipedia.summary(text)
      try:
        emb = discord.Embed(title= f'\nСодержание запроса после парса: {new_page.title}', description= f'**\n{summ}**', Colour = discord.Colour.gold())
        emb.set_author(name = 'Информация из википедии', url = 'https://vk.com/norimyxxxo1702', icon_url = 'https://avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        emb.set_footer(text = f'Информация показана для {ctx.author.display_name}', icon_url = ctx.author.avatar_url)
        await msg.edit(embed=emb)
      except:
        embed = discord.Embed(description = f'**❌ {ctx.author.mention}, мне не удалось найти информацию по запросу {text}.**', Colour = discord.Colour.gold())
        await msg.edit(embed=embed)

    @commands.command()
    async def help(self, ctx):
      if not ctx.guild.id == 822900692104249425:
            return
            
      embed = discord.Embed(title = 'Nelegal | Commands Panel', colour = 0x09F2C8)
      embed.add_field(name = "💰 Economy", value = f'```/casino [ставка] - Играть в казино (доступно только в 👹казино ).\n/coins [упоминание] - посмотреть количество семечек у себя или у пользователя.\n/pay [упоминание] [количество] - передать свои коины кому-то.\n/achive - Посмотреть выполненные ачивки.\n/topcoins - Таблица лидеров.\n/ящик - Ящик пандоры с которого может выпасть разные плюшки.\n/инфоящик - Посмотреть что может выпасть с ящика пандоры.```', inline = False)
      embed.add_field(name = "😈 Misc", value = f'```/user - посмотреть информацию о пользователе.\n/avatar - посмотреть аватарку пользователя.\n/messages - посмотреть свои сообщения.\n/voice - посмотреть сколько просидели в голосовом канале.```', inline = False)
      embed.add_field(name = "📞 Music", value = f'```/play - Запустить музыку\n/stop - Выключить музыку\n/volume - Установить громкость музыки\n/playinfo - Узнать какая сейчас музыка проигрывает\n/playlist - Список очереди\n/skip - Пропустить музыку\n/pause - Поставить на паузу музыку\n/resume - Возобновить музыку```', inline = False)
      embed.add_field(name = "🏆 Взаимодействия", value = f'```/поцелуй - поцеловать пользователя.\n/обнять - обнять пользователя.\n/обнимашки - обнять пользователя.\n/подмигнуть - подмигнуть пользователю.\n/погладить - погладить пользователя.\n/cat - Рандомное фото с котиками.```', inline = False)
      embed.add_field(name = "😈 Quest", value = f"```/quest - Посмотреть ежедневные задание.```", inline = False)
      embed.set_footer(text = 'Support Team by Jokos')
      await ctx.send(embed=embed)

    @commands.command()
    async def инфоящик(self, ctx):
      if not ctx.guild.id == 822900692104249425:
            return

      embed = discord.Embed(title = 'Nelegal | Ящик пандоры', colour = 0x09F2C8)
      embed.add_field(name = "💰 Инфо", value = f'```1. Вам может выпасть от 1 до 4 коина.\n2. Своя личная роль\n3. Любой скин на сервере.```', inline = False)
      embed.set_footer(text = 'Support Team by Jokos')
      await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def thelp(self, ctx):
      if not ctx.guild.id == 822900692104249425:
            return
            
      embed = discord.Embed(title = 'Nelegal | Commands Panel', colour = 0x09F2C8)
      embed.add_field(name = "💰 Кмд", value = f'```/createglobal - Создать глобальный квест\n/createquest - Создать ежедневное задание```', inline = False)
      embed.set_footer(text = 'Support Team by Jokos')
      await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def delquest(self, ctx):
      for i in quest.find():
        quest.delete_one({"_id": i["_id"]})
        questik.update_one({"guild": ctx.guild.id}, {"$set": {"zakritq": 1}})
        await ctx.send(f"+")
    

    @ящик.error
    async def ящик_error(self, ctx, error):
      if isinstance(error, commands.CommandNotFound):
        return await ctx.send(embed=discord.Embed(description=f'{ctx.author.name}, Команда не найдена!', ))
      elif isinstance(error, commands.MissingPermissions):
        return await ctx.send(embed=discord.Embed(description=f'{ctx.author.name}, У бота недостаточно прав!\n'
        f'Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций.', ))
      elif isinstance(error, commands.MissingPermissions) or isinstance(error, discord.Forbidden):
        return await ctx.send(embed=discord.Embed(description=f'{ctx.author.name}, У вас недостаточно прав!', ))
      elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=discord.Embed(description=f'{ctx.author.name}, Воу, Воу, Не надо так быстро прописывать команды.\n'
        f'Подожди {error.retry_after:.2f} секунд и сможешь написать команду ещё раз.'))

def setup(client):
    client.add_cog(econom(client))