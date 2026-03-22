import discord
from dictionary import (
    EMOJI_CITY, EMOJI_ATTACK, EMOJI_DEFENSE, EMOJI_TROOPS,
    EMOJI_STRIKER, EMOJI_GUARDIAN, EMOJI_SALVE, EMOJI_SCAV,
    EMOJI_FEARLESS, EMOJI_BATTLE, EMOJI_CAUTIOUS, DIVIDER,
    format_val
)

BRIGHT_BLOOD_RED = 0xC8102E

class UIHandler:
    @staticmethod
    def create_battle_embed(result):
        cl = result.get('city_level', 1)
        embed = discord.Embed(
            title=f"{EMOJI_CITY} City {cl} | Total Defense: {format_val(result.get('dp', 0))}",
            description=f"Wall: {format_val(result.get('cw', 0))} | Troops & Guard: {format_val(result.get('dp', 0) - result.get('cw', 0))}",
            color=BRIGHT_BLOOD_RED
        )
        embed.add_field(name=f"{EMOJI_BATTLE} Battle Report", value=(
            f"{EMOJI_ATTACK} **{format_val(result.get('ap', 0))} AP** | {EMOJI_STRIKER} {result.get('striker', 0):.0f}%\n"
            f"{EMOJI_TROOPS} **{format_val(result.get('at_troops', 0))}** → **{format_val(result.get('at_troops', 0) - result.get('attacker_killed', 0))}** ☠️ **{format_val(result.get('attacker_killed', 0))}** (-{result.get('at_loss_pct', 0):.1f}%)\n"
            f"{EMOJI_FEARLESS} 90%: **{format_val(result.get('rev_a90', 0))}** | 75%: **{format_val(result.get('rev_a75', 0))}**\n"
            f"{EMOJI_SCAV} 162%: **{format_val(result.get('scav_162', 0))}** | 144%: **{format_val(result.get('scav_144', 0))}**\n\u200b"
        ), inline=False)
        embed.add_field(name=f"{EMOJI_DEFENSE} {format_val(result.get('dp', 0))} DP | {EMOJI_GUARDIAN} {result.get('guardian', 0):.0f}%", value=(
            f"{EMOJI_TROOPS} **{format_val(result.get('dt_troops', 0))}** → **{format_val(result.get('dt_troops', 0) - result.get('defender_killed', 0))}** ☠️ **{format_val(result.get('defender_killed', 0))}** (-{result.get('dt_loss_pct', 0):.1f}%)\n"
            f"{EMOJI_FEARLESS} 90%: **{format_val(result.get('rev_d90', 0))}** | 75%: **{format_val(result.get('rev_d75', 0))}**\n"
            f"{EMOJI_SALVE} {result.get('salv', 0):.0f}%: **{format_val(result.get('salvager_gold', 0))}**\n{DIVIDER}"
        ), inline=False)
        embed.add_field(name="Cost From Level | Cautious | Salve Profit", value=(
            f"Lvl {max(1, cl-5)} → **{format_val(result.get('cost_5', 0))}** | {EMOJI_CAUTIOUS} **{format_val(result.get('cautious_5', 0))}** | {EMOJI_SALVE}**{ '+' if result.get('salve_profit_5', 0) >= 0 else ''}{format_val(result.get('salve_profit_5', 0))}**\n"
            f"Lvl {max(1, cl-10)} → **{format_val(result.get('cost_10', 0))}** | {EMOJI_CAUTIOUS} **{format_val(result.get('cautious_10', 0))}** | {EMOJI_SALVE}**{ '+' if result.get('salve_profit_10', 0) >= 0 else ''}{format_val(result.get('salve_profit_10', 0))}**\n"
            f"Lvl {max(1, cl-15)} → **{format_val(result.get('cost_15', 0))}** | {EMOJI_CAUTIOUS} **{format_val(result.get('cautious_15', 0))}** | {EMOJI_SALVE}**{ '+' if result.get('salve_profit_15', 0) >= 0 else ''}{format_val(result.get('salve_profit_15', 0))}**\n"
            f"Lvl 1 → **{format_val(result.get('cost_full', 0))}** | {EMOJI_CAUTIOUS} **{format_val(result.get('cautious_full', 0))}** | {EMOJI_SALVE}**{ '+' if result.get('salve_profit_full', 0) >= 0 else ''}{format_val(result.get('salve_profit_full', 0))}**"
        ), inline=False)
        embed.set_footer(text=f"Troops+Guard = {result.get('defender_troop_pct', 0):.1f}% of Total Defense")
        return embed

    @staticmethod
    def create_calc_embed(result):
        battle_data = result.get('full_result', result)
        embed = UIHandler.create_battle_embed(battle_data)
        embed.title = f"{EMOJI_CITY} City {battle_data.get('city_level', 1)} | Total Defense: {format_val(battle_data.get('dp', 0))}"
        embed.color = BRIGHT_BLOOD_RED
        opt_dt = format_val(result.get('defender_troops', battle_data.get('dt_troops', 0)))
        embed.description = f"**Optimal Defender Troops:** {opt_dt}\n\n" + (embed.description or "")
        rec = result.get('recommended')
        if rec:
            saves = result.get('main_defender_troops', 0) - rec.get('defender_troops', 0)
            recommended_text = (
                f"Stats: **{rec.get('salvager', 0):.1f}%**