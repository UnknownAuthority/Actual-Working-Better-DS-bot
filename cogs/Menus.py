import discord
from discord.ext import commands

class Menus(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.command()
  async def role(self,ctx,roleType: str = "group"):
    """Gives you a list of desired roles according to keywords, eg: group, Team
      if you want to access study groups just go ?role group, for teams "?role Team"
    default value, = group
    """
    view = RoleSelectDropdownView(ctx=ctx,roleType=roleType)
    try:
      await ctx.send("Pick your role", view=view)
    except discord.HTTPException:
      await ctx.send("We either cannot give you that role or those kinds of roles do not exist")




class RoleSelectDropdown(discord.ui.Select):
  def __init__(self, ctx, roleType):
    # get all roles we wanna get, roles of groups eg: C# study groups
    # dependant on string search if the role contains said string
    # eg: roleType = study, so all roles with study in em will be listed
    # along with a perms check to see if they don't have moderation powers of course
    lowest =  discord.utils.get(ctx.guild.roles, name="@everyone")
   
    self.availableRoles = [role for role in ctx.guild.roles if roleType.lower() in role.name.lower() and role.permissions == lowest.permissions]
   
    options = [discord.SelectOption(label= role.name, description=role.name, emoji="🟦") for role in self.availableRoles]
   
    super().__init__(
            placeholder="Choose the role you want",
            min_values=1,
            max_values=1,
            options=options,
        )

  async def callback(self, interaction: discord.Interaction):
    for role in self.availableRoles:
      if role.name == self.values[0]:
        await interaction.user.add_roles(role, reason="They asked for it")

class RoleSelectDropdownView(discord.ui.View):
    def __init__(self, ctx, roleType):
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(RoleSelectDropdown(ctx=ctx,roleType=roleType))

def setup(client):
    client.add_cog(Menus(client))



    
    


