import random
import logging
import discord
from discord.ext import commands
from pathlib import (
    Path,
)
from androgee.cogs.spam_badwords import Androgee
from androgee.init import COMMAND_PREFIX, BOT_TOKEN, mod_role_id


logging.basicConfig(level=logging.WARNING)
bot = commands.Bot(command_prefix=COMMAND_PREFIX)
media_folder = Path(
    __file__, "../media"
).resolve()  # Root of the media folder from file.


# Super quick and easy random selection, partial credit to citrusMarmelade
def get_image(ctx):
    images = list(media_folder.glob(f"{ctx.command}/*"))
    return discord.File(random.choice(images))


@bot.command(name="spray", aliases=["spritzered"])
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


@bot.command(name="bonk")
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


def start():
    bot.add_cog(Androgee(bot))
    bot.run(BOT_TOKEN)
