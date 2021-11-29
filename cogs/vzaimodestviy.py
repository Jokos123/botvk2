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


class vzaimo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()

    async def on_ready(self):
        print('Vzaimo connect')

    @commands.command()
    async def погладить(self, ctx, member: discord.Member = None):
        response = requests.get('https://nekos.life/api/pat')
        json_data = json.loads(response.text)
        embed = discord.Embed(color = 0x09F2C8, description = f'{member.mention} вас погладил(-а) {ctx.author.mention}')
        embed.set_image(url = json_data['url'])
        await ctx.send(embed = embed)

    @commands.command()
    async def подмигнуть(self, ctx, member: discord.Member = None):
        response = requests.get('https://some-random-api.ml/animu/wink')
        json_data = json.loads(response.text)
        embed = discord.Embed(color = 0x09F2C8, description = f'{member.mention} вам подмигнул(-а) {ctx.author.mention}')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed)

    @commands.command(aliases = ['обнимашки'])
    async def обнять(self, ctx, member: discord.Member = None):
        response = requests.get('https://nekos.life/api/hug')
        json_data = json.loads(response.text)
        embed = discord.Embed(color = 0x09F2C8, description = f'{member.mention} вас обнял(-а) {ctx.author.mention}')
        embed.set_image(url = json_data['url'])
        await ctx.send(embed = embed)

    @commands.command()
    async def поцелуй(self, ctx, member: discord.Member = None):
        response = requests.get('https://nekos.life/api/kiss')
        json_data = json.loads(response.text)
        embed = discord.Embed(color = 0x09F2C8, description = f'{member.mention} вас поцеловал(-а) {ctx.author.mention}')
        embed.set_image(url = json_data['url'])
        await ctx.send(embed = embed)

    @commands.command(aliases = ['киска', 'котик', 'котяра', 'кися', 'кот', 'котейка', 'котя', 'киса'])
    async def cat(self, ctx, member: discord.Member = None):
        response = requests.get('https://some-random-api.ml/img/cat')
        json_data = json.loads(response.text)
        embed = discord.Embed(color = 0x09F2C8, title = f'Котик :)')
        embed.set_image(url = json_data['link'])
        await ctx.send(embed = embed)

def setup(client):
	client.add_cog(vzaimo(client))