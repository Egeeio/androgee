from discord.ext import commands
from androgee.init import mod_role_name, mod_role_id, swear_list, COMMAND_PREFIX


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

    @commands.command(name="source")
    async def source(self, ctx):
        message = (
            f"{ctx.author.mention} the source is at https://github.com/Egeeio/androgee"
        )
        await ctx.send(message)

    @commands.has_any_role(mod_role_name, int(mod_role_id))
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
