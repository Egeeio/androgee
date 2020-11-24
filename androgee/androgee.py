import os
import random
import logging
import discord
from discord.ext import commands


logging.basicConfig(level=logging.WARNING)
bot = commands.Bot(command_prefix=os.environ['DISCORD_PREFIX'])

@bot.event
async def on_ready():
    print('We is logged in as {0.user}'.format(bot))


@bot.command(name="spray")
async def spray(ctx):
    image = get_image(ctx)
    await ctx.send(file=image)


@bot.command(name="bonk")
async def spray(ctx):
    image = get_image(ctx)
    await ctx.send(file=image)


def get_image(ctx):
    images = []
    files = os.walk(f"{os.path.dirname(__file__)}/media/{ctx.command}")
    for root, dirs, files in files:
        for name in files:
            images.append(f"{root}/{name}")
    img = discord.File(random.choice(images))
    return img

def start():
    bot.run(os.environ['DISCORD_TOKEN'])
