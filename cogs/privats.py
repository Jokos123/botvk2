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


conn = sqlite3.connect("cogs/database.db")
cursor = conn.cursor()

global s
s = 0

class privats(commands.Cog):
    """privats Cog."""

    def __init__(self, client: commands.Bot):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Voice Privat')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        global s

        if not member.guild.id == 822900692104249425:
            return

        if after.channel == None:
            return

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

        if not after.channel == None:
            if after.channel.id == 822906398270029876:
                if s == 1:
                    s = 0
                    return await member.move_to(None)
                s = 1
                mainCategory = discord.utils.get(member.guild.categories, id=822906431081676840)
                ath = re.split(r'\W+', str(member))
                channel2 = await member.guild.create_voice_channel(name=f"📞 ┃ {member.display_name} | {ath[-1]}",category=mainCategory)
                await channel2.set_permissions(member, view_channel = True, connect = True, manage_channels = True, manage_permissions = False, speak = True, move_members = False, use_voice_activation = True, priority_speaker = True, mute_members = False, deafen_members = False)
                vch = self.client.get_channel(822906398270029876)
                if not vch.members:
                    s = 0
                    return await channel2.delete()
                else:
                    if member in vch.members:
                        try:
                            await member.move_to(channel2)
                        except:
                            pass
                        if not channel2.members:
                            s = 0
                            return await channel2.delete()
                    else:
                        s = 0
                        return await channel2.delete()
                
                for i in mainCategory.channels:
                    if isinstance(i, discord.VoiceChannel):
                        if not i.id == 822906398270029876:
                            if len(i.members) == 0:
                                try:
                                    await i.delete()
                                except:
                                    pass
                s = 0
                def check(a,b,c):
                    return len(channel2.members) == 0
                await self.client.wait_for('voice_state_update', check=check)
                return await channel2.delete()

def setup(client):
    client.add_cog(privats(client))