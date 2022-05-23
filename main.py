import discord
import os
import requests
import json

import DAILY
import DONCHIAN
import RSI
import SMA

client = discord.Client()

def get_advice(userMessage):
  if userMessage == '$daily':
    message = DAILY.advice()
  elif userMessage == '$sma':
    message = SMA.advice()
  elif userMessage == '$don':
    message = DONCHIAN.advice()
  elif userMessage == '$rsi':
    message = RSI.advice()
  else:
    message = 'error, try again'
  return message

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print('If you want to get daily advice, please use $daily command.'.format(client))
  print('If you want to get advice based on SMA strategy, please use $sma command.'.format(client))
  print('If you want to get advice based on Donchian strategy, please use $don command.'.format(client))
  print('If you want to get advice based on RSI strategy, please use $rsi command.'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$daily'):
    advice = get_advice('$daily')
    await message.channel.send(advice)
  if message.content.startswith('$sma'):
    advice = get_advice('$sma')
    await message.channel.send(advice)
  if message.content.startswith('$don'):
    advice = get_advice('$don')
    await message.channel.send(advice)
  if message.content.startswith('$rsi'):
    advice = get_advice('$rsi')
    await message.channel.send(advice)
client.run(os.getenv('TOKEN'))