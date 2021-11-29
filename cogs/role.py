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
rolef = db["role"]

def add(member: discord.Member, arg):
  if rolef.count_documents({"id": member.id}) == 0:
    rolef.insert_one({"guild": 822900692104249425, "id": member.id, "rols": 0, "derols": 0, "dezaprols": 0})
    rolef.update_one({"id": member.id}, {"$set": {arg: 1}})
  else:
    rolef.update_one({"id": member.id}, {"$set": {arg: rolef.find_one({"id": member.id})[arg] + 1}})


global uje 
uje = []

global meid
meid = []

global RCH
RCH = ['ФМ', 'фм', 'Фм', 'фМ', 'FM', 'fm', 'Fantomas', 'fm', 'СТ', 'ст', 'Ст', 'сТ', 'st', 'ST', 'СБ', 'сб', 'Сб', 'сБ', 'SB', 'sb', 'ЧК', 'чк', 'Чк', 'чК', 'HK','hk', 'КМ', 'км', 'кМ', 'Км', 'KM', 'km', 'УМ', 'ум', 'Ум', 'уМ', 'YM', 'ym', 'РМ', 'рм', 'RM', 'rm']

class role(commands.Cog):
    """ROLE Cog."""

    def __init__(self, client: commands.Bot):
        self.client = client 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Role State by jokos - Запущен')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == f'<@!{self.client.user.id}>' or  ctx.content == f'<@{self.client.user.id}>':
            await ctx.channel.send(f'{ctx.author.mention},', embed = discord.Embed(title = 'Основная информация', description = f'**1**', colour = 0xFB9E14), delete_after = 20)
  
        global uje 
        role_registr = ['роль', 'роли', 'дайте роль', 'хочу роль', 'роль дайте', 'выдайте роль', '-роль', 'Роль', 'Роли', 'Дайте роль', 'Хочу роль', 'Роль дайте', 'Выдайте роль', '-Роль', '!Роль', '!роль' ]
        nick_registr = ['ФМ', 'фм', 'Фм', 'фМ', 'FM', 'fm', 'Fantomas', 'fm', 'СТ', 'ст', 'Ст', 'сТ', 'st', 'ST', 'СБ', 'сб', 'Сб', 'сБ', 'SB', 'sb', 'ЧК', 'чк', 'Чк', 'чК', 'HK','hk', 'КМ', 'км', 'кМ', 'Км', 'KM', 'km', 'УМ', 'ум', 'Ум', 'уМ', 'YM', 'ym', 'РМ', 'рм', 'RM', 'rm']
        opg = ['ФМ', 'фм', 'Фм', 'фМ', 'FM', 'fm', 'Fantomas', 'fm', 'СТ', 'ст', 'Ст', 'сТ', 'st', 'ST', 'СБ', 'сб', 'Сб', 'сБ', 'SB', 'sb', 'ЧК', 'чк', 'Чк', 'чК', 'HK','hk', 'КМ', 'км', 'кМ', 'Км', 'KM', 'km', 'УМ', 'ум', 'Ум', 'уМ', 'YM', 'ym', 'РМ', 'рм', 'RM', 'rm']

        ROLES = {
            'ФМ': 822905587665731655,
            'Фм': 822905587665731655,
            'фм': 822905587665731655,
            'фМ': 822905587665731655,
            'FM': 822905587665731655,
            'fm': 822905587665731655,
            'Fantomas': 822905587665731655,
            'fm': 822905587665731655,
            'Groove': 822905587665731655,
            'groove': 822905587665731655,
            'GROOVE': 822905587665731655,
            'СТ': 822905586408357899,
            'ст': 822905586408357899,
            'Ст': 822905586408357899,
            'сТ': 822905586408357899,
            'st': 822905586408357899,
            'ST': 822905586408357899,
            'Aztec': 822905586408357899,
            'aztec': 822905586408357899,
            'AZTEC': 822905586408357899,
            'СБ': 822905591772086312,
            'сб': 822905591772086312,
            'Сб': 822905591772086312,
            'сБ': 822905591772086312,
            'SB': 822905591772086312,
            'sb': 822905591772086312,
            'Vagos': 822905591772086312,
            'vagos': 822905591772086312,
            'VAGOS': 822905591772086312,
            'ЧК': 822905590937681921,
            'чк': 822905590937681921,
            'Чк': 822905590937681921,
            'чК': 822905590937681921,
            'HK': 822905590937681921,
            'hk': 822905590937681921,
            'ballas': 822905590937681921,
            'Ballas': 822905590937681921,
            'BALLAS': 822905590937681921,
            'РМ': 822905593785352212,
            'рм': 822905593785352212,
            'RM': 822905593785352212,
            'rm': 822905593785352212,
            'rM': 822905593785352212,
            'Rm': 822905593785352212,
            'Рм': 822905593785352212,
            'рМ': 822905593785352212,
            'КМ': 822905593001410640,
            'Км': 822905593001410640,
            'KM': 822905593001410640,
            'Km': 822905593001410640,
            'км': 822905593001410640,
            'kM': 822905593001410640,
            'УМ': 822905593710903326,
            'Ум': 822905593710903326,
            'уМ': 822905593710903326,
            'Um': 822905593710903326,
            'uM': 822905593710903326,
            'UM': 822905593710903326,
        }

        if not ctx.author.bot:
            if not ctx.guild: # Проверка что это ЛС
                for i in rolef.find({"user_id": ctx.author.id}):
                    if not i["zaproschannel"] == 0:
                        if ctx.attachments == []:
                            return
                        else:
                          channel = self.client.get_channel(822921305933873233)
                          guild = self.client.get_guild(822900692104249425)
                          member = discord.utils.get(guild.members, id = i["user_id"])
                          embed = discord.Embed(description = '`Discord >> Проверка на валидность никнейма`', colour = discord.Colour.blue())
                          embed.set_footer(text = f'Support Team by Jokos')
                          embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {ctx.author.mention}', inline = True)
                          embed.add_field(name = 'Никнейм', value = f'`Ник:` {ctx.author.display_name}', inline = True)
                          embed.add_field(name = 'Роль для выдачи', value = f'`Роль для выдачи`: {discord.utils.get(guild.roles, id = i["role_id"]).mention}', inline = False)
                          embed.add_field(name = 'Отправлено с канала', value = f'{self.client.get_channel(i["zaproschannel"]).mention}', inline = False)
                          embed.add_field(name = 'Действия', value = '`[✔️] - выдать роль.`\n`[❌] - отказать.`\n`[❔] - Запросить скрин-шот статистики повторно`\n`[✏️] - Установить пользователю Nick_Name`\n\n ⇓ ⇓Снизу статистика игрока ⇓ ⇓ ')
                          embed.set_image(url = ctx.attachments[0].url)
                          message = await channel.send(f'`[UPDATE]` `Пользователь {member.display_name}`({member.mention}) `отправил доказательства на получение роли!`', embed = embed)
                          await ctx.author.send('`[SUCCESFULL] Ваши доказательства отправлены в необходимый канал`')
                          rolef.update_one({"user_id": ctx.author.id}, {"$set": {"message_id":  message.id}})
                          await message.add_reaction('✔️')
                          await message.add_reaction('❌')
                          await message.add_reaction('❔')
                          await message.add_reaction('✏️')
                            
            elif not ctx.guild.id == 822900692104249425:
                return
            
        msg = ctx.content.lower()
        if msg in role_registr:
            ak = ctx.author.display_name.replace('[', '')
            ak1 = ak.replace(']', '')
            ak2 = ak1.split()
            if not ctx.channel.id == 822906090403921930:
                await ctx.delete()
                return await ctx.channel.send(embed = discord.Embed(description = f'**❌ {ctx.author.mention}, получать роли нужно только в канале <#822906090403921930>!**', colour = discord.Colour.blue()), delete_after = 5)

            ath = re.findall(r'\w*', ctx.author.display_name)
            for z in ath:
                if z in nick_registr:
                    break

            if z in nick_registr:
                if rolef.count_documents({"user_id": ctx.author.id}) == 1 and rolef.find_one({"user_id": ctx.author.id})["is_active"] == 1:
                    await ctx.add_reaction('🕐')
                    return await ctx.channel.send(f'{ctx.author.mention}, `Вы уже отправили своё заявление на получение роли, дождитесь его одобрения.`', delete_after = 5)

                channel = self.client.get_channel(822921305933873233)
                nad_role = discord.utils.get(ctx.guild.roles, id=ROLES[z])
                
                embed = discord.Embed(description = '`Discord >> Проверка на валидность никнейма`', colour = discord.Colour.blue(), timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = f'Support Team by Jokos', icon_url = ctx.guild.icon_url)
                embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {ctx.author.mention}', inline = True)
                embed.add_field(name = 'Никнейм', value = f'`Ник:` {ctx.author.display_name}', inline = True)
                embed.add_field(name = 'Роль для выдачи', value = f'`Роль для выдачи`: {nad_role.mention}', inline = False)
                embed.add_field(name = 'Отправлено с канала', value = f'{ctx.channel.mention}', inline = False)
                embed.add_field(name = 'Действия', value = '`[✔️] - выдать роль.`\n`[❌] - отказать.`\n`[❔] - Запросить скрин-шот статистики`\n`[✏️] - Установить пользователю Nick_Name`')

                if nad_role in ctx.author.roles:
                    await ctx.channel.send(f'{ctx.author.mention}, `у вас уже есть роль` {nad_role.mention}', delete_after = 5)
                    return await ctx.add_reaction('❌')

                await ctx.add_reaction('📨')

                message = await channel.send(embed = embed)
                await message.add_reaction('✔️')

                rolef.insert_one({"user_id": ctx.author.id, "role_id": nad_role.id, "message_id": message.id, "is_active": 1, "channel": ctx.channel.id, "leader": 0, "pruf": 0, "zaproschannel": 0, "prufid": 0, "zapid": 0, "kuda": channel.id, "setn": 0})
                await message.add_reaction('❌')
                await message.add_reaction('❔')
                await message.add_reaction('✏️')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global meid
        guild = self.client.get_guild(payload.guild_id)
        if guild == None:
            return
        
        role_checkers = [650239061285404672, 479048866704916540, 479049028705976340, 479049200768647169, 479185785510166567, 479198132211548161, 479198415578988554, 479198488563810315]
        chal = [822903894736633896, 822921305933873233]

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
            if channel.id == 822903894736633896:
              if memb.top_role.position < self.client.get_guild(payload.guild_id).get_role(477785202899288084).position:
                return
            
                
            if rolef.count_documents({"message_id": message.id}) == 0:
                await message.delete()
                return await channel.send(f'`[BUGTRAKER]` {memb.mention} `удалил багнутый запрос`')

            for i in rolef.find({"message_id": message.id}):
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(i["user_id"])  
                chan = self.client.get_channel(i["channel"])
                if member == None:
                    await message.delete()
                    await channel.send(f'`[BUGTRAKER]` {memb.mention} `запрос был багнутым, мне пришлось его удалить. ID Удалённого запроса: {i["user_id"]}`')
                    return rolef.delete_one({"message_id": message.id})
                if i["is_active"] == 1 or i["is_active"] == 2:
                    if emoji == '❔':
                        if i["pruf"] == 0:
                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `запрашивает у вас статистику игрового аккаунта, отправьте в личные сообщения боту скриншот [/stats + /time]`')
                            serf = await channel.send(f'`[PRUF]` {memb.mention} `запросил доказательства от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.update_one({"message_id": message.id}, {"$set": {"pruf": 1, "zaproschannel": channel.id, "zapid": serf.id}})
                            await member.send(f'{member.mention}, `модератор {memb.display_name} запрашивает у вас статистику игрового аккаунта, отправьте в личные сообщения боту скриншот [/stats + /time]`')
                            await message.delete()
                        else:
                            await channel.send(f'`[ERROR]` {memb.mention}, `статистику запросил другой модератор.`', delete_after = 5)
                    if emoji == '✏️':
                        if i["setn"] == 0:
                            rolef.update_one({"message_id": message.id}, {"$set": {"setn": 1}})
                            mes1 = await channel.send(f'{memb.mention}, `введите ник-нейм который хотите установить в чат.`')
                            def check(m):
                                return m.author.id == memb.id and m.channel.id == channel.id
                            try:
                                msg = await self.client.wait_for('message', timeout= 120.0, check = check)
                            except Exception:
                                await channel.send(f'{memb.mention}, `Время установки НикНэйма вышло`', delete_after = 5)
                                await mes1.delete()
                                try:
                                    await self.client.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                                    rolef.update_one({"message_id": message.id}, {"$set": {"setn": 0}})
                                except:
                                    pass
                            if len(list(msg.content)) > 32:
                                await channel.send(f'{memb.mention}, `Вы превысили допустимый лимит символов: {len(list(msg.content))}/32`', delete_after = 5)
                                await msg.delete()
                                await mes1.delete()
                                try:
                                    await self.client.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                                    rolef.update_one({"message_id": message.id}, {"$set": {"setn": 0}})
                                except:
                                    pass
                            else:
                                await member.edit(nick = msg.content)
                                await channel.send(f'`[INFO]` `Модератор` {memb.mention} `установил пользователю` {member.mention} `ник: {msg.content}`')
                                await member.send(f'{member.mention}, `модератор {memb.display_name} установил Вам следующий ник: {msg.content}`\n`Если вы считаете, что данный ник является недопустимым, напишите жалобу на форум:` https://forum.robo-humster.ru/')
                                await msg.delete()
                                await mes1.delete()
                                await self.client.http.remove_reaction(channel.id, message.id, emoji, memb.id)
                                rolef.update_one({"message_id": message.id}, {"$set": {"setn": 0}})
                        else:
                            await channel.send(f'`[ERROR]` {memb.mention}, `данному пользователю уже меняют ник`', delete_after = 5)
                        
                    elif emoji == '✔️':                          
                        if i["is_active"] == 1:              
                            for role in member.roles:
                                if role.id in role_checkers:
                                    await member.remove_roles(role)
                                else:
                                    pass
                            
                            if not i["prufid"] == 0:
                                msg = await channel.fetch_message(i["prufid"])
                                await msg.delete()

                            if not i["zapid"] == 0:
                                msg1 = await channel.fetch_message(i["zapid"])
                                await msg1.delete()

                            await member.add_roles(self.client.get_guild(payload.guild_id).get_role(i["role_id"]))
                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `одобрил ваш запрос на выдачу роли.`\n`Роль` <@&{i["role_id"]}> `была выдана!`')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})
                            add(memb, "rols")
                            return await message.delete()
                        elif i["is_active"] == 2:
                            membs = self.client.get_guild(payload.guild_id).get_member(i["leader"])
                            if membs.id == memb.id:
                                return
                            
                            await message.delete()
                            rol = self.client.get_guild(payload.guild_id).get_role(i["role_id"])
                            await chan.send(f'`[ACCEPT]` {memb.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {member.display_name}, с ID: {member.id}`')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил снятие роли ({rol.name}) от` {membs.mention}, `пользователю {member.display_name}, с ID: {member.id}`')
                            await member.remove_roles(rol)
                            rolef.delete_one({"message_id": message.id})
                            add(memb, "derols")
                    elif emoji == '❌':
                        if i["is_active"] == 1:
                            await message.delete()
                            if not i["prufid"] == 0:
                                msg = await channel.fetch_message(i["prufid"])
                                await msg.delete()

                            if not i["zapid"] == 0:
                                msg1 = await channel.fetch_message(i["zapid"])
                                await msg1.delete()

                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на выдачу роли.`\n`Ваш ник при отправке: {member.display_name}`\n`Установите ник на: [Фракция Ранг/10] Имя_Фамилия`')
                            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})
                        elif i["is_active"] == 2:
                            member = self.client.get_guild(payload.guild_id).get_member(i["leader"])
                            await message.delete()
                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос на снятие роли у пользователя` {member.mention}')
                            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i["user_id"]}`')
                            rolef.delete_one({"message_id": message.id})

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        global RCH

        SNRL = {
            'ФМ': 822905587665731655,
            'Фм': 822905587665731655,
            'фм': 822905587665731655,
            'фМ': 822905587665731655,
            'FM': 822905587665731655,
            'fm': 822905587665731655,
            'Fantomas': 822905587665731655,
            'fm': 822905587665731655,
            'Groove': 822905587665731655,
            'groove': 822905587665731655,
            'GROOVE': 822905587665731655,
            'СТ': 822905586408357899,
            'ст': 822905586408357899,
            'Ст': 822905586408357899,
            'сТ': 822905586408357899,
            'st': 822905586408357899,
            'ST': 822905586408357899,
            'Aztec': 822905586408357899,
            'aztec': 822905586408357899,
            'AZTEC': 822905586408357899,
            'СБ': 822905591772086312,
            'сб': 822905591772086312,
            'Сб': 822905591772086312,
            'сБ': 822905591772086312,
            'SB': 822905591772086312,
            'sb': 822905591772086312,
            'Vagos': 822905591772086312,
            'vagos': 822905591772086312,
            'VAGOS': 822905591772086312,
            'ЧК': 822905590937681921,
            'чк': 822905590937681921,
            'Чк': 822905590937681921,
            'чК': 822905590937681921,
            'HK': 822905590937681921,
            'hk': 822905590937681921,
            'ballas': 822905590937681921,
            'Ballas': 822905590937681921,
            'BALLAS': 822905590937681921,
            'РМ': 822905593785352212,
            'рм': 822905593785352212,
            'RM': 822905593785352212,
            'rm': 822905593785352212,
            'rM': 822905593785352212,
            'Rm': 822905593785352212,
            'Рм': 822905593785352212,
            'рМ': 822905593785352212,
            'КМ': 822905593001410640,
            'Км': 822905593001410640,
            'KM': 822905593001410640,
            'Km': 822905593001410640,
            'км': 822905593001410640,
            'kM': 822905593001410640,
            'УМ': 822905593710903326,
            'Ум': 822905593710903326,
            'уМ': 822905593710903326,
            'Um': 822905593710903326,
            'uM': 822905593710903326,
            'UM': 822905593710903326,
        }

        if not before.guild.id == 822900692104249425:
            return

        if before.display_name == after.display_name:
            return

        else:
            if discord.utils.get(before.guild.roles, id = 720958695764131850) in before.roles:
                return
            elif discord.utils.get(before.guild.roles, id = 727112273704779797) in before.roles:
                return
            elif discord.utils.get(before.guild.roles, id = 727112347105099877) in before.roles:
                return
            else:
                ath = re.findall(r'\w*', before.display_name)
                ath2 = re.findall(r'\w*', after.display_name)
                if ath[1] == ath2[1]:
                  return
                if ath[1] in RCH:
                    channel = self.client.get_channel(822906090403921930)
                    sf_roles = discord.utils.get(before.guild.roles, id=SNRL[ath[1]])
                    if not sf_roles in before.roles:
                        return

                    await before.remove_roles(sf_roles)
                    embed = discord.Embed(description = f'**{after.mention}, `вы изменили свой ник.`\n`Роль` <@&{SNRL[ath[1]]}> `снята`**', color=discord.Colour.blue())
                    embed.set_footer(text = f'Support Team by Jokos')
                    embed.set_thumbnail(url = 'https://images-ext-2.discordapp.net/external/bnUk9lweCuYaZT2wcaEVZllXV4GaWfVfwmU9WGI-5-I/https/images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                    await channel.send(embed = embed)

def setup(client):
    client.add_cog(role(client))