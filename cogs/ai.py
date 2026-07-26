import os
from typing import Optional

from discord.ext import commands
from openai import OpenAI


class AI(commands.Cog):
    """AI-powered chat commands using a Groq-compatible API endpoint."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="ask", help="Ask the bot a question using AI.")
    @commands.cooldown(rate=2, per=20, type=commands.BucketType.user)
    async def ask(self, ctx: commands.Context, *, question: str) -> None:
        if not question.strip():
            await ctx.send("Please provide a question to ask.")
            return

        async with ctx.typing():
            answer = self._get_ai_response(question)

        await ctx.send(answer)

    def _get_ai_response(self, question: str) -> str:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return self._fallback_response(question)

        try:
            client = OpenAI(
                api_key=api_key,
                base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            )
            response = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant in a Discord server."},
                    {"role": "user", "content": question},
                ],
                temperature=0.7,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return self._fallback_response(question)

    def _fallback_response(self, question: str) -> str:

        lowered = question.lower()
        if "hello" in lowered or "hi" in lowered:
            return "Hello! I’m currently running in fallback mode, but I’m happy to help with your questions."
        if "thanks" in lowered or "thank you" in lowered:
            return "You’re welcome! I’m here to help whenever you need me."
        return (
            "I’m using a fallback response right now because the AI service is unavailable. "
            f"Your question was: {question}"
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))
