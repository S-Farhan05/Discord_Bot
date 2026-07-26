import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is missing. Please set it in the .env file.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
    activity=discord.Activity(type=discord.ActivityType.playing, name="!help | AI powered"),
)


@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("The bot is ready to serve.")


@bot.command(name="help", help="Show all available bot commands.")
async def help_command(ctx: commands.Context) -> None:
    embed = discord.Embed(title="Bot Commands", color=discord.Color.blurple())
    embed.add_field(name="Basic", value="`!ping` `!serverinfo` `!userinfo @user` `!poll [question]`", inline=False)
    embed.add_field(name="AI", value="`!ask [question]`", inline=False)
    embed.add_field(name="Moderation", value="`!clear [number]` `!kick @user [reason]` `!ban @user [reason]` `!mute @user [duration]` `!unmute @user` `!unban [user_id]`", inline=False)
    embed.set_footer(text="Use the commands above in any text channel.")
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception) -> None:
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Missing argument: {error.param.name}")
        return

    if isinstance(error, commands.BadArgument):
        await ctx.send(f"⚠️ Invalid argument: {error}")
        return

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️ You do not have permission to use that command.")
        return

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("⚠️ I do not have the required permissions to perform that action.")
        return

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Slow down! Please try again in {error.retry_after:.2f} seconds.")
        return

    await ctx.send(f"⚠️ An unexpected error occurred: {error}")


async def load_cogs() -> None:
 
    for extension in ("cogs.moderation", "cogs.fun", "cogs.ai"):
        await bot.load_extension(extension)


if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(TOKEN)
