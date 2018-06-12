import asyncio, config, discord, random, aiohttp
import pymysql

messages = ["OwO Whats this", "MonkaS", "OwO", "Haiiiii", ".help", "🤔🤔🤔", "HMMM🤔", "USE n! WEW", "n!HELP REE"]
connection = pymysql.connect(host="localhost",
                                     user="root",
                                     password="rektdiscord",
                                     db="nekobot",
                                     port=3306)
stats2 = ["OwO whats n!help", "🤔🤔🤔", "👀", "(╯°□°）╯︵ ┻━┻",
                  "¯\_(ツ)_/¯", "┬─┬ノ(ಠ_ಠノ)", "><(((('>", "_/\__/\__0>", "ô¿ô", "°º¤ø,¸¸,ø¤º°`°º¤ø,", "=^..^=",
                  "龴ↀ◡ↀ龴", "^⨀ᴥ⨀^", "^⨀ᴥ⨀^", "⨌⨀_⨀⨌", "•|龴◡龴|•", "ˁ˚ᴥ˚ˀ", "⦿⽘⦿", " (╯︵╰,)",
                  " (╯_╰)", "㋡", "ˁ˚ᴥ˚ˀ", "\(^-^)/"]
db = connection.cursor()

class DiscordBotsOrgAPI:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = config.dbots_key

    async def startdbl(self):
        while True:
            print("Getting all servers.")
            totalservers = len(self.bot.guilds)
            print("Attempting to update server count.")
            try:
                url = "https://discordbots.org/api/bots/310039170792030211/stats"
                payload = {
                    "server_count": int(totalservers),
                    "shard_id": self.bot.shard_id,
                    "shard_count": len(self.bot.shards)
                }
                async with aiohttp.ClientSession() as cs:
                    async with cs.post(url, json=payload, headers={"Authorization": config.dbots_key}) as r:
                        res = await r.json()
                print(res)
                print("Posted server count. {}".format(totalservers))
                game = discord.Streaming(name=random.choice(stats2), url="https://www.twitch.tv/rektdevlol")
                await self.bot.change_presence(activity=game)
            except Exception as e:
                print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post('https://bots.discord.pw/api/bots/310039170792030211/stats',
                                            headers={'Authorization': f'{config.dpw_key}'},
                                            json={"server_count": int(totalservers),
                                                  "shard_id": self.bot.shard_id,
                                                  "shard_count": self.bot.shard_count}) as response:
                        t = await response.read()
                        print(t)
            except Exception as e:
                print(f"Failed to post to pw, {e}")
            await asyncio.sleep(1800)


    async def on_ready(self):
        await self.startdbl()

def setup(bot):
    bot.add_cog(DiscordBotsOrgAPI(bot))
