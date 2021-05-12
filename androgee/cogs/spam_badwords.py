from discord.ext import commands
from androgee.init import MOD_ROLE_ID, MOD_ROLE_NAME, swear_list, COMMAND_PREFIX


def isbad(word: str) -> bool:
    if word in swear_list:
        return True
    return False


class BadWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"We is logged in as {self.bot.user}")

    @commands.has_any_role(MOD_ROLE_NAME, int(MOD_ROLE_ID))
    @commands.command(name="unlock")
    async def unlock(self, ctx) -> None:
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
    async def on_message(self, ctx) -> None:
        if await self.last_message(ctx, ctx.content):
            await ctx.channel.send(
                f"<@&{MOD_ROLE_ID}> Hey admins there is a person spamming messages, I'm locking the channel"
            )
            await ctx.author.send(
                "admins have been alerted to your shenanigans. You should probably stop unless getting banned is your game plan"
            )
            overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
            role = ctx.guild.get_role(int(MOD_ROLE_ID))
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
        else:  # we don't need to run this if the spam check
            for word in ctx.content.split(" "):
                if self.isbad(word.lower().replace("~", "").replace("`", "")):
                    # sometime this throws a 400 and says it can not dm the user. in testing  it does send a dm
                    await ctx.author.send(
                        f"please stop using slurs, we don't tolarate them in any manner the following message triggered this message:\n{ctx.content}"
                    )
                    await ctx.delete()
                    break

    async def last_message(self, ctx, og_meesage) -> bool:
        messages = await ctx.channel.history(
            limit=5
        ).flatten()  # anything more then 5 increases wait time pretty heavily
        count = 1
        for message in messages:
            if message.author.bot:
                pass  # if the bot said it, it don't matter
            elif message.content == og_meesage:
                count += 1
        if count > 5:
            return True
        return False

    def isbad(self, word: str) -> bool:
        if word in swear_list:
            return True
        return False
