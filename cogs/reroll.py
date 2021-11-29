import discord
from discord.ext import commands
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
    async def reroll(self, ctx, channel: discord.TextChannel, id_: int):
        try:
            new_msg = await channel.fetch_message(id_)
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))
            winner = random.choice(users)
            await ctx.channel.send(f":tada: Новый победитель:{winner.mention}!")
        except:
            prefix = config['prefix']
            await ctx.send(
                f":x: Была допущена ошибка! \n`{prefix}reroll <Канал, на котором размещена раздача> <messageID сообщения раздачи>` ")

def setup(client):
    client.add_cog(reroll(client))