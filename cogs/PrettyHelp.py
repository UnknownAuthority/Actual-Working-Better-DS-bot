import discord
from discord.ext import commands

class MyHelpCommand(commands.MinimalHelpCommand):
  async def send_command_help(self, command):
    embed = discord.Embed(title=self.get_command_signature(command), colour=discord.Colour.green())
    embed.add_field(name="Usage", value=command.help)
    alias= command.aliases
    if alias:
      embed.add_field(name="Aliases", value= ", ".join(alias), inline=False)
    channel = self.get_destination()
    await channel.send(embed=embed)
 
  async def send_bot_help(self, mapping):
    channel = self.get_destination()
    for x,y in mapping.items():
      arr = []
      for i in y:
        try:
          if not i.hidden:
            arr.append(i.name)
        except:
          arr.append(i.name)
      mapping[x] = arr
    await channel.send(embed = discord.Embed(title="Module contents appear here", description="Commands appear here, use ?help <command> to get more info on them", colour = discord.Colour.green()) ,view=HelpSelectDropdownView(message=channel, mapping=mapping))
    



class PrettyHelp(commands.Cog):
  def __init__(self, client):
    self._original_help_command = client.help_command
   
    client.help_command = MyHelpCommand()
    
    client.help_command.cog = self
  
  def cog_unload(self):
    self.client.help_command = self._original_help_command      

        
class HelpSelectDropdown(discord.ui.Select):
  def __init__(self, message, mapping):
      self.name_and_command = []
      for cog, commands in mapping.items():
        
        if commands:
         
          arr = [getattr(cog, "qualified_name", "No Category"),commands]
         
          self.name_and_command.append(arr)
      options = []
      for i in self.name_and_command:
 
        options.append(discord.SelectOption(label=i[0], description=i[0]))
  
       
      super().__init__(
            placeholder="Choose the module you want",
            min_values=1,
            max_values=1,
            options=options,
        )
  def embedGen(self, name, commands):
    return discord.Embed(title=name, description=" ".join(commands), colour = discord.Colour.green())
    
  async def callback(self, interaction: discord.Interaction):
    for nameCommand in self.name_and_command:
      if nameCommand[0] == self.values[0]:
        await interaction.message.edit(embed=self.embedGen(nameCommand[0], nameCommand[1]))
class HelpSelectDropdownView(discord.ui.View):
  def __init__(self, message, mapping):
    super().__init__()
    self.add_item(HelpSelectDropdown(message=message,mapping=mapping))


def setup(client):
  client.add_cog(PrettyHelp(client))