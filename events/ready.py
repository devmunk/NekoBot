import logging
import discord
import config
from datetime import datetime

logger = logging.getLogger(__name__)

class ErrorHandler:

    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.bot.uptime = datetime.utcnow()

        guilds = len(self.bot.guilds)
        members = len(set(self.bot.get_all_members()))
        shards = self.bot.shard_count

        logger.info(f"Ready, {guilds} Guilds, {members} Members, {shards} Shards.")
        logger.info(f"ShardID {self.bot.shard_id}")

        await self.bot.change_presence(status=discord.Status.idle)

    async def on_shard_ready(self, shardid):
        logger.info(f"Shard {shardid} Ready!")

        webhook_url = f"https://discordapp.com/api/webhooks/{config.webhook_id}/{config.webhook_token}"
        payload = {
            "embeds": [
                {
                    "title": "Shard Connect.",
                    "description": f"Shard {shardid} has connected on ShardID {self.bot.shard_id}.",
                    "color": 14593471
                }
            ]
        }
        await self.bot.aiohttp.post(webhook_url, json=payload)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))