import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from typing import Final
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler = logging.FileHandler(filename='disnake.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()

intents = disnake.Intents.default()
intents.typing = True
intents.message_content = True
intents.presences = True
intents.reactions = True
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True
bot = commands.Bot(command_prefix='!',test_guilds=[os.getenv('GUILD_IDS')],command_sync_flags=command_sync_flags,)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(description="Make the bot say something")
@commands.is_owner()
async def say(inter, channel: disnake.TextChannel, content: str):
    await channel.send(content)
    await inter.response.send_message(f"Message sent in {channel.mention}: {content}")

@bot.slash_command(description="Give the list of commands")
async def help(ctx):
    commands_list = [command.name for command in bot.slash_commands]
    commands_str = "\n".join(commands_list)
    await ctx.send(f"Here are all the available commands:\n{commands_str}")

@bot.slash_command(description="Gives the bot information",name="botinfo")
async def botinfo(ctx):
    embed = disnake.Embed(title=f"Bot information: {bot.user}")
    embed.set_thumbnail(url="Add image URL here")
    embed.add_field(name="Username", value=bot.name, inline=True)
    embed.add_field(name="Account Created", value=bot.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Author", value=bot.owner, inline=True )
    await ctx.send(embed=embed)

@bot.slash_command(name="userinfo", description="Displays user information", guild_ids=test_guilds)
async def userinfo(inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
    embed = disnake.Embed(title=f"User Information for {user.display_name}", color=0x7289DA)
    if user.avatar:
        embed.set_thumbnail(url=user.avatar.url)
    else:
        embed.set_thumbnail(url="https://www.google.com/imgres?q=discord%20default%20avatar&imgurl=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FFvpBu6vXwAAAKe4.jpg&imgrefurl=https%3A%2F%2Ftwitter.com%2FWeedleTwineedle%2Fstatus%2F1655708119987638272&docid=QRDp5NfhVRYrAM&tbnid=vUOZ3t1XrXZVvM&vet=12ahUKEwiL_uiR9MiHAxVWR2wGHfUeHgEQM3oECHAQAA..i&w=1200&h=900&hcb=2&ved=2ahUKEwiL_uiR9MiHAxVWR2wGHfUeHgEQM3oECHAQAA")  

    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%b %d, %Y"), inline=True)
    
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%b %d, %Y"), inline=True)
    roles = [role.mention for role in user.roles if role.name != "@everyone"]
    embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=True)

    await inter.response.send_message(embed=embed)

@userinfo.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')



    

bot.run(os.getenv('DISCORD_TOKEN'))


