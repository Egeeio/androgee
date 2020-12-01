import os
import random
import logging
import discord
from discord.utils import get
from discord.ext import commands


logging.basicConfig(level=logging.WARNING)
bot = commands.Bot(command_prefix=os.environ["DISCORD_PREFIX"])
global black_list
black_list = []
with open("black_list.txt", "r") as f:
    for line in f.readlines():
        black_list.append(line.strip())
    f.close()


@bot.event
async def on_ready():
    print("We is logged in as {0.user}".format(bot))


@bot.command(name="spray")
async def spray(ctx, member: discord.Member = None):
    image = get_image(ctx)
    if member == None:
        await ctx.send(file=image)
    else:
        message = f"{member.mention} was sprayed by {ctx.message.author.mention}"
        await ctx.send(message, file=image)


@bot.command(name="bonk")
async def spray(ctx, member: discord.Member = None):
    image = get_image(ctx)
    if member == None:
        await ctx.send(file=image)
    else:
        message = f"{member.mention} was bonked by {ctx.message.author.mention}"
        await ctx.send(message, file=image)


@bot.command("role")
async def role(ctx, command, *, role=None):
    if command == "regen":
        global black_list
        black_list = []
        with open("black_list.txt", "r") as f:
            for line in f.readlines():
                black_list.append(line.strip())
        f.close()
    elif command == "list":
        roles = await ctx.guild.fetch_roles()
        role_list = ""
        for role in roles:
            if role.name in black_list:
                pass
            else:
                role_list = role_list + role.name + "\n"
        await ctx.send(f"these are the avalible roles:\n{role_list}")
    elif command == "add":
        if role == None:
            await ctx.send("must specify role.")
        else:
            if role in black_list:
                await ctx.send("only a admin can assign this role")
            else:
                role_to_give = get(ctx.guild.roles, name=role)
                await ctx.author.add_roles(role_to_give)


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
