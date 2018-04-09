import discord
import asyncio
import logging
import handlers.main as handlers
from config import discord as conf

CLIENT = discord.Client()

@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print('------')

@CLIENT.event
async def on_message(msg):
    await handlers.D.handle(msg, CLIENT)

#async def sendToChannel(text, channel):

#Actually do the bot
CLIENT.run(conf["token"])
SERVER = conf["serverID"]
logging.info(CLIENT.servers)