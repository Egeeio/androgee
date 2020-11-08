import os
import discord
from discord.ext import commands

client = commands.Bot("$")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# command = $hello
@client.command()
async def hello(ctx):
    await ctx.send("Hello!")


# command = $nuzzle
@client.command()
async def nuzzle(ctx):
    await ctx.send(f"*nuzzles* {ctx.author.name}")


# help is a inbuilt function it will raise an error when used
@client.command()
async def h(ctx):
    message = """
    **$hello** get Hello back
**$nuzzle** get nuzzled
**$h**   get this message
    """
    await ctx.send(message)


"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
"""
token = os.environ["DISCORD_TOKEN"]
client.run(token)
