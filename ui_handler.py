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
                f"Stats: **{rec.get('salvager', 0):.1f}%** {EMOJI_SALVE} / **{rec.get('guardian', 0):.1f}%** {EMOJI_GUARDIAN}\n"
                f"City Level: **{rec.get('city_level', 'N/A')}** | Defender Troops: **{format_val(rec.get('defender_troops', 0))}**\n"
                f"{EMOJI_SALVE} Salve Gold: **{format_val(rec.get('salvager_gold', 0))}**\n"
                f"Saves **\~{format_val(saves)}** troops per hit"
            )
            embed.add_field(name=f"{DIVIDER}\nRecommended for this City", value=recommended_text, inline=False)
        embed.set_footer(text=f"{embed.footer.text or ''}\ncalc powered by MLE")
        return embed

    @staticmethod
    def create_ap_embed(result):
        embed = discord.Embed(title=f"{EMOJI_ATTACK} Attack Power", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Input", value=f"{EMOJI_TROOPS} Troops: **{result.get('formatted_troops', '0')}**\n{EMOJI_STRIKER} Striker: **{result.get('striker', 0):.0f}%**", inline=False)
        embed.add_field(name="Results", value=f"{EMOJI_ATTACK} AP: **{format_val(result.get('ap', 0))}**\n{EMOJI_CITY} Max Empty City: **{result.get('max_city', 1)}**", inline=False)
        embed.set_footer(text="ap powered by MLE")
        return embed

    @staticmethod
    def create_farm_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CITY} Cities Needed to Level Up", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Result", value=(
            f"From level **{result.get('current_level', 1)}** you need **{result.get('cities_needed', 0)}** "
            f"cities at level **{result.get('city_level', 'the city level you inputted')}** to level up\n"
            f"XP per city: **{format_val(result.get('xp_per_city', 0))}**"
        ), inline=False)
        embed.set_footer(text="farm powered by MLE")
        return embed

    @staticmethod
    def create_level_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CITY} Leveling Plan", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Summary", value=f"Start: **{format_val(result.get('starting_troops', 0))}** | Hits: **{result.get('cities_hitted', 0)}** | Final Level: **{result.get('final_character_level', 1)}**", inline=False)
        embed.set_footer(text="level powered by MLE")
        return embed

    @staticmethod
    def create_sui_embed(result):
        embed = discord.Embed(title=f"{EMOJI_SALVE} Suicide Optimal City", color=BRIGHT_BLOOD_RED)
        value = (
            f"{EMOJI_CITY} City Level: **{result.get('city_level', 1)}**\n"
            f"{EMOJI_GUARDIAN} Guardian: **{result.get('guardian', 0):.0f}%**\n"
            f"{EMOJI_TROOPS} Troops: **{format_val(result.get('dt_troops', 0))}**\n"
            f"Troops & Guard make up **{result.get('troop_pct', 0):.1f}%** of Total Defense"
        )
        if result.get('salvager_gold', 0) > 0:
            value += f"\n{EMOJI_TROOPS} With a **{format_val(result.get('suicide_at_troops', 0))}** suicide, you'd earn {EMOJI_SALVE} **{format_val(result.get('salvager_gold', 0))}**"
        embed.add_field(name="Minimum city level to accept suicides on:", value=value, inline=False)
        embed.set_footer(text="sui powered by MLE")
        return embed

    @staticmethod
    def create_xp_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CITY} XP Calculator", color=BRIGHT_BLOOD_RED)
        if 'total_xp' in result:
            embed.add_field(name="Cumulative XP", value=f"**{format_val(result['total_xp'])}** XP from {result['cities']} cities at level {result['city_level']} (modifier **{result.get('modifier', 100):.0f}%**)", inline=False)
        elif 'xp' in result:
            embed.add_field(name="Single City XP", value=f"**{format_val(result['xp'])}** XP at city level {result['city_level']} (modifier **{result.get('modifier', 100):.0f}%**)", inline=False)
        embed.set_footer(text="xp powered by MLE")
        return embed

    @staticmethod
    def create_bulk_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CITY} Bulk Upgrade Report", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Details", value=f"Quantity: **{result.get('cities', 1)}**\nFrom **{result.get('start_level', 1)}** → **{result.get('target_level', 10)}**", inline=False)
        embed.add_field(name="Gold Cost", value=f"Per City: **{format_val(result.get('total_cost', 0) / result.get('cities', 1))}**\nTotal: **{format_val(result.get('total_cost', 0))}**\n{DIVIDER}\n{EMOJI_CAUTIOUS} Half Return: **{format_val(result.get('total_cost', 0) * 0.5)}**", inline=False)
        embed.set_footer(text="bulk powered by MLE")
        return embed

    @staticmethod
    def create_drain_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CAUTIOUS} Cautious-Only Build", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Result", value=(
            f"**{result.get('cycles_completed', 0)}** cities upgraded at **{format_val(result.get('cost_per_cycle', 0))}**, "
            f"with **{format_val(result.get('cautious_return_per_cycle', 0))}** returned each hit."
        ), inline=False)
        embed.set_footer(text="drain powered by MLE")
        return embed

    @staticmethod
    def create_profile_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CITY} Profile Information", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Data", value=str(result), inline=False)
        embed.set_footer(text="profile powered by MLE")
        return embed

    @staticmethod
    def create_permissions_embed(result):
        embed = discord.Embed(title=f"{EMOJI_GUARDIAN} Permissions", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="Users", value=str(result), inline=False)
        embed.set_footer(text="permissions powered by MLE")
        return embed

    @staticmethod
    def create_allprofiles_embed(result):
        embed = discord.Embed(title=f"{EMOJI_CITY} All Profiles", color=BRIGHT_BLOOD_RED)
        embed.add_field(name="List", value=", ".join(result) if result else "None", inline=False)
        embed.set_footer(text="allprofiles powered by MLE")
        return embed