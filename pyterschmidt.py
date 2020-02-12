
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

import discord
import re
import random


class DiscordMessageModule:
    __commands = []
    __syntaxs = {}
    __permissions = {}
    __functions = {}
    __isStrict = False
    __client = None

    def __init__(self, client, commands, syntaxs, permissions, functions):
        self.__client = client
        self.__commands = commands
        self.__syntaxs = syntaxs
        self.__permissions = permissions
        self.__functions = functions

    # returns the client. kinda a workaround, since i can't do it with a non-private field
    def _getclient(self):
        return self.__client

    # check to see if a message matches the syntax of a command
    def __checksyntax(self, message):
        return map(lambda x: x[0], filter(lambda x: re.search(x[1], message.content, re.IGNORECASE), self.__syntaxs.items()))
        # check for a syntax match

    # public method to be called when a potential command message is picked up
    async def doaction(self, message):
        matched_commands = self.__checksyntax(message)
        for command in matched_commands:
            await self.__functions[command](message)


class DiscordReactModule:
    __client = None

    def __init__(self, client):
        self.__client = client

    def _getclient(self):
        return self.__client

    async def do_reaction_add(self, reaction, user):
        pass

    async def do_reaction_remove(self, reaction, user):
        pass


class RedditReactModule(DiscordReactModule):
    __reddit = None

    def __init__(self, client, reddit):
        super().__init__(client)
        self.__reddit = reddit

    async def do_reaction_add(self, reaction, user):
        if reaction.emoji.name == "upvote":
            self.__reddit.upvote_user(reaction.message.guild, reaction.message.author)

        if reaction.emoji.name == "downvote":
            self.__reddit.downvote_user(reaction.message.guild, reaction.message.author)

    async def do_reaction_remove(self, reaction, user):
        if reaction.emoji.name == "upvote":
            self.__reddit.downvote_user(reaction.message.guild, reaction.message.author)

        if reaction.emoji.name == "downvote":
            self.__reddit.upvote_user(reaction.message.guild, reaction.message.author)


class RedditModule(DiscordMessageModule):
    __reddit = None

    def __init__(self, client, reddit):
        thecommands = ["karma", "karmalist"]
        thesyntaxs = {"karma": "karma$", "karmalist": "karmalist$"}
        thepermissions = {"karma": [], "karmalist": []}
        thefunctions = {"karma": self.__do_karma, "karmalist": self.__do_karmalist}
        super().__init__(client, thecommands, thesyntaxs, thepermissions, thefunctions)

        self.__reddit = reddit

    async def __do_karma(self, message):
        await message.channel.send("You have %d karma." % self.__reddit.get_karma(message.guild, message.author))

    async def __do_karmalist(self, message):
        karmas_sorted = {k: v for k, v in sorted(self.__reddit.get_karmas(message.guild).items(), key=lambda x: x[1], reverse=True)}
        the_embed = discord.Embed(title="Reddit Leaderboard", type="rich")
        for (user, karma) in karmas_sorted.items():
            the_user = super()._getclient().get_user(user)
            if the_user:
                the_embed.add_field(name="%s#%s" % (the_user.name, the_user.discriminator), value=karma, inline=False)
        await message.channel.send(embed=the_embed)


class CouncilModule(DiscordMessageModule):
    __valid_emotes = ["HarryTeemo", "HarryKuma", "HarryHoliday", "Harrygasm", "HarryUncaring"]
    __emote_map = {}

    def __init__(self, client):
        thecommands = ["council"]
        thesyntaxs = {"council": "council"}
        thepermissions = {"council": []}
        thefunctions = {"council": self.__do_council}
        super().__init__(client, thecommands, thesyntaxs, thepermissions, thefunctions)

        for guild in client.guilds:
            self.__emote_map[guild.id] = {k: v for (k, v) in map(lambda x: (x.name, x.id), guild.emojis)}

    async def __do_council(self, message):
        matcher = re.search("council (.*)", message.content)


class TestModule(DiscordMessageModule):
    def __init__(self, client):
        thecommands = ["peter"]
        thesyntaxs = {"peter": "peter$"}
        thepermissions = {"peter": []}
        thefunctions = {"peter": self.__do_peter}
        super().__init__(client, thecommands, thesyntaxs, thepermissions, thefunctions)

    async def __do_peter(self, message):
        await message.channel.send("PEEEEETAAAAAAAAAAH")
