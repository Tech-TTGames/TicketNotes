"""General settings cog."""
import logging

import discord
from discord import app_commands
from discord.ext import commands

from tickets_plus import TicketsPlus


@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
class Settings(commands.GroupCog, name="settings", description="Settings for the bot."):
    """Provides commands to change the bot's settings."""

    def __init__(self, bot: TicketsPlus):
        self._bt = bot
        super().__init__()
        logging.info("Loaded %s", self.__class__.__name__)

    @app_commands.command(name="tracked", description="Change the tracked users.")
    @app_commands.describe(user="The user to track/untrack.")
    async def change_tracked(self, ctx: discord.Interaction, user: discord.User):
        """
        This command is used to change the tracked users.
        If a user is already tracked, they will be untracked.
        """
        async with self._bt.get_connection() as conn:
            new, ticket_user = await conn.get_ticket_user(user.id, ctx.guild.id)  # type: ignore
            if not new:
                await conn.delete(ticket_user)
                text = f"Untracked {user.mention}"
            else:
                text = f"Tracked {user.mention}"
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(text, ephemeral=True)

    @app_commands.command(name="staff", description="Change the staff roles.")
    @app_commands.describe(role="The role to add/remove from staff roles.")
    async def change_staff(self, ctx: discord.Interaction, role: discord.Role):
        """
        This command is used to change the staff roles, Staff are allowed to use staff commands.
        If a role is already here, it will be removed.
        """
        async with self._bt.get_connection() as conn:
            new, staff_role = await conn.get_staff_role(role.id, ctx.guild.id)  # type: ignore
            if not new:
                await conn.delete(staff_role)
                text = f"Removed {role.mention} from staff roles."
            else:
                text = f"Added {role.mention} to staff roles."
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(text, ephemeral=True)

    @app_commands.command(name="observers", description="Change the observers roles.")
    @app_commands.describe(role="The role to add/remove from observers roles.")
    async def change_observers(self, ctx: discord.Interaction, role: discord.Role):
        """
        This command is used to change the observers roles, which are pinged one new notes threads.
        If a role is already here, it will be removed.
        """
        async with self._bt.get_connection() as conn:
            new, obsrvrs = await conn.get_staff_role(role.id, ctx.guild.id)  # type: ignore
            if not new:
                await conn.delete(obsrvrs)
                text = f"Removed {role.mention} from ping staff roles."
            else:
                text = f"Added {role.mention} to ping staff roles."
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(text, ephemeral=True)

    @app_commands.command(
        name="communitysupport", description="Change the community support roles."
    )
    @app_commands.describe(role="The role to add/remove from community support roles.")
    async def change_community_roles(
        self, ctx: discord.Interaction, role: discord.Role
    ):
        """
        This command is used to change the community support roles,
        COMSUP roles are added to channels side-by-side without any perms.
        If a role is already here, it will be removed.
        """
        async with self._bt.get_connection() as conn:
            new, comsup = await conn.get_community_role(role.id, ctx.guild.id)  # type: ignore
            if not new:
                await conn.delete(comsup)
                text = f"Removed {role.mention} from community support roles."
            else:
                text = f"Added {role.mention} to community support roles."
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(text, ephemeral=True)

    @app_commands.command(name="openmsg", description="Change the open message.")
    @app_commands.describe(message="The new open message.")
    async def change_openmsg(self, ctx: discord.Interaction, message: str):
        """This command is used to change the open message."""
        async with self._bt.get_connection() as conn:
            guild = await conn.get_guild(ctx.guild.id)  # type: ignore
            guild.open_message = message
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(
            f"Open message is now {message}", ephemeral=True
        )

    @app_commands.command(
        name="staffteamname", description="Change the staff team's name."
    )
    @app_commands.describe(name="The new staff team's name.")
    async def change_staffteamname(self, ctx: discord.Interaction, name: str):
        """This command is used to change the staff team's name."""
        async with self._bt.get_connection() as conn:
            guild = await conn.get_guild(ctx.guild.id)  # type: ignore
            guild.staff_team_name = name
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(f"Staff team is now {name}", ephemeral=True)

    @app_commands.command(
        name="msgdiscovery", description="Toggle message link discovery."
    )
    async def toggle_msg_discovery(self, ctx: discord.Interaction):
        """This command is used to toggle message link discovery."""
        async with self._bt.get_connection() as conn:
            guild = await conn.get_guild(ctx.guild.id)  # type: ignore
            new_status = not guild.msg_discovery
            guild.msg_discovery = new_status
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(
            f"Message link discovery is now {new_status}",
            ephemeral=True,
        )

    @app_commands.command(name="stripbuttons", description="Toggle button stripping.")
    async def toggle_button_stripping(self, ctx: discord.Interaction):
        """This command is used to toggle button stripping."""
        async with self._bt.get_connection() as conn:
            guild = await conn.get_guild(ctx.guild.id)  # type: ignore
            new_status = not guild.strip_buttons
            guild.strip_buttons = new_status
            await conn.commit()
            await conn.close()
        await ctx.response.send_message(
            f"Button stripping is now {new_status}",
            ephemeral=True,
        )


async def setup(bot: TicketsPlus):
    """Setup function for the cog."""
    await bot.add_cog(Settings(bot))
