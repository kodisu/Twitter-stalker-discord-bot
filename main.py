import threading
import my_utils
import feeder
from stalker import stalk_all
import os
import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File
from replit import db
import json
from keep_alive import keep_alive






def looper():
    threading.Timer(900.0, looper).start() # call every 15 minute
    stalk_all()

# def feeder():
#   rules = feeder.get_rules()
#   delete = feeder.delete_all_rules(rules)
#   set = feeder.set_rules(delete)
#   feeder.get_stream(set)

#RUNNING CODE#
webhook_url = os.environ['DISCORD_WEBHOOK']
discord.webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

# discord bot
client = discord.Client()

@client.event
async def on_ready():
  print('Logged in a {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client:
      return
    if message.content.startswith('$meow'):
      await message.channel.send("meow meow")
    if message.content.startswith ('$twitter stalk all'):
      stalk_all()


keep_alive()
looper()
client.run(os.environ['DISCORD_BOT_TOKEN'])
# feeder()


