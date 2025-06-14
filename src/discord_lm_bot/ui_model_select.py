# File purpose: Discord UI View that lets a user pick gpt-4o or o3.
import discord
from .database import set_user_setting


class ModelSelect(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=60)
        self.user_id = user_id

    @discord.ui.select(
        placeholder="Choose your preferred model…",
        options=[
            discord.SelectOption(label="gpt-4o", description="Latest & smartest"),
            discord.SelectOption(label="o3", description="Fast & efficient"),
        ],
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        choice = select.values[0]
        set_user_setting(self.user_id, "active_model", choice)
        await interaction.response.edit_message(
            content=f"✅ Your model is now **{choice}**",
            view=None,
        )
