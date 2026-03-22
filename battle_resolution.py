from cities import Cities
from troops_calc import TroopsCalc
import math

class BattleResolution:
    @staticmethod
    def full_battle_result(
        at_troops: float, striker: float, scav: float, fearless: float,
        dt_troops: float, guardian: float, salv: float, brave: float,
        city_level: int
    ) -> dict:
        ap = TroopsCalc.attacker_power(at_troops, striker)
        dp_troops = TroopsCalc.defender_power(dt_troops, guardian, city_level)
        cw = Cities.get_cw_val(city_level)
        total_dp = cw + dp_troops

        if ap >= total_dp:
            attacker_wins = True
            dt_killed = dt_troops
            
            defender_effective = dp_troops + cw
            x = defender_effective / ap
            at_killed = min(at_troops, at_troops * (0.3 * x + 0.7 * x * x))
        else:
            attacker_wins = False
            at_killed = at_troops
            
            defender_effective = dp_troops + cw
            x = ap / defender_effective
            dt_killed = min(dt_troops, dt_troops * (0.3 * x + 0.7 * x * x))

        killed = dt_killed if attacker_wins else at_killed

        scavenger_gold = math.floor(dt_killed * (scav / 100))
        troop_ratio = dp_troops / total_dp if total_dp > 0 else 0
        salvager_gold = math.floor(at_killed * troop_ratio * (salv / 100))

        revived = killed * (fearless / 100) if attacker_wins else killed * (brave / 100)

        final_att = at_troops - at_killed + revived
        final_def = dt_troops - dt_killed + revived
        
        at_loss_pct = round((at_killed / at_troops * 100), 1) if at_troops > 0 else 0
        dt_loss_pct = round((dt_killed / dt_troops * 100), 1) if dt_troops > 0 else 0

        defender_troop_pct = round(troop_ratio * 100, 2)
        winner_loss_pct = at_loss_pct if attacker_wins else dt_loss_pct

        return {
            "attacker_wins": attacker_wins,
            "ap": ap,
            "dp": total_dp,
            "cw": cw,
            "at_troops": at_troops,
            "dt_troops": dt_troops,
            "final_attacker": final_att,
            "final_def": final_def,
            "attacker_killed": at_killed,
            "defender_killed": dt_killed,
            "at_loss_pct": at_loss_pct,
            "dt_loss_pct": dt_loss_pct,
            "scavenger_gold": scavenger_gold,
            "salvager_gold": salvager_gold,
            "rev_a90": round(at_killed * 0.90),
            "rev_a75": round(at_killed * 0.75),
            "rev_d90": round(dt_killed * 0.90),
            "rev_d75": round(dt_killed * 0.75),
            "scav_162": round(dt_killed * 1.62),
            "scav_144": round(dt_killed * 1.44),
            "defender_troop_pct": defender_troop_pct,
            "winner_loss_pct": winner_loss_pct,
            "striker": striker,
            "guardian": guardian,
            "salv": salv,
            "city_level": city_level
        }