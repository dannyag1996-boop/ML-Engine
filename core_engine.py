from battle_resolution import BattleResolution
from cities import Cities
from xp_handler import XPHandler
from optimizer import BattleOptimizer
from profiles_handler import ProfilesHandler
from dictionary import clean_input

profiles = ProfilesHandler()

class CoreBattleEngine:
    def __init__(self):
        self.optimizer = BattleOptimizer()
        self.battle_cache = {}  # Upgrade 3: simple cache

    def get_profile_stats(self, profile_name: str, side: str = "defender"):
        if side == "defender":
            return profiles.get_defender_stats(profile_name)
        return profiles.get_attacker_stats(profile_name)

    def simulate_battle(self, at_troops=0.0, striker=0.0, scav=0.0, fearless=75.0,
                        dt_troops=0.0, guardian=0.0, salv=0.0, brave=75.0,
                        city_level=1):
        key = (round(at_troops, 1), round(striker, 1), round(dt_troops, 1), round(guardian, 1), round(salv, 1), city_level)
        if key in self.battle_cache:
            return self.battle_cache[key]

        if at_troops < 0: at_troops = 0.0
        if dt_troops < 0: dt_troops = 0.0
        if city_level < 1: city_level = 1

        result = BattleResolution.full_battle_result(
            at_troops=at_troops, striker=striker, scav=scav, fearless=fearless,
            dt_troops=dt_troops, guardian=guardian, salv=salv, brave=brave,
            city_level=city_level
        )

        cl = city_level
        result['cost_5'] = Cities.get_cc_val(cl) - Cities.get_cc_val(max(1, cl-5))
        result['cost_10'] = Cities.get_cc_val(cl) - Cities.get_cc_val(max(1, cl-10))
        result['cost_15'] = Cities.get_cc_val(cl) - Cities.get_cc_val(max(1, cl-15))
        result['cost_full'] = Cities.get_cc_val(cl)
        result['cautious_5'] = result['cost_5'] * 0.5
        result['cautious_10'] = result['cost_10'] * 0.5
        result['cautious_15'] = result['cost_15'] * 0.5
        result['cautious_full'] = result['cost_full'] * 0.5
        result['salve_profit_5'] = result.get('salvager_gold', 0) - result['cautious_5']
        result['salve_profit_10'] = result.get('salvager_gold', 0) - result['cautious_10']
        result['salve_profit_15'] = result.get('salvager_gold', 0) - result['cautious_15']
        result['salve_profit_full'] = result.get('salvager_gold', 0) - result['cautious_full']

        self.battle_cache[key] = result
        return result

    def optimize_calc(self, args):
        return self.optimizer.optimize_calc(args)

    def optimize_farm(self, args):
        return self.optimizer.optimize_farm(args)

    def optimize_leveling_plan(self, args):
        return self.optimizer.optimize_leveling_plan(args)

    def sui_calc(self, args):
        return self.optimizer.sui_calc(args)

    def bulk_cost_calc(self, args):
        start = int(clean_input(args[0] if len(args) > 0 else 1, True))
        target = int(clean_input(args[1] if len(args) > 1 else 10, True))
        num = int(clean_input(args[2] if len(args) > 2 else 1, True))
        raw_total, _ = Cities.total_gold_multiple_cities(start, target, num)
        return {"total_cost": round(raw_total, 1), "cities": num, "start_level": start, "target_level": target}

    def drain_calc(self, args):
        start_level = int(clean_input(args[0] if len(args) > 0 else 1, True))
        target_level = int(clean_input(args[1] if len(args) > 1 else start_level + 1, True))
        gold_stock = Cities.parse_gold_float(args[2] if len(args) > 2 else "0")
        cautious_pct = clean_input(args[3] if len(args) > 3 else 50, True)

        cost = Cities.gold_required_for_upgrade(start_level, target_level)
        cautious_return = Cities.get_cc_val(target_level) * (cautious_pct / 100)
        cycles = 0
        current_gold = gold_stock
        while current_gold >= cost:
            current_gold -= cost
            current_gold += cautious_return
            cycles += 1
        return {
            "cycles_completed": cycles,
            "final_gold": round(current_gold, 1),
            "cost_per_cycle": cost,
            "cautious_return_per_cycle": round(cautious_return, 1),
            "starting_level": start_level,
            "target_level": target_level
        }

    def calculate_xp(self, args):
        return XPHandler.calculate_xp(args)