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
import aiofiles
import requests
import jishaku
import wikipedia
import traceback
import sys
from pymongo import MongoClient
from ruamel.yaml import YAML
from dotenv import load_dotenv


load_dotenv()
yaml = YAML()

with open("./config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)


client = commands.Bot(command_prefix = '/',intents = discord.Intents().all())
client.load_extension('jishaku')
client.remove_command('help')
guild = discord.Guild
        
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

token = os.environ.get('BOT_TOKEN')

client.run(str(token))