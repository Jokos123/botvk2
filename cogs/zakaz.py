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
zakaz = db["zakaz"]
role = db["role"]




def is_owner(ctx):
    return ctx.message.author.id == 576480513716649984

def add(member: discord.Member, arg):
  if role.count_documents({"id": member.id}) == 0:
    role.insert_one({"guild": 477547500232769536, "id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "repa": 0, "rols": 0, "derols": 0, "dezaprols": 0})
    role.update_one({"id": member.id}, {"$set": {arg: 1}})
  else:
    role.update_one({"id": member.id}, {"$set": {arg: role.find_one({"id": member.id})[arg] + 1}})

class zakaz(commands.Cog):
    """zakaz Cog."""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('zakaz conn')
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        cluster = MongoClient("mongodb+srv://rodinadb:nbsGK02riO3PkygA@cluster0.cdvgc.mongodb.net/rodina?retryWrites=true&w=majority")
        db = cluster["rodina"]
        zakaz = db["zakaz"]
        if ctx.channel.id == 823948904545779722:
            czakaz = discord.utils.get(ctx.guild.categories, id= 823948617319448576)
            prov = discord.utils.get(
                ctx.guild.channels, name=f'заказ-{ctx.author.id}')

            msg = ctx.content.lower()
            if ctx.author.bot:
                if ctx.author.id == 822908821813985350:
                    return
                else:
                    await ctx.delete()
                    return
            else:
                await ctx.delete()

                if prov in czakaz.channels:
                    return await ctx.channel.send(
                        f'`[ERROR]` {ctx.author.mention}, `Вы уже имеете активный заказ! Для перехода в него нажмите на его название -` <#{prov.id}>.',
                        delete_after=10)

                channel = await ctx.guild.create_text_channel(
                    f'Заказ {ctx.author.mention}',
                    
                    overwrites=None,
                    category=czakaz,
                    reason='Создание нового заказа.')
                await ctx.channel.send(
                    embed=discord.Embed(
                        description=
                        f'**{ctx.author.mention}, Для вас создан канал - <#{channel.id}>!**',
                        colour=discord.Colour.blue()),
                    delete_after=20)
                await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True)
                embed1 = discord.Embed(description=f'''**Обращение к поддержке Discord**''', colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
                embed1.add_field(name='Отправитель\n', value=f'**Пользователь:** `{ctx.author.display_name}`', inline=False)
                embed1.add_field(name='Суть обращения', value=f'{ctx.content}', inline=False)
                embed1.set_footer(text = 'Support Team by Jokos', icon_url = self.client.user.avatar_url)
                await channel.send(f'{ctx.author.mention} для команды поддержки <@&822903299828744212>\n', embed=embed1)
                zakaz.update_one({"proverka": "1"}, {"$set": {"last_name": ctx.author.display_name}})
                message_id = 823954130975588402
                chans = self.client.get_channel(823948904545779722)
                message = await chans.fetch_message(message_id)
                emb23 = discord.Embed(description = f'**«Нелегальная Лавка» - это официальный магазин Центрального Округа, в котором вы можете приобрести такие товары, как эксклюзивные скины, автомобили, аксессуары, игровые предметы и различные плюшки на нашем официальном дискорд сервере.**\n\n```Для заказа услуг либо отправления заказа продавцам напишите любое слово в данный текстовый канал, после чего в созданном текстовом канале вы сможете задать свой заказ.```', colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
                emb23.set_author(name='Central district || nelegals', icon_url= 'https://i.imgur.com/s5CvtOT.png')
                emb23.add_field(name = 'Последний заказ от:', value=f'`{ctx.author.display_name}`', inline = False)
                emb23.set_footer(text=f'Support Team by Jokos', icon_url = self.client.user.avatar_url)
                await message.edit(embed=emb23)

def setup(client):
    client.add_cog(zakaz(client))