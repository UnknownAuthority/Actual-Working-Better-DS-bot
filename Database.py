import pymongo
import time
import os
import asyncio
import discord


class Database:
    def __init__(self):
        self.DB = os.getenv("DB")
        self.dbclient = pymongo.MongoClient(self.DB)
        self.db = self.dbclient["DiscordBot"]

    async def insertmember(self, ctx, member, unmutetime):
        collection = self.db["MutedPeople"]
        dictwithmember = {
            "memberid": member,
            "unmutetime": round(unmutetime + time.time()),
            "guild_id": ctx.guild.id,
        }
        collection.insert_one(dictwithmember)

    async def remove_and_unmute(self, client):
        print("inside the function")
        collection = self.db["MutedPeople"]
        while True:
            await asyncio.sleep(30)
            allobjects = collection.find({})

            if allobjects.count() > 0:
                for i in allobjects:

                    guild = await client.fetch_guild(i["guild_id"])

                    id = i["memberid"]

                    member = await guild.fetch_member(id)

                    unmutetime = i["unmutetime"]

                    if time.time() >= unmutetime:

                        mutedRole = discord.utils.get(guild.roles, name="Muted")

                        await member.remove_roles(mutedRole)

                        collection.delete_many(i)
                        await member.send(f"You have been unmuted for {guild.name}")
