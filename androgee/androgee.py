import os
import sys
import random
import logging
import discord
from discord.ext import commands
from pathlib import Path # This makes working with files and searching through them a piece of cake

# I think it'd be better if we check if environment
# variables are present before doing anything else.
try:
    mod_role_id = os.environ["mod_role_id"]
    mod_role_name = os.environ["mod_role_name"]
    COMMAND_PREFIX = os.environ["DISCORD_PREFIX"]
    BOT_TOKEN = os.environ["DISCORD_TOKEN"]
except KeyError as e:
    print(f'The {e} environment variable is missing! Androgee cannot run!')
    sys.exit(1)

logging.basicConfig(level=logging.WARNING)
bot = commands.Bot(command_prefix=COMMAND_PREFIX)
media_folder=Path(__file__, '../media').resolve() # Root of the media folder from file.

@bot.event
async def on_ready():
    print(f"We is logged in as {bot.user}")


@bot.command(name="spray", aliases=["spritzered"])
@commands.has_any_role(mod_role_name, mod_role_id)
async def spray(ctx, member: discord.Member = None):
    try:
        image = get_image(ctx)
        if member == None:
            await ctx.send(file=image)
        else:
            ctx.send(f"!tempmute {member.mention} 300 being too rowdy")
            message = f"{member.mention} was sprirzered by {ctx.message.author.mention}"
            await ctx.send(message, file=image)
    except commands.MissingRole:
        image = get_image(ctx)
        if member == None:
            await ctx.send(file=image)
        else:
            message = f"{member.mention} was sprirzered by {ctx.message.author.mention}"
            await ctx.send(message, file=image)


@bot.command(name="bonk")
@commands.has_any_role(mod_role_name, mod_role_id)
async def spray(ctx, member: discord.Member = None):
    try:
        image = get_image(ctx)
        if member == None:
            await ctx.send(file=image)
        else:
            ctx.send(f"!tempmute {member.mention} 300 being too rowdy")
            message = f"{member.mention} was bonked by {ctx.message.author.mention}"
            await ctx.send(message, file=image)
    except commands.MissingRole:
        image = get_image(ctx)
        if member == None:
            await ctx.send(file=image)
        else:
            message = f"{member.mention} was bonked by {ctx.message.author.mention}"
            await ctx.send(message, file=image)


@bot.command(name="source")
async def source(ctx):
    message = (
        f"{ctx.author.mention} the source is at https://github.com/Egeeio/androgee"
    )
    await ctx.send(message)


# Super quick and easy random selection. Partial credit goes to citrusMarmelade.
def get_image(ctx):
    images = list(media_folder.glob(f'{ctx.command}/*'))
    return discord.File(random.choice(images)) 


def start():
    bot.run(BOT_TOKEN)
