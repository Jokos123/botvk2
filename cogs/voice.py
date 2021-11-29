import discord
from discord.ext import commands
import json
import asyncio
import sqlite3
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rodinadb:nbsGK02riO3PkygA@cluster0.cdvgc.mongodb.net/rodina?retryWrites=true&w=majority")
db = cluster["rodina"]
voise = db["mess"]

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.prev = []

    @commands.command(aliases = ["voice", "гч"])
    async def __voice(self, ctx):
      if voise.count_documents({"id": ctx.author.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'Вы просидели в голосовом канале: `0`', colour = 0x09F2C8))
      
      else:
        seconds = voise.find_one({"id": ctx.author.id})["vsv"]
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return await ctx.send(embed = discord.Embed(title = 'Central district || nelegals', description = f'Вы просидели в голосовом канале: `{hours} час. {minutes} мин. {seconds} cек`', colour = 0x09F2C8))

      

      
        
      
        
        
        
        
        
        
        
        
      
        
  
        
 
def setup(client):
    client.add_cog(Voice(client))