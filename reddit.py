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

import json
from os import path


class Reddit:
    __karmas = {}

    def __init__(self, client):
        self.__load_json(client.guilds)

    def __vote_user(self, guild, user, change):
        if not (guild.id in self.__karmas.keys()):
            self.__karmas[guild.id] = {}
        the_karmas = self.__karmas[guild.id]

        if not (user.id in the_karmas.keys()):
            the_karmas[user.id] = 0
        the_karmas[user.id] += change

    def __save_json(self):
        for (guild, karmas) in self.__karmas.items():
            the_list = []
            for k, v in karmas.items():
                the_list.append({"user": k, "karma": v})
            the_json = json.dumps(the_list)

            the_path = "./reddit_%d.json" % guild
            with open(the_path, "w+b") as f:
                f.write(the_json.encode("utf8"))

    def __load_json(self, guilds):
        for guild in guilds:
            json_path = "./reddit_%d.json" % guild.id
            guild_karmas = None

            if not path.isfile(json_path):
                print("Guild %d lacks a Reddit karma file, creating." % guild.id)
                with open(json_path, "w") as file:
                    file.write("[]")

            with open(json_path, "r") as file:
                guild_karmas = json.loads(file.read())

            if guild_karmas:
                self.__karmas[guild.id] = {x["user"]: x["karma"] for x in guild_karmas}

    def upvote_user(self, guild, user):
        self.__vote_user(guild, user, 1)
        self.__save_json()

    def downvote_user(self, guild, user):
        self.__vote_user(guild, user, -1)
        self.__save_json()

    def get_karma(self, guild, user):
        if guild.id in self.__karmas.keys():
            if user.id in self.__karmas[guild.id].keys():
                return self.__karmas[guild.id][user.id]
            else:
                return 0
        else:
            return 0

    def get_karmas(self, guild):
        if guild.id in self.__karmas.keys():
            return self.__karmas[guild.id]
        else:
            return {}
