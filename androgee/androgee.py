import os
import sys
import random
import logging
import requests
import discord
from discord.ext import commands
from pathlib import (
    Path,
)

global swear_list
swear_list = requests.get(
    "https://raw.githubusercontent.com/dariusk/wordfilter/master/lib/badwords.json"
).json()
swear_list.append(
    "trap"
)  # the word trap was requested by someone on the server maybe we should have a seprate git repo for the wordlist?

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


def isbad(word: str) -> bool:
    if word.lower() in swear_list:
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
            message = f"{member.mention} was bonked by {ctx.author.mention}"
            await ctx.send(message, file=image)

    @commands.command(name="source")
    async def source(self, ctx):
        message = (
            f"{ctx.author.mention} the source is at https://github.com/Egeeio/androgee"
        )
        await ctx.send(message)

    @commands.command(name="unlock")
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages:
            await ctx.send("this channel is already unlocked 🔓")
        else:
            overwrite.send_messages = True
            await ctx.channel.set_permissions(
                ctx.guild.default_role, overwrite=overwrite
            )
            await ctx.send("this channel is now unlocked 🔓")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        check = await self.last_message(ctx, ctx.content)
        if check:
            await ctx.channel.send(
                f"<@&{mod_role_id}> Hey admins there is a person spamming messages, I'm locking the channel"
            )
            await ctx.author.send(
                "admins have been alerted to your shenanigans. You should probably stop unless getting banned is your game plan"
            )
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            role = ctx.guild.get_role(int(mod_role_id))
            print(role)
            overwrites_owner = ctx.channel.overwrites_for(role)
            await ctx.channel.send(
                f"🔒 Channel is locked down. Use `{COMMAND_PREFIX}unlock` to unlock."
            )
            overwrite.send_messages = False
            overwrites_owner.send_messages = True
            await ctx.channel.set_permissions(
                ctx.guild.default_role, overwrite=overwrite
            )
            await ctx.channel.set_permissions(
                role,
                overwrite=overwrites_owner,
            )
        badwords = False
        for word in ctx.content.split(" "):
            check = isbad(word.replace("~", "").replace("`", ""))
            if check:
                badwords = True
        if badwords:
            await ctx.author.send(
                f"please stop using slurs, we don't tolarate them in any manner the following mess triggered this message:\n{ctx.content}"
            )

            await ctx.delete()

    async def last_message(self, ctx, og_meesage):
        messages = await ctx.channel.history(limit=10).flatten()
        count = 1
        for message in messages:
            if message.author.bot:
                pass  # if the bot said it, it don't matter
            elif message.content == og_meesage:
                count += 1
        if count > 5:
            return True
        return False


def start():
    bot.add_cog(Androgee(bot))
    bot.run(BOT_TOKEN)
