from main import convert
import discord
from discord.ext import commands
import asyncio
import random
from ruamel.yaml import YAML

yaml = YAML()

with open("./config.yml", "r", encoding="utf-8") as file:
    config = yaml.load(file)

class reroll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_role(config['giveaway_role'])
    async def giveaway(self, ctx):
        timeout = config["setup_timeout"]
        embedq1 = discord.Embed(title=":gift: | МАСТЕР УСТАНОВКИ",
                                description=f"Добро пожаловать в мастер установки. Ответьте на следующие вопросы в рамках ``{timeout}`` Секунды!")
        embedq1.add_field(name=":star: | Вопрос 1",
                          value="Где мы должны провести раздачу?\n\n **Пример**: ``#General``")
        embedq2 = discord.Embed(title=":gift: | МАСТЕР УСТАНОВКИ",
                                description="Большой! Перейдем к следующему вопросу.")
        embedq2.add_field(name=":star: | Question 2",
                          value="Как долго это должно длиться? ``<s|m|h|d|w>``\n\n **Пример**:\n ``1d``")
        embedq3 = discord.Embed(title=":gift: | МАСТЕР УСТАНОВКИ",
                                description="Потрясающие. Вы дошли до последнего вопроса!")
        embedq3.add_field(name=":star: | Question 2",
                          value="Какой приз получит победитель?\n\n **Пример**:\n ``NITRO``")

        questions = [embedq1,
                     embedq2,
                     embedq3]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(embed=i)

            try:
                msg = await self.client.wait_for('message', timeout=config['setup_timeout'], check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(title=":gift: **Мастер настройки розыгрыша**",
                                      description=":x: Вы не ответили вовремя!")
                await ctx.send(embed=embed)
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2: -1])
        except:
            embed = discord.Embed(title=":gift: **Мастер настройки розыгрыша**",
                                  description=":x: Вы неправильно указали канал!")
            await ctx.send(embed=embed)
            return

        channel = self.client.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            embed = discord.Embed(title=":gift: **Мастер настройки розыгрыша**",
                                  description=":x: Вы не установили правильную единицу времени!")
            await ctx.send(embed=embed)
            return
        elif time == -2:
            embed = discord.Embed(title=":gift: **Мастер настройки розыгрыша**",
                                  description=":x: Единица времени ** ДОЛЖНА ** быть целым числом")
            await ctx.send(embed=embed)
            return
        prize = answers[2]

        embed = discord.Embed(title=":gift: **Мастер настройки розыгрыша**",
                              description="Ладно, все готово. Розыгрыш начнется!")
        embed.add_field(name="Размещенный канал:", value=f"{channel.mention}")
        embed.add_field(name="Время:", value=f"{answers[1]}")
        embed.add_field(name="Приз:", value=prize)
        await ctx.send(embed=embed)
        print(
            f"Началась новая розыгрыш! Хостинг: {ctx.author.mention} | Размещенный канал: {channel.mention} | Время: {answers[1]} | Приз: {prize}")
        print("------")
        embed = discord.Embed(title=f":gift: **РАЗДАЧА ЗА: {prize}**",
                              description=f"Реагировать с {config['react_emoji']} Участвовать!")
        embed.add_field(name="Длится:", value=answers[1])
        embed.add_field(name=f"Хостинг:", value=ctx.author.mention)
        msg = await channel.send(embed=embed)

        await msg.add_reaction(config['react_emoji'])
        await asyncio.sleep(time)

        new_msg = await channel.fetch_message(msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)
        if config['ping_winner_message'] == True:
            await channel.send(f":tada: Поздравления! {winner.mention} победил: **{prize}**!")
            print(f"Новый Победитель! Пользователь: {winner.mention} | Приз: {prize}")
            print("------")

        embed2 = discord.Embed(title=f":gift: **РАЗДАЧА ЗА: {prize}**",
                               description=f":trophy: **Победитель:** {winner.mention}")
        embed2.set_footer(text="Розыгрыш закончился")
        await msg.edit(embed=embed2)



def setup(client):
    client.add_cog(reroll(client))