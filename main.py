# This example requires the 'message_content' intent.

# https://discord.com/api/oauth2/authorize?client_id=1210673428944785428&permissions=116736&scope=bot

import discord

# setup translator
import translators as ts

token = ""

en_channel_id = 0
cn_channel_id = 0


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



def to_cn(msg):
    return ts.translate_text(msg, to_language="zh-CN", translator="google")

def to_en(msg): 
    return ts.translate_text(msg, from_language="auto", to_language="en", translator="google")



async def do(message, send_to, translate_func):
    # text check, if not, don't send a text embed
    if message.content != "" and message.content != None:
        tl_msg = translate_func(message.content)

        embed=discord.Embed( description=tl_msg)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
        await send_to.send(embed=embed)


    # handles images
    for attached in message.attachments:
        await send_to.send(embed=discord.Embed()
                            .set_image(url=attached.url)
                            .set_author(name=message.author.name, icon_url=message.author.avatar.url))






@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # gets cn_chat and en_chat channel object
    global cn_chat 
    global en_chat 

    cn_chat = client.get_channel(cn_channel_id)
    en_chat = client.get_channel(en_channel_id)

    print('Channel set')

@client.event
async def on_message(message):
    # escpae, don't take into account own msgs
    if message.author == client.user:
        return
    
    # status check and escape
    if message.content.startswith('$status'):
        await message.channel.send('Up!')
        return 


    # if in en chat, translate and send to cn chat
    if message.channel == en_chat:
        await do(message, cn_chat, to_cn)


    # if in cn chat, translate and send to en chat
    if message.channel == cn_chat:
        await do(message, en_chat, to_en)
        


    # print(message.channel)

client.run(token)