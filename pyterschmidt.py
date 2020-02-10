import abc
import re


class DiscordMessageModule:
    def __init__(self, client):
        pass

    def _checksyntax(self, message):
        pass
        # check for a syntax match

    async def doaction(self, message):
        if self._checksyntax(message):
            await self._performaction(message)

    async def _performaction(self, message):
        pass
        # do the action


class TestModule(DiscordMessageModule):
    def __init__(self, client):
        super().__init__(client)

    def _checksyntax(self, message):
        return True if re.search("[Pp][Ee][Tt][Ee][Rr]", message.content) else False

    async def _performaction(self, message):
        await message.channel.send("PEEEEETAAAAAAAAAAH")
