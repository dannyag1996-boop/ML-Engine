from profiles_handler import ProfilesHandler
from core_engine import CoreBattleEngine
from ui_handler import UIHandler
from cities import Cities
from dictionary import clean_input, normalize_stat, format_val
from troops_calc import TroopsCalc
from xp_handler import XPHandler  # ← Added (fixes /farm /xp /cityxp)
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
            elif cmd == "level":
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
            elif cmd == "bulk":
                result = engine.bulk_cost_calc(args)
                embed = ui.create_bulk_embed(result)
                await ctx.send(embed=embed)
            elif cmd == "drain":
                result = engine.drain_calc(args)
                embed = ui.create_drain_embed(result)
                await ctx.send(embed=embed)
            # Profile commands (skipped phase) - now have placeholders
            elif cmd == "setprofile":
                await self._set_profile(ctx, args)
            elif cmd == "adjustother":
                await self._adjust_other(ctx, args)
            elif cmd == "adjustperm":
                await self._adjust_perm(ctx, args)
            elif cmd == "profile2":
                await self._profile2(ctx, args)
            elif cmd == "useprofile":
                await self._use_profile(ctx, args)
            elif cmd == "noprofile":
                await self._noprofile(ctx)
            elif cmd == "clear":
                await self._clear(ctx, args)
            elif cmd == "profile":
                await self._profile(ctx, args)
            elif cmd == "permissions":
                await self._permissions(ctx, args)
            elif cmd == "allprofiles":
                await self._allprofiles(ctx)
            elif cmd == "attackers":
                await self._attackers(ctx)
            elif cmd == "builders":
                await self._builders(ctx)
            elif cmd == "assign":
                await self._assign(ctx, args)
            elif cmd == "help" or cmd == "commands":
                await self.show_help(ctx)
            else:
                await ctx.send(f"❌ Unknown command `{cmd}`. Use `$help`.")
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

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

    # === Placeholder methods for skipped profile phase ===
    async def _set_profile(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _adjust_other(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _adjust_perm(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _profile2(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _use_profile(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _noprofile(self, ctx): await ctx.send("❌ Profiles phase skipped for now.")
    async def _clear(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _profile(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _permissions(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    async def _allprofiles(self, ctx): await ctx.send("❌ Profiles phase skipped for now.")
    async def _attackers(self, ctx): await ctx.send("❌ Profiles phase skipped for now.")
    async def _builders(self, ctx): await ctx.send("❌ Profiles phase skipped for now.")
    async def _assign(self, ctx, args): await ctx.send("❌ Profiles phase skipped for now.")
    # =======================================================

    async def show_help(self, ctx):
        embed = discord.Embed(title="All Commands", color=0x3498db)
        embed.add_field(name="Battle", value="$sim $ap $calc $farm $level $sui $xp $bulk $drain", inline=False)
        embed.add_field(name="Profiles", value="$setprofile $adjustother $adjustperm $profile2 $useprofile $noprofile $clear $profile $permissions $allprofiles $attackers $builders $assign", inline=False)
        embed.add_field(name="Help", value="$help $commands", inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(name="ap", description="Calculate Attack Power")
    @app_commands.describe(troops="Troops (e.g. 456g)", striker="Striker %")
    async def slash_ap(self, interaction: discord.Interaction, troops: str, striker: float = 0.0):
        result = self._parse_ap([troops, str(striker)])
        embed = ui.create_ap_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sim", description="Run battle simulation")
    @app_commands.describe(city_level="City level", attacker_troops="Attacking troops", striker="Striker %", scavenger="Scavenger %", defender_troops="Defending troops", guardian="Guardian %", salvager="Salvager %", revival="Revival %")
    async def slash_sim(self, interaction: discord.Interaction, city_level: int = 115, attacker_troops: str = "325g", striker: float = 550.0, scavenger: float = 162.0, defender_troops: str = "105g", guardian: float = 140.0, salvager: float = 321.0, revival: float = 75.0):
        args = [str(city_level), attacker_troops, str(striker), str(scavenger), defender_troops, str(guardian), str(salvager), str(revival)]
        result = self._parse_sim(args)
        embed = ui.create_battle_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="calc", description="Optimization - Max or Even mode")
    @app_commands.describe(
        attacker_troops="Attacking troops (e.g. 450g)",
        striker="Striker %",
        guardian="Guardian %",
        salvager="Salvager %",
        mode="Mode: max or even",
        acceptable_loss="Acceptable attacker loss % before revive (default 25)"
    )
    async def slash_calc(self, interaction: discord.Interaction, attacker_troops: str, striker: float = 778.0, guardian: float = 140.0, salvager: float = 321.0, mode: str = "max", acceptable_loss: float = 25.0):
        await interaction.response.defer()
        args = [attacker_troops, str(striker), str(guardian), str(salvager), mode, str(acceptable_loss)]
        result = engine.optimize_calc(args)
        embed = ui.create_calc_embed(result)
        
        await asyncio.sleep(0.8)
        try:
            await interaction.followup.send(embed=embed)
        except discord.errors.HTTPException as e:
            if "429" in str(e):
                await asyncio.sleep(1.5)
                await interaction.followup.send(embed=embed)
            else:
                raise

    @app_commands.command(name="farm", description="Cities needed to level up")
    @app_commands.describe(current_level="Current character level", city_level="City level to hit", modifier="XP modifier %")
    async def slash_farm(self, interaction: discord.Interaction, current_level: int = 1, city_level: int = 115, modifier: float = 100.0):
        result = XPHandler.calculate_cities_needed_to_level_up(current_level, city_level, modifier)
        embed = ui.create_farm_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sui", description="Suicide Optimization")
    @app_commands.describe(defender_troops="Defender troops (required)", guardian="Guardian % (required)", attacker_troops="Attacker troops for suicide calc (optional)", salvager="Salvager % (optional)", target_pct="Target defense % (default 90)")
    async def slash_sui(self, interaction: discord.Interaction, defender_troops: str, guardian: float, attacker_troops: str = "0", salvager: float = 0.0, target_pct: float = 90.0):
        result = engine.sui_calc([defender_troops, str(guardian), attacker_troops, str(salvager), str(target_pct)])
        embed = ui.create_sui_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="xp", description="Cumulative XP for X cities")
    @app_commands.describe(cities="Number of cities", city_level="City level", modifier="XP modifier %")
    async def slash_xp(self, interaction: discord.Interaction, cities: int = 5, city_level: int = 115, modifier: float = 100.0):
        result = XPHandler.calculate_cumulative_xp(cities, city_level, modifier)
        embed = ui.create_xp_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cityxp", description="Single city XP")
    @app_commands.describe(city_level="City level", modifier="XP modifier %")
    async def slash_cityxp(self, interaction: discord.Interaction, city_level: int = 115, modifier: float = 100.0):
        result = XPHandler.calculate_single_city_xp(city_level, modifier)
        embed = ui.create_xp_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bulk", description="Bulk Upgrade Report")
    @app_commands.describe(quantity="Quantity", from_level="From level", to_level="To level")
    async def slash_bulk(self, interaction: discord.Interaction, quantity: int = 1, from_level: int = 1, to_level: int = 10):
        result = engine.bulk_cost_calc([str(from_level), str(to_level), str(quantity)])
        embed = ui.create_bulk_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="drain", description="Drain cycle simulation")
    @app_commands.describe(start_level="Starting city level", target_level="Target city level", gold_stock="Gold stock (e.g. 500g)", cautious_pct="Cautious %")
    async def slash_drain(self, interaction: discord.Interaction, start_level: int = 1, target_level: int = 10, gold_stock: str = "100g", cautious_pct: float = 50.0):
        args = [str(start_level), str(target_level), gold_stock, str(cautious_pct)]
        result = engine.drain_calc(args)
        embed = ui.create_drain_embed(result)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="level", description="Leveling Plan")
    @app_commands.describe(attacker_troops="Attacking troops", striker="Striker %", current_level="Current level")
    async def slash_level(self, interaction: discord.Interaction, attacker_troops: str, striker: float = 550.0, current_level: int = 1):
        result = engine.optimize_leveling_plan([attacker_troops, str(striker), str(current_level)])
        embed = ui.create_level_embed(result)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandHandler(bot))
