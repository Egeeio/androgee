import os
import random
import logging
import asyncio
import discord
from discord.ext import commands


logging.basicConfig(level=logging.WARNING)
bot = commands.Bot(command_prefix=os.environ["DISCORD_PREFIX"])
mod_role_id = os.environ["mod_role_id"]


@bot.event
async def on_ready():
    print(f"We is logged in as {bot.user}")


@bot.command(name="spray")
async def spray(ctx, member: discord.Member = None):
    image = get_image(ctx)
    if member == None:
        await ctx.send(file=image)
    else:
        if mod_role_id in [y.id for y in ctx.author.roles]:
            await member.edit(mute=True)
            message = f"{member.mention} was sprayed by {ctx.message.author.mention}"
            await ctx.send(message, file=image)
            await asyncio.sleep(10)
            await member.edit(mute=False)
        else:
            message = f"{member.mention} was sprayed by {ctx.message.author.mention}"
            await ctx.send(message, file=image)


@bot.command(name="bonk")
async def spray(ctx, member: discord.Member = None):
    image = get_image(ctx)
    if member == None:
        await ctx.send(file=image)
    else:
        if mod_role_id in [y.id for y in ctx.author.roles]:
            await member.edit(mute=True)
            message = f"{member.mention} was bonked by {ctx.message.author.mention}"
            await ctx.send(message, file=image)
            await asyncio.sleep(10)
            await member.edit(mute=False)
        else:
            message = f"{member.mention} was bonked by {ctx.message.author.mention}"
            await ctx.send(message, file=image)


@bot.command(name="source")
async def source(ctx):
    message = (
        f"{ctx.author.mention} the source is at https://github.com/Egeeio/androgees"
    )
    await ctx.send(message)


def get_image(ctx):
    images = []
    files = os.walk(f"{os.path.dirname(__file__)}/media/{ctx.command}")
    for root, dirs, files in files:
        for name in files:
            images.append(f"{root}/{name}")
    loc = random.randint(0, len(images) - 1)
    img = discord.File(images[loc])
    return img


def start():
    bot.run(os.environ["DISCORD_TOKEN"])
