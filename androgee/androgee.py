import random
import logging
import discord
from discord.ext import typed_commands as commands  # type:ignore
from pathlib import (
    Path,
)
from androgee.cogs.spam_badwords import BadWords
from androgee.init import COMMAND_PREFIX, BOT_TOKEN, MOD_ROLE_ID


logging.basicConfig(level=logging.WARNING)
bot: commands.Bot = commands.Bot(command_prefix=COMMAND_PREFIX)
media_folder = Path(
    __file__, "../media"
).resolve()  # Root of the media folder from file.


# Super quick and easy random selection, partial credit to citrusMarmelade
def get_image(ctx):
    images = list(media_folder.glob(f"{ctx.command}/*"))
    return discord.File(random.choice(images))


@bot.command(name="spray", aliases=["spritzered"])
async def spray(self, ctx, member: discord.Member = None):
    if MOD_ROLE_ID in [y.id for y in ctx.author.roles] and member is not None:
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
    if MOD_ROLE_ID in [y.id for y in ctx.author.roles] and member is not None:
        await member.send("Hey just a heads up you where to rowdy, tone it down")
        await ctx.channel.purge(10)
    image = get_image(ctx)
    if member is None:
        await ctx.send(file=image)
    else:
        message = f"{member.mention} was bonked by {ctx.author.mention}"
        await ctx.send(message, file=image)


@bot.command(name="source")
async def source(self, ctx):
    message = (
        f"{ctx.author.mention} the source is at https://github.com/Egeeio/androgee"
    )
    await ctx.send(message)


def start():
    bot.add_cog(BadWords(bot))
    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    start()
