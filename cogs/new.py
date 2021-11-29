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

class new(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('new conn')
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id == 843462502884704306:
            msg = ctx.content.lower()
            if ctx.author.bot:
                if ctx.author.id == 822908821813985350:
                    return
                else:
                    return
            else:
                channel2 = self.client.get_channel(843462502884704306)

                await channel2.send(f'+')

                channel = self.client.get_channel(822938428147499038)

                embed1 = discord.Embed(title = f"Central district || nelegals", description=f'{ctx.content}', colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
                embed1.set_footer(text = 'Support Team by Jokos', icon_url = self.client.user.avatar_url)
                await channel.send(f'@everyone', embed=embed1)

def setup(client):
    client.add_cog(new(client))