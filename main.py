import discord
import os
import pandas as pd
from datetime import date

client = discord.Client()

def quoteMsg(msg):
  return "`" + msg + "`"

async def case_today(message):
  url = 'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv'
  df = pd.read_csv(url, header=0)
  caseTodayIloc = df.iloc[-1]
  
  today = date.today()
  todayFormat = today.strftime("%Y-%m-%d")

  if (todayFormat != caseTodayIloc['date']) :
    msgDate = ('Cases for today has not been updated yet.')    

  caseDate = 'MALAYSIA COVID-19 Cases as of %s' % caseTodayIloc['date']
  caseNew = 'New Cases : %s' % caseTodayIloc['cases_new']

  finalMsg = quoteMsg('%s\n\n%s\n%s' % (msgDate,caseDate,caseNew))
  await message.channel.send(finalMsg)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-kt'):
       await case_today(message)

    if message.content.startswith('-khelp'):
       await message.channel.send(quoteMsg('KOVID-MY COMMANDS \n\n-kt for today/latest cases recorded by KKM\n-khelp for help'))

client.run(os.getenv('TOKEN'))