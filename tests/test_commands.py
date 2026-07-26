import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from cogs.ai import AI
from cogs.fun import Fun
from cogs.moderation import Moderation


class CommandTests(unittest.IsolatedAsyncioTestCase):
    async def test_ping(self):
        bot = MagicMock(latency=0.123)
        cog = Fun(bot)
        ctx = SimpleNamespace(send=AsyncMock())

        await cog.ping.callback(cog, ctx)

        ctx.send.assert_awaited_once()
        self.assertIn("Pong!", ctx.send.await_args.args[0])

    async def test_serverinfo(self):
        bot = MagicMock()
        cog = Fun(bot)
        guild = SimpleNamespace(
            name="Test Server",
            member_count=3,
            created_at=SimpleNamespace(strftime=lambda fmt: "2026-07-22"),
            icon=None,
        )
        ctx = SimpleNamespace(guild=guild, send=AsyncMock())

        await cog.serverinfo.callback(cog, ctx)

        ctx.send.assert_awaited_once()
        embed = ctx.send.await_args.kwargs["embed"]
        self.assertEqual(embed.title, "Test Server")

    async def test_userinfo(self):
        bot = MagicMock()
        cog = Fun(bot)
        target = SimpleNamespace(
            display_name="Tester",
            name="tester",
            id=42,
            joined_at=SimpleNamespace(strftime=lambda fmt: "2026-07-22"),
            roles=[SimpleNamespace(name="@everyone", mention="@everyone"), SimpleNamespace(name="Admin", mention="@Admin")],
        )
        ctx = SimpleNamespace(author=target, send=AsyncMock())

        await cog.userinfo.callback(cog, ctx, None)

        ctx.send.assert_awaited_once()
        embed = ctx.send.await_args.kwargs["embed"]
        self.assertEqual(embed.title, "User Info - Tester")

    async def test_poll(self):
        bot = MagicMock()
        cog = Fun(bot)
        reaction_message = SimpleNamespace(add_reaction=AsyncMock())
        ctx = SimpleNamespace(send=AsyncMock(return_value=reaction_message))

        await cog.poll.callback(cog, ctx, question="Is this working?")

        ctx.send.assert_awaited_once()
        self.assertEqual(reaction_message.add_reaction.await_count, 2)

    async def test_ask_fallback(self):
        bot = MagicMock()
        cog = AI(bot)
        ctx = SimpleNamespace(send=AsyncMock(), typing=lambda: SimpleNamespace(__aenter__=lambda self: None, __aexit__=lambda self, exc_type, exc, tb: False))

        async def fake_typing():
            class CM:
                async def __aenter__(self):
                    return None
                async def __aexit__(self, exc_type, exc, tb):
                    return False
            return CM()

        ctx.typing = lambda: asyncio.Future()  # placeholder to be replaced below

        class TypingContext:
            async def __aenter__(self):
                return None
            async def __aexit__(self, exc_type, exc, tb):
                return False

        ctx.typing = lambda: TypingContext()

        await cog.ask.callback(cog, ctx, question="Hello")

        ctx.send.assert_awaited_once()
        self.assertIn("Hello", ctx.send.await_args.args[0])

    async def test_kick(self):
        bot = MagicMock()
        cog = Moderation(bot)
        member = SimpleNamespace(mention="@test", top_role=3, id=99, kick=AsyncMock())
        author = SimpleNamespace(top_role=5, id=1)
        guild = SimpleNamespace(owner_id=2)
        ctx = SimpleNamespace(author=author, guild=guild, send=AsyncMock())

        await cog.kick.callback(cog, ctx, member, reason="spam")

        member.kick.assert_awaited_once_with(reason="spam")
        ctx.send.assert_awaited_once()

    async def test_ban(self):
        bot = MagicMock()
        cog = Moderation(bot)
        member = SimpleNamespace(mention="@test", top_role=3, id=99, ban=AsyncMock())
        author = SimpleNamespace(top_role=5, id=1)
        guild = SimpleNamespace(owner_id=2)
        ctx = SimpleNamespace(author=author, guild=guild, send=AsyncMock())

        await cog.ban.callback(cog, ctx, member, reason="spam")

        member.ban.assert_awaited_once_with(reason="spam")
        ctx.send.assert_awaited_once()

    async def test_clear(self):
        bot = MagicMock()
        cog = Moderation(bot)
        channel = SimpleNamespace(purge=AsyncMock(return_value=[1, 2, 3, 4, 5]))
        ctx = SimpleNamespace(channel=channel, send=AsyncMock())

        await cog.clear.callback(cog, ctx, 5)

        channel.purge.assert_awaited_once_with(limit=6)
        ctx.send.assert_awaited_once()

    async def test_mute(self):
        bot = MagicMock()
        cog = Moderation(bot)
        member = SimpleNamespace(add_roles=AsyncMock(), roles=[], mention="@test")
        role = SimpleNamespace()
        channel = SimpleNamespace(set_permissions=AsyncMock())
        guild = SimpleNamespace(
            text_channels=[channel],
            voice_channels=[],
            roles=[SimpleNamespace(name="@everyone")],
        )
        ctx = SimpleNamespace(guild=guild, send=AsyncMock())

        async def fake_get_or_create_muted_role(guild_obj):
            return role

        cog._get_or_create_muted_role = fake_get_or_create_muted_role

        await cog.mute.callback(cog, ctx, member)

        member.add_roles.assert_awaited_once()
        ctx.send.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
