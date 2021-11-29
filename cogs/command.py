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


class comm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()

    async def on_ready(self):
        print('Comm connect')

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
    	member = ctx.author if not member else member
    	roles = [ ]
    	if not len(member.roles) == 1:
    		f = 0
    		for i in member.roles:
    			if not i.id == ctx.guild.default_role.id:
    				f += 1
    				s = len(member.roles) - f
    				roles.append(f'`{s}.` <@&{i.id}>\n')
    	embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
    	embed.set_author(name = f"🍀 Аватарка пользователя - {member}")
    	embed.set_image(url = member.avatar_url)
    	embed.set_footer(text = f'Support Team by Jokos')
    	await ctx.send(embed = embed)

def setup(client):
	client.add_cog(comm(client))