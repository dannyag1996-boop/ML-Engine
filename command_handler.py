from profiles_handler import ProfilesHandler
from core_engine import CoreBattleEngine
from ui_handler import UIHandler
from cities import Cities
from dictionary import clean_input, normalize_stat, format_val
from troops_calc import TroopsCalc
from xp_handler import XPHandler
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

profiles = ProfilesHandler()
engine = CoreBattleEngine()
ui = UIHandler()

class CommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_prefix_command(self, ctx, parts: list):
        cmd = parts[0].lower()
        args = parts[1:]
        try:
            if cmd == "sim":
                result = self._parse_sim(args)
                embed = ui.create_battle_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "ap":
                result = self._parse_ap(args)
                embed = ui.create_ap_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "calc":
                result = self._parse_calc(args)
                embed = ui.create_calc_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "farm":
                result = engine.optimize_farm(args)
                embed = ui.create_farm_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "plan":
                result = engine.optimize_leveling_plan(args)
                embed = ui.create_level_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "sui":
                result = engine.sui_calc(self._parse_sui(args))
                embed = ui.create_sui_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "xp":
                result = engine.calculate_xp(args)
                embed = ui.create_xp_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "cost":
                # Prefix uses same order as slash (amount start target) → swap for engine
                result = engine.bulk_cost_calc([args[1] if len(args)>1 else "1", args[2] if len(args)>2 else "10", args[0] if len(args)>0 else "1"])
                embed = ui.create_bulk_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "drain":
                result = engine.drain_calc(args)
                embed = ui.create_drain_embed(result)
                await ctx.send(embed=embed)
            elif cmd in ["setprofile", "adjustother", "adjustperm", "profile2", "useprofile", "noprofile", "clear", "profile", "permissions", "allprofiles", "attackers", "builders", "assign"]:
                await ctx.send("Profiles phase skipped for now.")
            elif cmd == "help" or cmd == "commands":
                await self.show_help(ctx)
            else:
                await ctx.send(f"Unknown command `{cmd}`. Use `$help`.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

    def _parse_calc(self, args):
        return args

    def _parse_sim(self, args):
        city_level = int(clean_input(args[0], True)) if len(args) > 0 else 115
        at_troops = clean_input(args[1], False) if len(args) > 1 else 0.0
        striker = clean_input(args[2], True) if len(args) > 2 else 0.0
        scav = clean_input(args[3], True) if len(args) > 3 else 0.0
        dt_troops = clean_input(args[4], False) if len(args) > 4 else 0.0
        guardian = clean_input(args[5], True) if len(args) > 5 else 0.0
        salv = clean_input(args[6], True) if len(args) > 6 else 0.0
        fearless = clean_input(args[7], True) if len(args) > 7 else 75.0
        result = engine.simulate_battle(at_troops=at_troops, striker=striker, scav=scav, fearless=fearless, dt_troops=dt_troops, guardian=guardian, salv=salv, brave=fearless, city_level=city_level)
        return result

    def _parse_ap(self, args):
        troops = clean_input(args[0], False) if len(args) > 0 else 0.0
        striker = clean_input(args[1], True) if len(args) > 1 else 0.0
        ap = TroopsCalc.attacker_power(troops, striker)
        max_city = 1
        for lvl in range(1, 201):
            if ap > Cities.get_cw_val(lvl):
                max_city = lvl
            else:
                break
        return {"ap": ap, "max_city": max_city, "formatted_ap": format_val(ap), "formatted_troops": format_val(troops), "striker": striker}

    def _parse_sui(self, args):
        dt_troops = clean_input(args[0] if len(args) > 0 else 0, False)
        guardian = clean_input(args[1] if len(args) > 1 else 0, True)
        at_troops = clean_input(args[2] if len(args) > 2 else 0, False)
        salv = clean_input(args[3] if len(args) > 3 else 0, True)
        target_pct = clean_input(args[4] if len(args) > 4 else 90, True)
        return [dt_troops, guardian, at_troops, salv, target_pct]

    async def show_help(self, ctx):
        embed = discord.Embed(title="All Commands", color=0x3498db)
        embed.add_field(name="Battle", value="$sim $ap $calc $farm $plan $sui $xp $cost $drain", inline=False)
        embed.add_field(name="Profiles", value="Skipped for now", inline=False)
        embed.add_field(name="Help", value="$help $commands", inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(name="ap", description="Calculate Attack Power")
    @app_commands.describe(troops="Troops (e.g. 456g)", striker="Striker bonus %")
    async def slash_ap(self, interaction: discord.Interaction, troops: str, striker: float = 0.0):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        result = self._parse_ap([troops, str(striker)])
        embed = ui.create_ap_embed(result)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="calc", description="Run full battle calc with optimizer")
    @app_commands.describe(gold="Attacker gold (e.g. 450g)", troops="Attacker troops", city_level="Defender city level", defender_troops="Defender troops", mode="Mode (max/even)", cautious="Cautious %")
    async def slash_calc(self, interaction: discord.Interaction, gold: str, troops: str, city_level: int, defender_troops: str, mode: str = "even", cautious: float = 90.0):
        await interaction.response.defer()
        await asyncio.sleep(0.8)
        try:
            result = engine.optimize_calc(gold, troops, city_level, defender_troops, mode, cautious)
            embed = ui.create_calc_embed(result)
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"Error: {str(e)}")

    @app_commands.command(name="farm", description="Cities needed to level up")
    @app_commands.describe(current_level="Current player level", city_level="City level to farm", modifier="Modifier % (50/100/150/200)")
    async def slash_farm(self, interaction: discord.Interaction, current_level: int, city_level: int, modifier: float = 100.0):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        result = engine.optimize_farm([str(current_level), str(city_level), str(modifier)])
        embed = ui.create_farm_embed(result)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="plan", description="Leveling plan (was /level)")
    @app_commands.describe(current_level="Current player level", target_level="Target level")
    async def slash_level(self, interaction: discord.Interaction, current_level: int, target_level: int):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        result = engine.optimize_leveling_plan([str(current_level), str(target_level)])
        embed = ui.create_level_embed(result)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="sui", description="SUI calculator")
    @app_commands.describe(defender_troops="Defender troops", attacker_troops="Attacker troops", guardian="Guardian %", salvager="Salvager %", target_loss="Target loss %")
    async def slash_sui(self, interaction: discord.Interaction, defender_troops: str, attacker_troops: str, guardian: float = 0.0, salvager: float = 0.0, target_loss: float = 90.0):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        result = engine.sui_calc(self._parse_sui([defender_troops, str(guardian), attacker_troops, str(salvager), str(target_loss)]))
        embed = ui.create_sui_embed(result)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="xp", description="XP calculator")
    @app_commands.describe(cities_hit="Cities hit", city_level="City level", modifier="Modifier %")
    async def slash_xp(self, interaction: discord.Interaction, cities_hit: int, city_level: int, modifier: float = 100.0):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        result = engine.calculate_xp([str(cities_hit), str(city_level), str(modifier)])
        embed = ui.create_xp_embed(result)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="cost", description="Bulk upgrade cost (was /bulk)")
    @app_commands.describe(
        amount="Amount of cities",
        start_level="Starting city level",
        target_level="Target city level"
    )
    async def slash_bulk(self, interaction: discord.Interaction, amount: int, start_level: int, target_level: int):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        # FIXED: Pass list in engine-expected order [start, target, amount]
        result = engine.bulk_cost_calc([str(start_level), str(target_level), str(amount)])
        embed = ui.create_bulk_embed(result)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="drain", description="Cautious-only drain simulation")
    @app_commands.describe(start_level="Starting city level", target_level="Target city level", gold_stock="Defender gold stock", cautious="Cautious %")
    async def slash_drain(self, interaction: discord.Interaction, start_level: int, target_level: int, gold_stock: str, cautious: float = 50.0):
        await interaction.response.defer()
        await asyncio.sleep(0.5)
        result = engine.drain_calc([str(start_level), str(target_level), gold_stock, str(cautious)])
        embed = ui.create_drain_embed(result)
        await interaction.followup.send(embed=embed)

# End of file