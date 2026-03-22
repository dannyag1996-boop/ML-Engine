import discord
from dictionary import (
    EMOJI_CITY, EMOJI_ATTACK, EMOJI_DEFENSE, EMOJI_TROOPS,
    EMOJI_STRIKER, EMOJI_GUARDIAN, EMOJI_SALVE, EMOJI_SCAV,
    EMOJI_FEARLESS, EMOJI_BATTLE, EMOJI_CAUTIOUS, DIVIDER,
    format_val
)

BRIGHT_BLOOD_RED = 0xC8102E

class UIHandler:
    # ... (all other embeds unchanged - battle, calc, ap, farm, level, sui, xp, bulk, profile, permissions, allprofiles remain exactly as before)

    @staticmethod
    def create_drain_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CAUTIOUS} Cautious-Only Build", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Result", value=(
            f"**{result.get('cycles_completed', 0)}** cities upgraded at **{format_val(result.get('cost_per_cycle', 0))}**, "
            f"with **{format_val(result.get('cautious_return_per_cycle', 0))}** returned each hit.\n"
            f"Started at level **{result.get('starting_level', 1)}** → Target **{result.get('target_level', 1)}**\n"
            f"Final gold left: **{format_val(result.get('final_gold', 0))}**"
        ), inline=False)
        embed.set_footer(text="drain powered by MLE")
        return embed

    # (the rest of the file is unchanged - all other methods are identical to the last version)