import os
import logging
from discord.ext import commands


logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name="spray")
async def spray(ctx):
    await jail(ctx)


@bot.command(name="bonk")
async def spray(ctx):
    jail(ctx)

async def jail(ctx):
    await ctx.send(f"bonking {ctx.author.name}")

token = os.environ['DISCORD_TOKEN']
bot.run(token)
