import math
from dictionary import clean_input
from cities import Cities

class XPHandler:
    @staticmethod
    def parse_modifier(modifier_input: str | float) -> float:
        if isinstance(modifier_input, (int, float)):
            return float(modifier_input) / 100.0   # Option A: always treat float as percentage
        s = str(modifier_input).strip().replace('%', '')
        try:
            val = float(s)
            return val / 100.0 if '%' in str(modifier_input) else val
        except:
            return 1.0

    @staticmethod
    def calculate_xp_this_hit(
        defender_killed: float,
        city_wall: float,
        modifier_input: str | float = "100%"
    ) -> float:
        base_xp = (defender_killed * 3.0) + city_wall
        multiplier = XPHandler.parse_modifier(modifier_input)
        return base_xp * multiplier

    @staticmethod
    def get_xp_needed_for_next_level(current_level: int) -> float:
        if current_level < 1:
            return 50.0
        return round(50 * (1.3 ** (current_level - 1)), 2)

    @staticmethod
    def check_level_up(current_xp: float, current_level: int) -> tuple[int, float]:
        xp_needed = XPHandler.get_xp_needed_for_next_level(current_level)
        if current_xp >= xp_needed:
            return current_level + 1, 0.0
        return current_level, current_xp

    @staticmethod
    def calculate_cumulative_xp(cities: int = 5, city_level: int = 115, modifier: float = 100.0):
        cw = Cities.get_cw_val(city_level)
        total_xp = 0.0
        for _ in range(cities):
            total_xp += XPHandler.calculate_xp_this_hit(50000, cw, modifier)
        return {"total_xp": round(total_xp, 1), "cities": cities, "city_level": city_level, "modifier": modifier}

    @staticmethod
    def calculate_single_city_xp(city_level: int = 115, modifier: float = 100.0):
        cw = Cities.get_cw_val(city_level)
        xp = XPHandler.calculate_xp_this_hit(50000, cw, modifier)
        return {"xp": round(xp, 1), "city_level": city_level, "modifier": modifier}

    @staticmethod
    def calculate_cities_needed_to_level_up(current_level: int, city_level: int = 115, modifier: float = 100.0):
        cw = Cities.get_cw_val(city_level)
        xp_per_city = XPHandler.calculate_xp_this_hit(50000, cw, modifier)
        needed = XPHandler.get_xp_needed_for_next_level(current_level)
        cities_needed = math.ceil(needed / xp_per_city)
        return {
            "cities_needed": cities_needed,
            "current_level": current_level,
            "city_level": city_level,          # ← THIS WAS THE MISSING LINE
            "xp_per_city": round(xp_per_city, 1)
        }