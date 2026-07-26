import asyncio
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

from cogs.fun import Fun


class DummyContext:
    def __init__(self, guild):
        self.guild = guild
        self.sent_message = None

    async def send(self, embed=None):
        self.sent_message = embed
        return None


class FunCogTests(unittest.TestCase):
    def test_serverinfo_without_icon_does_not_crash(self):
        cog = Fun(MagicMock())
        guild = SimpleNamespace(
            name="Test Server",
            member_count=42,
            created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
            icon=None,
        )
        ctx = DummyContext(guild)

        asyncio.run(cog.serverinfo.callback(cog, ctx))

        self.assertIsNotNone(ctx.sent_message)


if __name__ == "__main__":
    unittest.main()
