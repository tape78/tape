import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from typing import Final
import os
import logging

logger = logging.getLogger('disnake')
logger.setLevel(logging.DEBUG)
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
bot = commands.Bot(command_prefix='!',test_guilds=["GUILD ID HERE"],command_sync_flags=command_sync_flags,intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    command_count = len(bot.slash_commands)

@bot.slash_command(description="Make the bot say something")
@commands.is_owner()
async def say(inter, channel: disnake.TextChannel, content: str):
    await channel.send(content)
    await inter.response.send_message(f"Message sent in {channel.mention}: {content}")

@bot.command()
@commands.is_owner()
async def say(ctx, channel: disnake.TextChannel, content: str):
    await channel.send(content)
    await ctx.send(f"Message sent in {channel.mention}: {content}")

@bot.slash_command(description="Give the list of commands")
async def help(ctx):
    commands_list = [command.name for command in bot.slash_commands]
    commands_str = "\n".join(commands_list)
    await ctx.send(f"Here are all the available commands:\n{commands_str}")

@bot.slash_command(description="Gives the bot information", name="botinfo")
async def botinfo(inter):
    embed = disnake.Embed(title=f"Bot information: {bot.user}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1264916815289782354/1266983968650170450/Tape.png?ex=66a72245&is=66a5d0c5&hm=b6a7aa88ffa81509f034b3bb1b592404d8bad7d9127cc362cedb322745bcdfda&")
    embed.add_field(name="Username", value=bot.user.name, inline=True)
    embed.add_field(name="Account Created", value=bot.user.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Author", value=str(bot.owner), inline=True)
    embed.add_field(name="Commands", value=len(bot.slash_commands), inline=True)
    await inter.response.send_message(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = disnake.Embed(title=f"Bot information: {bot.user}")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1264916815289782354/1266983968650170450/Tape.png?ex=66a72245&is=66a5d0c5&hm=b6a7aa88ffa81509f034b3bb1b592404d8bad7d9127cc362cedb322745bcdfda&")
    embed.add_field(name="Username", value=bot.user.name, inline=True)
    embed.add_field(name="Account Created", value=bot.user.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Author", value=str(bot.owner), inline=True)
    embed.add_field(name="Commands", value=len(bot.slash_commands), inline=True)
    await ctx.send(embed=embed)

@bot.slash_command(name="userinfo", description="Displays user information", guild_ids=test_guilds)
async def userinfo(inter: disnake.ApplicationCommandInteraction, user: disnake.Member):
    embed = disnake.Embed(title=f"User Information for {user.display_name}", color=0x7289DA)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%b %d, %Y"), inline=True)
    roles = [role.mention for role in user.roles if role.name != "@everyone"]
    embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=True)
    await inter.response.send_message(embed=embed)

@bot.command()
async def userinfo(ctx, user: disnake.Member):
    embed = disnake.Embed(title=f"User Information for {user.display_name}", color=0x7289DA)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Joined Server", value=user.joined_at.strftime("%b %d, %Y"), inline=True)
    roles = [role.mention for role in user.roles if role.name != "@everyone"]
    embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=True)
    await ctx.send(embed=embed)

@userinfo.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.slash_command(description="Ping...Pong!!")
async def ping(inter):
    await inter.response.send_message('Pong!')



bot.run(os.getenv('DISCORD_TOKEN'))


