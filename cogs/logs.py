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


class logs(commands.Cog):
    """LOGS Cog."""

    def __init__(self, client):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logs conn')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):

        if member.guild == None:
            return

        if not member.guild.id == 822900692104249425:
            return

        if after.channel == None:
            if not member.guild.id == 822900692104249425:
                return

            if not before.channel == None:
                if member.bot:
                    return
                channel = self.client.get_channel(823347864138285128)
                e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) вышел из голосового канала 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Выход из канала')
                e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
                e.add_field(name = "ID Участника", value = f"**{member.id}**")
                e.set_footer(text = f'Support Team by Jokos')
                return await channel.send(embed = e)

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

            if member.bot:
                return
            channel = self.client.get_channel(823347864138285128)
            e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) перешёл в другой голосовой канал 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
            e.set_author(name = f'Журнал аудита | Переход в канал')
            e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
            e.add_field(name = "Предыдущий канал", value = f"**{before.channel.name}({before.channel.mention})**")
            e.add_field(name = "ID Участника", value = f"**{member.id}**")
            e.set_footer(text = f'Support Team by Jokos')
            return await channel.send(embed = e)

        if not after.channel == None:
            if before.channel == None:
                if member.bot:
                    return
                channel = self.client.get_channel(823347864138285128)
                e = discord.Embed(description = f'**Пользователь {member.display_name}({member.mention}) зашёл в голосовой канал 🔊**', colour = member.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Вход в канал')
                e.add_field(name = "Действующий канал", value = f"**{after.channel.name}({after.channel.mention})**")
                e.add_field(name = "ID Участника", value = f"**{member.id}**")
                e.set_footer(text = f'Support Team by Jokos')
                return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        rguild = self.client.get_guild(822900692104249425)

        if not before in rguild.members:
            return

        if before.avatar_url == after.avatar_url:
            return

        channel = self.client.get_channel(823348165604147200)
        e = discord.Embed(description = f'**Пользователь {before.display_name}({before.mention}) изменил свой аватар!**', colour = before.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Измнение пользователя')
        e.add_field(name = "Новая аватарка", value = f"**[Кликабельная ссылка]({before.avatar_url})**")
        e.add_field(name = "ID Участника", value = f"**{before.id}**")
        e.set_image(url = after.avatar_url)
        e.set_thumbnail(url = before.avatar_url)
        e.set_footer(text = f'Support Team by Jokos')
        return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return

        if not message.guild.id == 822900692104249425:
            return

        channel = self.client.get_channel(823348479853199411)
        e = discord.Embed(colour = message.author.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Удаление сообщения')
        e.add_field(name = "Удалённое сообщение", value = f"```{message.content}```")
        e.add_field(name = "Автор", value = f"**{message.author.display_name}({message.author.mention})**")
        e.add_field(name = "Канал", value = f"**{message.channel.mention}**")
        e.add_field(name = "ID Сообщения", value = f"**{message.id}**")
        e.set_footer(text = f'Support Team by Jokos')
        return await channel.send(embed = e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.guild == None:
            return

        if not before.guild.id == 822900692104249425:
            return
        
        if before.content == after.content:
            return

        channel = self.client.get_channel(823348479853199411)
        e = discord.Embed(description = f'**[Сообщение]({before.jump_url}) было изменено.**', colour = before.author.color, timestamp = datetime.datetime.utcnow())
        e.set_author(name = f'Журнал аудита | Изменение сообщения')
        e.add_field(name = "Старое содержимое", value = f"```{before.content}```")
        e.add_field(name = "Новое соодержиое", value = f"```{after.content}```")
        e.add_field(name = "Автор", value = f"**{before.author.display_name}({before.author.mention})**")
        e.add_field(name = "Канал", value = f"**{before.channel.mention}**")
        e.add_field(name = "ID Сообщения", value = f"**{before.id}**")
        e.set_footer(text = f'Support Team by Jokos')
        return await channel.send(embed = e)

    @commands.Cog.listener()
    @commands.has_permissions(administrator = True)
    async def ping(self, ctx):
        await ctx.channel.purge(limit = 1)
        await ctx.send(embed = discord.Embed(
            title = '**🏓Понг**',
            description = f'**Задержка составила: {self.client.ws.latency * 1000:.0f} мс**'
        ))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild == None:
            return


        admins = [822955865106939955, 822904136521089024, 822904165319311360]

        roles = [822967144400420886, 822967146057433128, 822967144651161610, 822967142684295198, 823231716168302633, 823160375796170763, 822951975896481812, 822905586042929172, 822904167340703756, 822967141917523988, 822950540249923586, 822907382295822386, 822904737774829598]

        #mj = [733685870510735392, 394147378841518080, 583772223643451392, 376390578235113475, 583764095585484811, 325608396319358989, 739470499901603880]

        if not len(before.roles) == len(after.roles):
            
            role = [ ]
            if len(before.roles) > len(after.roles):
                for i in before.roles:
                    if not i in after.roles:
                        async for entry in before.guild.audit_logs(limit = 2, action = discord.AuditLogAction.member_role_update):
                            zapret = [822967144400420886, 822967146057433128, 822967144651161610, 822967142684295198, 823231716168302633, 823160375796170763, 822951975896481812, 822905586042929172, 822904167340703756, 822967141917523988, 822950540249923586, 822907382295822386, 822904737774829598]
                            if before.guild.id == 822900692104249425:
                                if entry.user.top_role.id in admins:
                                    if i.id in zapret:
                                        if entry.user.bot:
                                            return
                                        channel = self.client.get_channel(823349941190787082)
                                        e = discord.Embed(description = f'**Администратор {entry.user} забрал у пользователя {after} запрещённую роль({i.mention}), бот вернул её автоматически.**', Colour = before.colour, timestamp = datetime.datetime.utcnow())
                                        e.set_author(name = f'Журнал аудита | Снятие запрещённой роли', icon_url = self.client.user.avatar_url)
                                        e.set_footer(text = f'Support Team by Jokos', icon_url = self.client.user.avatar_url)
                                        await channel.send(embed = e)
                                        return await after.add_roles(i)                                   
                                else:
                                    return
                    if not i.id == before.guild.default_role.id:
                        role.append(f'➖ Была убрана роль {i.name}(<@&{i.id}>)\n')
            elif len(before.roles) < len(after.roles):
                    for i in after.roles:
                        if not i in before.roles:
                            if not i.id == before.guild.default_role.id:
                                role.append(f'➕ Была добавлена роль {i.name}(<@&{i.id}>)\n')
                            if i.id in roles:
                                async for entry in before.guild.audit_logs(limit = 2, action = discord.AuditLogAction.member_role_update):
                                    if before.guild.id == 325607843547840522:
                                        f = 0
                                        for b in entry.user.roles:
                                            if not entry.user.top_role.id in mj:
                                                if b.id in admins:
                                                    f += 1
                                                    await entry.user.remove_roles(b)
                                        if f >= 1:
                                            return await after.remove_roles(i)
                                        else:
                                            return
                                    elif before.guild.id == 822900692104249425:
                                        if entry.user.top_role.id in admins:
                                            if entry.user.bot:
                                                return
                                            channel = self.client.get_channel(823349941190787082)
                                            e = discord.Embed(description = f'**Пользователю {after} была выдана запрещённая роль({i.mention}) администратором {entry.user}, бот убрал её автоматически.**', Colour = before.colour, timestamp = datetime.datetime.utcnow())
                                            e.set_author(name = f'Журнал аудита | Выдача запрещённой роли', icon_url = self.client.user.avatar_url)
                                            e.set_footer(text = f'Support Team by Jokos', icon_url = self.client.user.avatar_url)
                                            await channel.send(embed = e)
                                            return await after.remove_roles(i)
                                        else:
                                            return

        if before.guild.id == 822900692104249425:
            if not before.display_name == after.display_name:
                channel = self.client.get_channel(823350125169475635)
                e = discord.Embed(description = f'**Пользователь {before.name}({after.mention}) изменил NickName**', colour = before.color, timestamp = datetime.datetime.utcnow())
                e.set_author(name = f'Журнал аудита | Изменение NickName участника')
                e.add_field(name = "Действующее имя", value = f"**{after.display_name}({after.mention})**")
                e.add_field(name = "Предыдущее имя", value = f"**{before.display_name}({before.mention})**")
                e.add_field(name = "ID Участника", value = f"**{after.id}**")
                e.set_footer(text = f'Support Team by Jokos')
                return await channel.send(embed = e)
            else:
                return

def setup(client):
    client.add_cog(logs(client))
