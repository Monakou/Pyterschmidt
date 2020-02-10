import sys
import discord
import re
import pyterschmidt as ps


if len(sys.argv) < 2:
    print("Usage: %s <token>" % sys.argv[0])
    sys.exit()

token = sys.argv[1]

modules = []

client = discord.Client()


@client.event
async def on_message(message):
    print("%s: %s" % (message.author.name, message.content))
    if 676504078309785601 in map(lambda x: x.id, message.mentions):
        for module in modules:
            await module.doaction(message)

@client.event
async def on_ready():
    print("Connected.")
    if len(modules) == 0:
        modules.append(ps.TestModule(client))

client.run(token)