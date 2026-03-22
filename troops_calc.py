from cities import Cities

class TroopsCalc:
    @staticmethod
    def attacker_power(troops: float, striker: float) -> float:
        # CORRECTED FORMULA: Striker is a bonus multiplier
        # 500m troops at 300% striker = 500m * (1 + 300/100) = 2g AP
        return troops * (1 + striker / 100)

    @staticmethod
    def defender_power(troops: float, guardian: float, city_level: int) -> float:
        bonus = guardian + Cities.get_guardian_city_bonus(city_level)
        return troops * (1 + bonus / 100)