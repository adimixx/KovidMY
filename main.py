import discord
import os
import pandas as pd
from datetime import date

client = discord.Client()

def quoteMsg(msg):
  return "```" + msg + "```"

async def case_today(message):
  urlCases = 'https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv'
  df = pd.read_csv(urlCases, header=0)
  caseTodayIloc = df.iloc[-1]  

  urlCasesState = 'https://github.com/MoH-Malaysia/covid19-public/raw/main/epidemic/cases_state.csv'

  dfCasesState = pd.read_csv(urlCasesState, header=0).query("date == '%s'" % caseTodayIloc['date']).drop('date',1)

  caseDate = 'MALAYSIA COVID-19 Cases as of %s' % caseTodayIloc['date']
  caseNew = 'New Cases : %s' % caseTodayIloc['cases_new']

  caseState = 'Cases by states : \n%s' % dfCasesState.to_string(index=False, header=False)

  finalMsg = quoteMsg('%s\n%s\n\n%s' % (caseDate,caseNew, caseState))
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