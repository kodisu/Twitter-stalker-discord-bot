import os
import requests
import discord
import discord
from discord import Webhook, RequestsWebhookAdapter, File
from replit import db
import json
from keep_alive import keep_alive


###Accounts to Stalk###
# these are the twitter accounts whos "following" list we are stalking
accounts = ["mcuban","elonmusk"]



#FUNCTIONS FOR STALKER#
def get_id(username):
  url = "https://api.twitter.com/2/users/by/username/" + username
  bearer =  os.environ['TWITTER_BEARER']
  payload={}
  headers = {
    'Authorization': bearer,
    'Cookie': 'guest_id=v1%3A; personalization_id="v1_j="'
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
    'Cookie': 'guest_id=v1%36; personalization_id="v1_jAjg=="'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  current_following = json.loads(response.text)
  current_following = current_following["data"] 
  
  intro_line = False

  try: 
    #if already stored in database
    last_following = db[id]
    if current_following == last_following:
      print(username + " no new following accounts yet")
    else:
      for f in current_following:
        if f in last_following:
          break
        else:
          if intro_line == False:
            discord.webhook.send(username + "\'s following new accounts:")
            intro_line = True
          link = " https://twitter.com/" + f['username']
          discord.webhook.send(f['username'] + link)
      db[id] = current_following #update the follower list into the database
  
  #if no key exists
  except KeyError: 
    db[id] = current_following
    discord.webhook.send(username + " added to stalking database")
  except json.decoder.JSONDecodeError:
    discord.webhook.send("during " + username + " GET call JSONDecodeError occured")

def stalk_all():
  # discord.webhook.send("initialising stalk...")
  for a in accounts:
    get_new_following(a)
  # discord.webhook.send("stalk completed.")
