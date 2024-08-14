from nextcord import Embed, Member
from discord.ext import commands
from bot_initialization import bot

class CogHookCommandsDefaults(commands.Cog):
        
    @bot.command(name="profile")
    async def profile(ctx, user: Member = None):
        if user == None:
            user = ctx.message.author
        inline = True
        embed = Embed(title=user.name+"#"+user.discriminator, color=0x0080ff)
        userData = {
            "Mention": user.mention,
            "Nick": user.nick,
            "Created at": user.created_at.strftime("%b %d, %Y, %T"),
            "Joined at": user.joined_at.strftime("%b %d, %Y, %T"),
            "Server": user.guild,
            "Top role": user.top_role
        }
        for [fieldName, fieldVal] in userData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=inline)
        embed.set_footer(text=f"id: {user.id}")

        embed.set_thumbnail(user.display_avatar)
        await ctx.send(embed=embed)

    @bot.command(name="server", pass_context=True)
    async def server(ctx):
        guild = ctx.message.author.guild
        inline = True
        embed = Embed(title=guild.name, color=0x0080ff)
        userData = {
            "Owner": guild.owner.mention,
            "Channels": len(guild.channels),
            "Members": guild.member_count,
            "Created at": guild.created_at.strftime("%b %d, %Y, %T"),
            "Description": guild.description,
        }
        for [fieldName, fieldVal] in userData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=inline)
        embed.set_footer(text=f"id: {guild.id}")

        embed.set_thumbnail(guild.icon)
        await ctx.send(embed=embed)
