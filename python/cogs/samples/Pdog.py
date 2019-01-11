"""This is a cog for a discord.py bot.
It prints out the current number of discord members and yt subs.

Commands:
    numbers         print yt subs + discord members

Load the cog by calling client.load_extension with the name of this python file
as an argument (without .py)
    example:    bot.load_extension('example')
or by calling it with the path and the name of this python file
    example:    bot.load_extension('folder.example')
"""

from discord.ext import commands
from discord import Member
from os import path
from datetime import datetime, timedelta
import json
import requests
import time
import typing

with open("../config.json", "r") as conffile:
    config = json.load(conffile)


class Stats():
    def __init__(self, client):
        self.client = client
        self.last_time = self.load_stats()
        with open(path.join(path.dirname(__file__), 'permissions.json')) as f:
            self.permitted_roles = json.load(f)[__name__.split('.')[-1]]

    async def __local_check(self, ctx):
        try:
            user_roles = [role.id for role in ctx.message.author.roles]
        except AttributeError:
            return False
        return any(role in self.permitted_roles for role in user_roles)

    def load_state(self):
        with open("../state.json", "r") as statefile:
            return json.load(statefile)

    def load_stats(self):
        state = self.load_state()
        return state.get('stats', [])

    def save_stats(self, stats):
        state = self.load_state()
        state['stats'] = stats
        with open("../state.json", "w") as statefile:
            return json.dump(state, statefile, indent=1)