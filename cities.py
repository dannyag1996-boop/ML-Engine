import math
from typing import Tuple

class Cities:
    @staticmethod
    def get_cc_val(lvl: int) -> float:
        if lvl < 1: return 0.0
        return 50 * (1.2 ** (lvl - 1) - 1)

    @staticmethod
    def get_cw_val(lvl: int) -> float:
        if lvl < 1: return 0.0
        return 70 * (1.2 ** (lvl - 1))

    @staticmethod
    def get_guardian_city_bonus(city_level: int) -> float:
        return city_level * 3.0

    @staticmethod
    def gold_required_for_upgrade(current_level: int, target_level: int) -> int:
        if current_level >= target_level:
            return 0
        if current_level < 1 or target_level < 1:
            raise ValueError("Levels must be >= 1")
        cumulative_current = math.floor(50 * ((1.2 ** (current_level - 1)) - 1))
        cumulative_target = math.floor(50 * ((1.2 ** (target_level - 1)) - 1))
        return max(0, cumulative_target - cumulative_current)

    @staticmethod
    def format_gold(value: float) -> str:
        if value >= 1e15: return f"{value/1e15:.2f}p"
        elif value >= 1e12: return f"{value/1e12:.2f}t"
        elif value >= 1e9: return f"{value/1e9:.2f}g"
        elif value >= 1e6: return f"{value/1e6:.2f}m"
        elif value >= 1e3: return f"{value/1e3:.2f}k"
        else:
            s = f"{value:.2f}"
            return s.rstrip("0").rstrip(".") if "." in s else s

    @staticmethod
    def parse_gold(value_with_suffix: str) -> int:
        s = value_with_suffix.strip().lower()
        suffix_multipliers = {'m': 1e6, 'g': 1e9, 't': 1e12, 'p': 1e15}
        if not s:
            raise ValueError("Empty value")
        last = s[-1]
        if last in suffix_multipliers:
            number_part = float(s[:-1])
            return int(number_part * suffix_multipliers[last])
        return int(float(s))

    @staticmethod
    def parse_gold_float(value_with_suffix: str) -> float:
        s = value_with_suffix.strip().lower()
        suffix_multipliers = {'m': 1e6, 'g': 1e9, 't': 1e12, 'p': 1e15}
        if not s:
            raise ValueError("Empty value")
        last = s[-1]
        if last in suffix_multipliers:
            number_part = float(s[:-1])
            return number_part * suffix_multipliers[last]
        return float(s)

    @staticmethod
    def total_gold_multiple_cities(current_level: int, target_level: int, number_of_cities: int = 1, gold_unit: int = 1) -> Tuple[int, str]:
        if number_of_cities < 1: raise ValueError("number_of_cities must be >= 1")
        if gold_unit < 1: raise ValueError("gold_unit must be >= 1")
        per_city = Cities.gold_required_for_upgrade(current_level, target_level)
        raw_total = per_city * number_of_cities * gold_unit
        return raw_total, Cities.format_gold(raw_total)

    @staticmethod
    def drain_calc(city_level: int, cautious: float = 50) -> dict:
        cost = Cities.get_cc_val(city_level)
        cautious_return = round(cost * (cautious / 100), 1)
        return {"city_level": city_level, "cautious_return": cautious_return}

    @staticmethod
    def level_for_attack_power(ap_suffixed: str):
        ap = Cities.parse_gold_float(ap_suffixed)
        if ap < 70:
            return (0, 0.0, "0")
        L = math.floor(math.log(ap / 70, 1.2) + 1)
        while L > 0 and Cities.get_cw_val(L) > ap:
            L -= 1
        while Cities.get_cw_val(L + 1) <= ap:
            L += 1
        wall_value = Cities.get_cw_val(L)
        return (L, wall_value, Cities.format_gold(wall_value))

    @staticmethod
    def level_for_attack_power_raw(ap_raw: float):
        if ap_raw < 70:
            return (0, 0.0, "0")
        L = math.floor(math.log(ap_raw / 70.0, 1.2) + 1)
        while L > 0 and Cities.get_cw_val(L) > ap_raw:
            L -= 1
        while Cities.get_cw_val(L + 1) <= ap_raw:
            L += 1
        wall_val = Cities.get_cw_val(L)
        return (L, wall_val, Cities.format_gold(wall_val))