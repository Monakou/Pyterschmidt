
#  MIT License
#
#  Copyright (c) 2020 E. G. Bland <egb528@york.ac.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import sys
import discord
import pyterschmidt as ps
import reddit


if len(sys.argv) < 2:
    print("Usage: %s <token>" % sys.argv[0])
    sys.exit()

token = sys.argv[1]

message_modules = []
react_modules = []

client = discord.Client()


@client.event
async def on_message(message):
    print("on_message fired")
    print("%s: %s" % (message.author.name, message.content))
    if 676504078309785601 in map(lambda x: x.id, message.mentions):
        for module in message_modules:
            await module.doaction(message)


@client.event
async def on_reaction_add(reaction, user):
    print("on_reaction_add fired")
    for module in react_modules:
        await module.do_reaction_add(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    print("on_reaction_remove fired")
    for module in react_modules:
        await module.do_reaction_remove(reaction, user)


@client.event
async def on_ready():
    print("Connected.")
    if len(message_modules) == 0:
        message_modules.append(ps.TestModule(client))

        red = reddit.Reddit(client)
        message_modules.append(ps.RedditModule(client, red))
        react_modules.append(ps.RedditReactModule(client, red))

client.run(token)