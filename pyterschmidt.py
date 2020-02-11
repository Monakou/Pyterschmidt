import re
import json
from os import path


class DiscordMessageModule:
    __commands = []
    __syntaxs = {}
    __permissions = {}
    __functions = {}
    __isStrict = False

    def __init__(self, commands, syntaxs, permissions, functions):
        self.__commands = commands
        self.__syntaxs = syntaxs
        self.__permissions = permissions
        self.__functions = functions

    # check to see if a message matches the syntax of a command
    def __checksyntax(self, message):
        return map(lambda x: x[0], filter(lambda x: re.search(x[1], message.content, re.IGNORECASE), self.__syntaxs.items()))
        # check for a syntax match

    # public method to be called when a potential command message is picked up
    async def doaction(self, message):
        matched_commands = self.__checksyntax(message)
        for command in matched_commands:
            await self.__functions[command](message)


class RedditModule(DiscordMessageModule):
    __karmas = {}

    def __init__(self, client):
        thecommands = ["karma", "karmalist"]
        thesyntaxs = {"karma": "karma", "karmalist": "karmalist"}
        thepermissions = {"karma": [], "karmalist": []}
        thefunctions = {"karma": self.__do_karma, "karmalist": self.__do_karmalist}
        super().__init__(thecommands, thesyntaxs, thepermissions, thefunctions)

        for guild in client.guilds:
            json_path = "./reddit_%d.json" % guild.id
            guild_karmas = None

            if not path.isfile(json_path):
                print("Guild %d lacks a Reddit karma file, creating." % guild.id)
                with open(json_path, "w") as file:
                    file.write("[]")

            with open(json_path, "r") as file:
                guild_karmas = json.loads(file.read())

            if guild_karmas:
                self.__karmas[guild.id] = guild_karmas

        for k in self.__karmas.items():
            print("Guild %d:" % k[0])
            for u in k[1]:
                print("User %d has %d karma." % (u["user"], u["karma"]))

    async def __do_karma(self, message):
        pass  # TODO don't forget to implement this!

    async def __do_karmalist(self, message):
        pass  # TODO don't forget to implement this!


class TestModule(DiscordMessageModule):
    def __init__(self, client):
        thecommands = ["peter"]
        thesyntaxs = {"peter": "peter"}
        thepermissions = {"peter": []}
        thefunctions = {"peter": self.__do_peter}
        super().__init__(thecommands, thesyntaxs, thepermissions, thefunctions)

    async def __do_peter(self, message):
        await message.channel.send("PEEEEETAAAAAAAAAAH")
