import discord
from discord.ext import commands
import time
import asyncio


# bot_client_id = 646168037044781067
# server_id = 646167787756191744
messages = joined = 0


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


@client.event
async def on_member_join(member, message):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await message.channel.send(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    global messages
    messages += 1

    id = client.get_guild(646167787756191744)

    if message.content.find("!hello") != -1:
        await message.channel.send('Hello! {0.author.mention}'.format(message))
    elif message.content == "!users":
        await message.channel.send(f"""Number of Members: {id.member_count}""")

    if message.content == "!help":
        embed = discord.Embed(title="Ahlstrom Commands")
        embed.add_field(name="!hello", value="Greets the user")
        embed.add_field(name="!users", value="Prints number of users")
        await message.channel.send(content=None, embed=embed)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='new role')
    await client.add_roles(member, role)


client.loop.create_task(update_stats())
client.run(token)
