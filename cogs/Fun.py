from discord.ext import commands
import re
import requests
import json
import discord
from flashtext import KeywordProcessor
from discord.commands import slash_command

# function code from freecodecamp
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote
def get_insult():
  response = requests.get("https://evilinsult.com/generate_insult.php")
  return response.text

# compile the regex
pattern = re.compile(r"ree+\b", re.IGNORECASE)


class Fun(commands.Cog):
    """Fun, non-serious commands, not made for practical purposes"""
    def __init__(self, client):
        self.client = client
        # get all the specialcommmands from the json file
        with open("NoPref.json", "r") as f:
            self.Dictwithstuff = json.loads(f.read())

    
    @slash_command()
    async def hello(self, ctx):
        await ctx.respond("hello!")
    @commands.command()
    async def insult(self, ctx):
      await ctx.send(get_insult())

    def im_sad_gen(self):
        return f"Don't be sad, here have a quote \n {get_quote()}"
    
    @commands.command()
    async def quote(self, ctx):
        await ctx.send(get_quote())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        """
        Figured that this might be time to explain our specialcommand system

        These commands can be of multiple words eg (welcome to ds) and do not require a prefix, as they're words searched inside messages

        It searches inside messages, eg:(considering command in question is "hello", it'll search if the message contains "hello" or not, therefore it will respond to a message such as "Oh, I forgot, Hello I am iron man")

        -Every command and response here are stored in the json file named "NoPref.json"        
        
        -Every command and response can be added on the go, with the methods ?cc and ?sc (although I somehow forgot to add deleting said commands lol)

        """

        # Iterate through the command and response in the dict

        for command, response in self.Dictwithstuff.items():
            """
            keyword_processors, this is from the flashtext library imported above
            pretty much a faster way to search through messages, since we don't need regex here anyways

            """
            # initialize a new keyword_processor
            keyword_processor = KeywordProcessor(case_sensitive=False)
            # set the command as the keyword to search for
            keyword_processor.add_keyword(command)
            #Add " and ' to be recognised as a word so "no u" doesn't triggered
            keyword_processor.add_non_word_boundary("'")
            keyword_processor.add_non_word_boundary('"')
            # get the content of the message
            messagecont = message.content
            if command in keyword_processor.extract_keywords(messagecont):
                # if the command is anything other than "im sad"
                # send the usual response
                # if it is "im sad" then send the response generator               
                if command == "im sad":
                  await message.channel.send(self.im_sad_gen())
                  break
                elif command == "try to insult me you bot":
                  await message.channel.send(get_insult())
                  break
                await message.channel.send(response)
            # if the message is a ree(with as many e's)
            # we need to regex pattern match it
            elif pattern.match(messagecont):
                await message.channel.send(
                    "https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544"
                )

                break
  
    @commands.command(aliases=["special"])
    async def specialCommands(self, ctx):      
        "Lists Commands Without any prefix, alias = noprefix"
        
        embed = discord.Embed(title="All Special Commands", description= "List of all phrases that'll trigger the bot")
        for x, y in self.Dictwithstuff.items():
            embed.add_field(name=x, value=y)
        embed.add_field(
            name="Ree",
            value="You can reee with as many e's you want(as long as its more than one) it'll send https://tenor.com/view/ree-pepe-triggered-angry-ahhhh-gif-13627544",
        )

        await ctx.send(embed=embed)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def cc(self, ctx, *, message: str):
        """
        usage = add a specialCommand
        syntax = [command name] || [reply]
        """

        # Split the command and the reply
        # and send it back to remain as a final confirmation

        await ctx.send(message.split("||"))

        # split the command and reply and strip of ending and beginning whitespace
        command, reply = message.split("||")[0].strip(), message.split("||")[1].strip()
        # sent the command as the key and reply as the value
        self.Dictwithstuff[command] = reply

        # send the final dictionary as a confirm
        await ctx.send(self.Dictwithstuff)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sc(self, ctx):
        """save the entire dictonary"""

        # just in case the owner cc'ed the thing and regretted it, the final method to actually save it is different
        await ctx.send(self.Dictwithstuff)
        with open("NoPref.json", "w") as f:
            f.write(json.dumps(self.Dictwithstuff))

    @commands.command()
    async def ImgToAscii(self, ctx):
        """
        Turns an image to ascii and sends a file containing the result

        syntax = ?imgtoascii (you can add an image or it'll convert your avatar)
        """
        import random

        # import the ToAscii class handling the ascii gen
        from ToAscii import ToAscii

        message = ctx.message
        # make a random name to save the image as
        name = f"{random.randint(1,10000)}.png"
        # init the class
        returnstr = ToAscii()

        # if it has an attachment save it
        # else grab and save the profile pic

        # the image gets deleted in the ToAscii class after we're done with it btw
        if message.attachments:
            await message.attachments[0].save(name)
        else:
            await message.author.avatar.save(name)
        # make a text file with the random name
        with open(f"{name}.txt", "w") as f:
            # write
            f.write(returnstr.main(name))
            # aannd send
            await ctx.send(file=discord.File(f"{name}.txt"))
        # import os and remove said file
        import os

        os.remove(f"{name}.txt")

   
def setup(client):
    client.add_cog(Fun(client))
