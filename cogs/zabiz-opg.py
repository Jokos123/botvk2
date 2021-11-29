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
import urllib
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rodinadb:nbsGK02riO3PkygA@cluster0.cdvgc.mongodb.net/rodina?retryWrites=true&w=majority")
db = cluster["rodina"]
zabiv = db["zabiv"]
nel = db["nel"]

def addbt(member: discord.Member, arg : int):
  if nel.count_documents({"id": member.id}) == 0:
    nel.insert_one({"guild": member.guild.id, "id": member.id, "nel": arg})
    return arg
  else:
    bal = arg + nel.find_one({"id": member.id})["nel"]
    nel.update_one({"id": member.id}, {"$set": {"nel": bal}})
    return bal
    
def add(member: discord.Member, arg):
  if zabiv.count_documents({"id": member.id}) == 0:
    zabiv.insert_one({"guild": 822900692104249425, "id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "repa": 0, "rols": 0, "derols": 0, "dezaprols": 0})
    zabiv.update_one({"id": member.id}, {"$set": {arg: 1}})
  else:
    zabiv.update_one({"id": member.id}, {"$set": {arg: zabiv.find_one({"id": member.id})[arg] + 1}})


global uje 
uje = []

global meid
meid = []

global RCH
RCH = ['ФМ', 'СТ', 'СБ', 'ЧК', 'КМ', 'УМ', 'РМ']

class role(commands.Cog):
    """ROLE Cog."""

    def __init__(self, client: commands.Bot):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Zabiv OPG State by jokos - Запущен')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        global uje 
        nick_registr = ['ФМ', 'фм', 'Фм', 'фМ', 'FM', 'fm', 'Fantomas', 'fm', 'СТ', 'ст', 'Ст', 'сТ', 'st', 'ST', 'СБ', 'сб', 'Сб', 'сБ', 'SB', 'sb', 'ЧК', 'чк', 'Чк', 'чК', 'HK','hk', 'КМ', 'км', 'кМ', 'Км', 'KM', 'km', 'УМ', 'ум', 'Ум', 'уМ', 'YM', 'ym', 'РМ', 'рм', 'RM', 'rm']
        opg = ['ФМ', 'фм', 'Фм', 'фМ', 'FM', 'fm', 'Fantomas', 'fm', 'СТ', 'ст', 'Ст', 'сТ', 'st', 'ST', 'СБ', 'сб', 'Сб', 'сБ', 'SB', 'sb', 'ЧК', 'чк', 'Чк', 'чК', 'HK','hk', 'КМ', 'км', 'кМ', 'Км', 'KM', 'km', 'УМ', 'ум', 'Ум', 'уМ', 'YM', 'ym', 'РМ', 'рм', 'RM', 'rm']

        msg = ctx.content.lower()

        if ctx.channel.id == 822954386115395584:
            ak = ctx.author.display_name.replace('[', '')
            ak1 = ak.replace(']', '')
            ak2 = ak1.split()

            msg = ctx.content.lower()

            ath = re.findall(r'\w*', ctx.author.display_name)
            for z in ath:
                if z in nick_registr:
                    break

            if z in nick_registr:

                channel = self.client.get_channel(823170062318960640)
                
                embed = discord.Embed(description = None, colour = discord.Colour.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = f'Support Team by Jokos', icon_url = ctx.guild.icon_url)
                embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {ctx.author.mention}', inline = True)
                embed.add_field(name = 'Никнейм', value = f'`Ник:` {ctx.author.display_name}', inline = True)
                embed.add_field(name = 'Отправлено с канала', value = f'{ctx.channel.mention}', inline = False)
                embed.add_field(name = 'Сообщения', value = f'{ctx.content}', inline = False)
                embed.add_field(name = 'Действия', value = '`[✔️] - Одобрить.`\n`[❌] - Отказать.`')

                await ctx.add_reaction('📨')

                message = await channel.send('@everyone', embed = embed)
                await message.add_reaction('✔️')

                name = ctx.content

                zabiv.insert_one({"user_id": ctx.author.id, "message_id": message.id, "content": name, "is_active": 1, "channel": ctx.channel.id, "leader": 0, "pruf": 0, "zaproschannel": 0, "prufid": 0, "zapid": 0, "kuda": channel.id, "setn": 0})
                await message.add_reaction('❌')     


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload): 
        chal = [823170062318960640]

        chakfd = self.client.get_channel(822905342413373440)

        user = self.client.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            channel = self.client.get_channel(payload.channel_id)
            if not channel.id in chal:
                return
            message = await channel.fetch_message(payload.message_id)
            memb = payload.member
            emoji = str(payload.emoji)
            
                
            if zabiv.count_documents({"message_id": message.id}) == 0:
                await message.delete()
                return await channel.send(f'`[BUGTRAKER]` {memb.mention} `удалил багнутый запрос`')

            for i in zabiv.find({"message_id": message.id}):
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(i["user_id"])  
                chan = self.client.get_channel(i["channel"])
                if member == None:
                    await message.delete()
                    await channel.send(f'`[BUGTRAKER]` {memb.mention} `запрос был багнутым, мне пришлось его удалить. ID Удалённого запроса: {i["user_id"]}`')
                    return zabiv.delete_one({"message_id": message.id})
                if i["is_active"] == 1:
                    if emoji == '✔️':                          
                        if i["is_active"] == 1:              

                            await chan.send(f'{member.mention}, `следящий` {memb.mention} `одобрил ваш запрос.`')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от` {member.mention}')

                            embed = discord.Embed(description = f'{member.mention}**:**\n```{zabiv.find_one({"message_id": message.id})["content"]}```\n{memb.mention} **- одобрено**', colour = discord.Colour.blue(), timestamp = datetime.datetime.utcnow())
                            embed.set_author(name='Central district || nelegals', icon_url= 'https://i.imgur.com/s5CvtOT.png')
                            embed.set_footer(text = f'Одобрил: {memb.name}', icon_url = memb.avatar_url)
                            embed.set_thumbnail(url = member.avatar_url)
                            await chakfd.send('@everyone', embed = embed)
                            return await message.delete()
                            st = 1
                            addbt(member, st)
                    if emoji == '❌':
                        if i["is_active"] == 1:

                            await chan.send(f'{member.mention}, `следящий` {memb.mention} `отказ ваш запрос.`')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `отказал запрос от` {member.mention}')
                            return await message.delete()

def setup(client):
    client.add_cog(role(client))