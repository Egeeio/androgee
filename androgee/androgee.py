import os
import sys
import random
import logging
import json
import discord
from discord.ext import commands
from pathlib import (
    Path,
)

with open("configs/badwords.json", "r") as f:
    global swear_list
    swear_list = json.loads(f.read())["banned"]

# I think it'd be better if we check if environment
# variables are present before doing anything else.
if os.path.exists(".env"):
    from dotenv import load_dotenv

    load_dotenv()
try:
    mod_role_id = os.environ["mod_role_id"]
    mod_role_name = os.environ["mod_role_name"]
    COMMAND_PREFIX = os.environ["DISCORD_PREFIX"]
    BOT_TOKEN = os.environ["DISCORD_TOKEN"]
except KeyError as e:
    print(f"The {e} environment variable is missing! Androgee cannot run!")
    sys.exit(1)
logging.basicConfig(level=logging.WARNING)
bot = commands.Bot(command_prefix=COMMAND_PREFIX)
media_folder = Path(
    __file__, "../media"
).resolve()  # Root of the media folder from file.


# Super quick and easy random selection, partial credit to citrusMarmelade
def get_image(ctx):
    images = list(media_folder.glob(f"{ctx.command}/*"))
    return discord.File(random.choice(images))


def isbad(word) -> bool:
    if word in swear_list:
        return True
    return False


class Androgee(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We is logged in as {self.bot.user}")

    @commands.command(name="spray", aliases=["spritzered"])
    async def spray(self, ctx, member: discord.Member = None):
        if mod_role_id in [y.id for y in ctx.author.roles] and member is not None:
            await member.send("Hey just a heads up you where to rowdy, tone it down")
            await ctx.channel.clear(10)
        image = get_image(ctx)
        if member is None:
            await ctx.send(file=image)
        else:
            message = f"{member.mention} was sprirzered by {ctx.message.author.mention}"
            await ctx.send(message, file=image)

    @commands.command(name="bonk")
    async def bonk(self, ctx, member: discord.Member = None):
        if mod_role_id in [y.id for y in ctx.author.roles] and member is not None:
            await member.send("Hey just a heads up you where to rowdy, tone it down")
            await ctx.channel.purge(10)
        image = get_image(ctx)
        if member is None:
            await ctx.send(file=image)
        else:
            message = f"{member.mention} was bonked by {ctx.message.author.mention}"
            await ctx.send(message, file=image)

        @commands.command(name="source")
        async def source(self, ctx):
            message = f"{ctx.author.mention} the source is at https://github.com/Egeeio/androgee"
            await ctx.send(message)

    @commands.command(name="reload")
    @commands.has_any_role(mod_role_name, mod_role_id)
    async def reload(self, ctx):
        with open("configs/badwords.json", "r") as f:
            global swear_list
            swear_list = json.loads(f.read())["banned"]
        await ctx.send("updated the banned word list")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        check = await self.last_message(ctx, ctx.content)
        if check:
            await ctx.channel.send(f"<@!{mod_role_id}> spamer")
            await ctx.author.send(
                "admins have been alerted to your shenanigans. You should probably stop unless getting banned is your game plan"
            )
        badwords = False
        for word in ctx.content.split(" "):
            check = isbad(word)
            if check:
                badwords = True
        if badwords:
            await ctx.delete()
            await ctx.author.send(
                "please stop using slurs, we don't tolarate them in any manner"
            )

    async def last_message(self, ctx, og_meesage):
        messages = await ctx.channel.history(limit=10).flatten()
        count = 1
        for message in messages:
            if message.content == og_meesage:
                count += 1
        if count > 5:
            return True
        return False


def start():
    bot.add_cog(Androgee(bot))
    bot.run(BOT_TOKEN)
