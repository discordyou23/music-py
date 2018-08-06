import discord
import asyncio
import youtube_dl
import os
from discord.ext import commands
from discord.ext.commands import Bot


bot=commands.Bot(command_prefix='W')

from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))
load_opus_lib()



@bot.event
async def on_ready():
    print("hi")
opts = {
            'default_search': 'auto',
            'quiet': True,
        }    
    
@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)



players={}
@bot.command(pass_context=True)
async def play(ctx, *,url):
    global play_server
    play_server = ctx.message.server
    voice = bot.voice_client_in(play_server)
    global player
    player = await voice.create_ytdl_player(url,ytdl_options=opts)
    players[play_server.id] = player
    if player.is_live == True:
        await bot.say("Can not play live audio yet.")
    elif player.is_live == False:
        player.start()


async def pause(ctx):
    player.pause()

@bot.command(pass_context=True)
async def resume(ctx):
    player.resume()
          
@bot.command(pass_context=True)
async def volume(ctx, vol):
    vol = float(vol)
    vol = player.volume = vol

@bot.command(pass_context=True)
async def stop(ctx):
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    await voice_client.disconnect()


    
    
 
@bot.event
async def on_ready():

    """WHEN BOT IS READY, PRINT MESSAGE IN TERMINAL"""
    print("I am running on " + bot.user.name)
    games=['Bread Puppies','Jump Rope Kitten: Nyawatobi','TripTrap','Potion Maker','Crusaders Quest','My Waffle Maker','AfroCat','Hello Kitty','Halo 4','My Cat Album','LINE: Disney Tsum Tsum','Cat Room','Alphabear','Play With Cats','My Dog Album','Giant Turnip Game','MEOW MEOW STAR ACRES','Patchmania','Tiny Sheep','Hello Kitty World – Fun Park Game']
#     while True:
#         global random_status_game
#         random_status_game=random.choice(games)
#         await asyncio.sleep(2)
    await bot.change_presence(game=discord.Game(name='Wjoin|Wplay-W Bot Music server'))
    
    
    
    

bot.run(os.environ['BOT_TOKEN'])
