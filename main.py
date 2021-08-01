import os
import requests
import discord
import discord
from discord import Webhook, RequestsWebhookAdapter, File
from replit import db
import json
from keep_alive import keep_alive
import threading

#FUNCTIONS#
def get_id(username):
  url = "https://api.twitter.com/2/users/by/username/" + username
  bearer =  os.environ['TWITTER_BEARER']
  payload={}
  headers = {
    'Authorization': bearer,
    'Cookie': 'your_cookie; personalization_id="your_id"'  
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  parsed = json.loads(response.text)
  return(parsed["data"]["id"])

def get_new_following(username):
  id = get_id(username)
  #max amount of followers we can get is 1000, a limitiation set by Twitter API v2
  url = url = "https://api.twitter.com/2/users/"+id+"/following"
  bearer =  os.environ['TWITTER_BEARER']
  payload={}
  headers = {
   'Authorization': bearer,
    'Cookie': 'your_cookie; personalization_id="your_id"'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  current_following = json.loads(response.text)
  current_following = current_following["data"] 

  try: 
    #if already stored in database
    last_following = db[id]
    if current_following == last_following:
      print(username + " no new following accounts yet")
    else:
      discord.webhook.send(username + " is following these new accounts:")
      for f in current_following:
        if f in last_following:
          break
        else:
          link = " https://twitter.com/" + f['username']
          discord.webhook.send("   new account: " + f['username'] + link)
      db[id] = current_following #update the follower list into the database
  
  #if no key exists
  except KeyError: 
    db[id] = current_following
    discord.webhook.send(username + " added to stalking database")

def stalk_all():
  for a in accounts:
    get_new_following(a)

def looper(count):
    threading.Timer(900.0, looper).start() # call every 15 minute
    stalk_all()
    count+=1
    print("loop no."+ str(count))


#RUNNING CODE#
webhook_url = os.environ['DISCORD_WEBHOOK']
discord.webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

# these are the twitter accounts whos "following" list we are stalking
accounts = ["mcuban","elonmusk","nyannyancat"]

# discord bot
my_secret = os.environ['DISCORD_BOT_TOKEN']
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
    if message.content.startswith ('$twitter stalk'):
      stalk_all()


keep_alive()
count = 0
looper(count)
client.run(os.environ['DISCORD_BOT_TOKEN'])
