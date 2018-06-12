import discord, aiohttp
import config

class Chatbot:

    def __init__(self, bot):
        self.bot = bot

    async def message_handler(self, message):
        channel = message.channel
        content = message.content
        if message.author.bot:
            return

        if content.startswith("<@310039170792030211> ") or content.startswith("<@!310039170792030211> "):
            commands = []
            for command in self.bot.commands:
                commands.append(command.name)
            hascommand = 0
            for command in commands:
                if str(message.content[22:]).startswith(command) or str(message.content[23:]).startswith(command):
                    hascommand += 1
            if hascommand >= 1:
                return
            await channel.trigger_typing()
            async with aiohttp.ClientSession(headers={"Authorization": config.chatbot}) as cs:
                terms = str(message.content[22:]).replace(" ", "%20")
                async with cs.get(f'https://api.dialogflow.com/v1/query?v=20150910&lang=en&query={terms}&sessionId=0') as r:
                    res = await r.json()
                    await channel.send(embed=discord.Embed(color=0xDEADBF, description=res['result']['fulfillment']['messages'][0]['speech']))

def setup(bot):
    n = Chatbot(bot)
    bot.add_listener(n.message_handler, "on_message")
    bot.add_cog(n)