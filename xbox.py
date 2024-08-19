import discord
from discord.ext import commands
import requests
import os

intents = discord.Intents.default()
TOKEN ='TON TOKEN'
bot = commands.Bot(command_prefix='!', intents=intents)
intents.message_content = True

 
@bot.event
async def on_ready():
    print('Logged on as', bot.user)

@bot.command()
async def xbox(ctx, xbox_id: str):
    headers = {
        'Authorization': 'Bearer ' + os.getenv('hamoud'),
        'X-Authorization': os.getenv('hamoud'),
        'Content-Type': 'application/json'
    }
    response = requests.get(f'https://xbl.io/api/v2/account/{xbox_id}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        user_data = data['profileUsers'][0]
        settings = {setting['id']: setting['value'] for setting in user_data['settings']}
        
        embed = discord.Embed(title=settings['Gamertag'], color=0x00ff00)
        embed.add_field(name="ID", value=user_data['id'], inline=False)
        embed.add_field(name="Gamerscore", value=settings['Gamerscore'], inline=True)
        embed.add_field(name="Account Tier", value=settings['AccountTier'], inline=True)
        embed.add_field(name="Xbox One Rep", value=settings['XboxOneRep'], inline=True)
        embed.add_field(name="Real Name", value=settings['RealName'], inline=False)
        embed.add_field(name="Bio", value=settings['Bio'], inline=False)
        embed.add_field(name="Location", value=settings['Location'], inline=True)
        embed.set_thumbnail(url=settings['GameDisplayPicRaw'])
        
        await ctx.send(embed=embed)
    else:
        await ctx.send('Unable to fetch Xbox info')

bot.run(TOKEN)
