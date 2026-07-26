import discord
from discord.ext import commands


class Fun(commands.Cog):
    """Fun and utility commands for the server."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ping", help="Check the bot latency.")
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def ping(self, ctx: commands.Context) -> None:
        latency_ms = round(self.bot.latency * 1000, 2)
        await ctx.send(f"🏓 Pong! {latency_ms}ms")

    @commands.command(name="serverinfo", help="Show information about the current server.")
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def serverinfo(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title=ctx.guild.name, color=discord.Color.blue())
        embed.add_field(name="Members", value=str(ctx.guild.member_count), inline=True)
        embed.add_field(name="Created", value=ctx.guild.created_at.strftime("%Y-%m-%d"), inline=True)

        if getattr(ctx.guild, "icon", None):
            embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed)

    @commands.command(name="userinfo", help="Show information about a user.")
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def userinfo(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        target = member or ctx.author
        roles = [role.mention for role in target.roles if role.name != "@everyone"]
        embed = discord.Embed(title=f"User Info - {target.display_name}", color=discord.Color.green())
        embed.add_field(name="Username", value=target.name, inline=True)
        embed.add_field(name="ID", value=str(target.id), inline=True)
        embed.add_field(name="Joined", value=target.joined_at.strftime("%Y-%m-%d") if target.joined_at else "Unknown", inline=True)
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="poll", help="Create a simple yes/no poll.")
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def poll(self, ctx: commands.Context, *, question: str) -> None:
        if not question.strip():
            await ctx.send("Please provide a question for the poll.")
            return

        message = await ctx.send(f"📊 Poll: {question}")
        for emoji in ("✅", "❌"):
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        general_channel = discord.utils.get(member.guild.text_channels, name="general")
        if general_channel is None:
            general_channel = next((channel for channel in member.guild.text_channels if channel.permissions_for(member.guild.me).send_messages), None)

        if general_channel is not None:
            await general_channel.send(
                f"Welcome {member.mention} to {member.guild.name}! Please read the rules and enjoy your stay."
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
