import os
import re
import asyncio
from typing import Optional

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Moderation commands for servers."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="kick", help="Kick a user from the server.")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided") -> None:
        if member == ctx.author:
            await ctx.send("You cannot kick yourself.")
            return

        if member.top_role >= ctx.author.top_role and ctx.guild.owner_id != ctx.author.id:
            await ctx.send("You cannot kick someone with an equal or higher role than you.")
            return

        await member.kick(reason=reason)
        await ctx.send(f"✅ Kicked {member.mention} for: {reason}")

    @commands.command(name="ban", help="Ban a user from the server.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = "No reason provided") -> None:
        if member == ctx.author:
            await ctx.send("You cannot ban yourself.")
            return

        if member.top_role >= ctx.author.top_role and ctx.guild.owner_id != ctx.author.id:
            await ctx.send("You cannot ban someone with an equal or higher role than you.")
            return

        await member.ban(reason=reason)
        await ctx.send(f"✅ Banned {member.mention} for: {reason}")

    @commands.command(name="unban", help="Unban a user from the server.")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def unban(self, ctx: commands.Context, user_id: int) -> None:
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.NotFound:
            await ctx.send("No user found with that ID.")
            return

        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user.mention}.")

    @commands.command(name="clear", help="Delete a number of recent messages from this channel.")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def clear(self, ctx: commands.Context, amount: int = 10) -> None:
        if amount < 1 or amount > 100:
            await ctx.send("Please provide a number between 1 and 100.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.", delete_after=3)

    @commands.command(name="mute", help="Mute a user by assigning a muted role. Usage: !mute @user 10m")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def mute(self, ctx: commands.Context, member: discord.Member, duration: str = "") -> None:
        muted_role = await self._get_or_create_muted_role(ctx.guild)

        if muted_role in member.roles:
            await ctx.send(f"{member.mention} is already muted.")
            return

        await member.add_roles(muted_role, reason="Muted via bot command")

        for channel in ctx.guild.text_channels:
            await channel.set_permissions(muted_role, send_messages=False, read_message_history=True, read_messages=True)

        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(muted_role, speak=False, connect=False)

        if duration:
            seconds = self._parse_duration(duration)
            if seconds is None:
                await ctx.send("⚠️ Invalid duration. Use formats like `10m`, `1h`, or `1d`.")
                return

            await ctx.send(f"✅ Muted {member.mention} for {duration}.")
            await asyncio.sleep(seconds)

            if muted_role in member.roles:
                await member.remove_roles(muted_role, reason="Mute duration expired")
                await ctx.send(f"🔓 {member.mention} has been unmuted after {duration}.")
        else:
            await ctx.send(f"✅ Muted {member.mention} indefinitely.")

    def _parse_duration(self, duration: str) -> Optional[int]:
        match = re.fullmatch(r"(\d+)([smhd])", duration.strip().lower())
        if not match:
            return None

        value = int(match.group(1))
        unit = match.group(2)

        if unit == "s":
            return value
        if unit == "m":
            return value * 60
        if unit == "h":
            return value * 60 * 60
        if unit == "d":
            return value * 60 * 60 * 24
        return None

    @commands.command(name="unmute", help="Unmute a user by removing the muted role.")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    async def unmute(self, ctx: commands.Context, member: discord.Member) -> None:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role is None:
            await ctx.send("There is no muted role in this server.")
            return

        if muted_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted.")
            return

        await member.remove_roles(muted_role, reason="Unmuted via bot command")
        await ctx.send(f"✅ Unmuted {member.mention}.")

    async def _get_or_create_muted_role(self, guild: discord.Guild) -> discord.Role:
        muted_role = discord.utils.get(guild.roles, name="Muted")
        if muted_role is None:
            muted_role = await guild.create_role(name="Muted", reason="Needed for mute command")
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await channel.set_permissions(muted_role, send_messages=False, read_message_history=True, read_messages=True)
                elif isinstance(channel, discord.VoiceChannel):
                    await channel.set_permissions(muted_role, speak=False, connect=False)
        return muted_role


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
