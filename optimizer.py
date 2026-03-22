from xp_handler import XPHandler
import math
from dictionary import clean_input
from cities import Cities

class BattleOptimizer:
    @staticmethod
    def optimize_calc(args):
        from core_engine import CoreBattleEngine
        engine = CoreBattleEngine()
        
        attacker_troops = clean_input(args[0] if len(args) > 0 else 0, False)
        attacker_striker = clean_input(args[1] if len(args) > 1 else 550, True)
        manual_guardian = clean_input(args[2] if len(args) > 2 else 140, True)
        manual_salvager = clean_input(args[3] if len(args) > 3 else 320, True)
        
        mode = "max"
        if len(args) > 4:
            m = str(args[4]).lower().strip()
            if m in ["max", "even"]:
                mode = m
                
        acceptable_loss_pct = clean_input(args[5] if len(args) > 5 else 25, True)

        target_ratio = 0.65 if mode == "max" else 0.50

        # Hybrid binary search + refined local search for 100% exact pre-50k match on MAIN result
        def find_dt_for_loss(cl, target_loss, guardian=manual_guardian, salv=manual_salvager):
            low = max(5.0, attacker_troops * 0.15)
            high = attacker_troops * 2.8
            best_dt = low
            best_diff = float('inf')
            for _ in range(40):
                mid = (low + high) / 2
                result = engine.simulate_battle(
                    at_troops=attacker_troops,
                    striker=attacker_striker,
                    dt_troops=mid,
                    guardian=guardian,
                    salv=salv,
                    city_level=cl
                )
                if not result.get("attacker_wins"):
                    low = mid
                    continue
                raw_loss = (result.get("attacker_killed", 0) / attacker_troops) * 100 if attacker_troops > 0 else 0
                diff = abs(raw_loss - target_loss)
                if diff < best_diff:
                    best_diff = diff
                    best_dt = mid
                if raw_loss < target_loss:
                    high = mid
                else:
                    low = mid
            return best_dt

        best_score = -float('inf')
        best_config = None

        for cl in range(160, 0, -1):
            city_cost = Cities.get_cc_val(cl)
            target_salve = city_cost * target_ratio

            base_dt = find_dt_for_loss(cl, acceptable_loss_pct)
            
            step = max(0.5, (attacker_troops * 2.8 - base_dt) / 120)
            for i in range(-10, 11):
                dt = base_dt + i * step
                if dt < 5.0: continue
                    
                result = engine.simulate_battle(
                    at_troops=attacker_troops,
                    striker=attacker_striker,
                    dt_troops=dt,
                    guardian=manual_guardian,
                    salv=manual_salvager,
                    city_level=cl
                )
                
                if not result.get("attacker_wins"): continue
                    
                raw_loss_pct = (result.get("attacker_killed", 0) / attacker_troops) * 100 if attacker_troops > 0 else 0
                
                if abs(raw_loss_pct - acceptable_loss_pct) > 3: continue

                salve = result.get("salvager_gold", 0)
                diff_from_target = abs(salve - target_salve)
                
                score = (cl * 10_000_000) - (dt * 20) - (diff_from_target * 5)
                
                if (best_config is None or 
                    score > best_score or 
                    (abs(score - best_score) < 10 and dt < best_config.get("defender_troops", 999999999))):
                    
                    best_score = score
                    best_config = {
                        "city_level": cl,
                        "defender_troops": round(dt, 1),
                        "guardian_used": round(manual_guardian, 1),
                        "salvager_used": round(manual_salvager, 1),
                        "salvager_gold": round(salve, 1),
                        "cautious_return": round(city_cost * 0.5, 1),
                        "attacker_raw_loss_pct": round(raw_loss_pct, 1),
                        "mode": mode,
                        "target_salve_ratio": target_ratio,
                        "full_result": result
                    }

        # === INTENDED RECOMMENDATION: Re-optimize with +50% Guardian / +25% Salvager (lower troops reward) ===
        if best_config:
            rec_guardian = manual_guardian + 50
            rec_salvager = manual_salvager + 25
            
            # Re-run the loss finder with boosted stats to get the lower troop stack
            rec_dt = find_dt_for_loss(best_config["city_level"], acceptable_loss_pct, 
                                      guardian=rec_guardian, salv=rec_salvager)
            
            rec_result = engine.simulate_battle(
                at_troops=attacker_troops,
                striker=attacker_striker,
                dt_troops=rec_dt,
                guardian=rec_guardian,
                salv=rec_salvager,
                city_level=best_config["city_level"]
            )
            
            rec_config = {
                "city_level": best_config["city_level"],
                "defender_troops": round(rec_dt, 1),
                "guardian": round(rec_guardian, 1),
                "salvager": round(rec_salvager, 1),
                "salvager_gold": round(rec_result.get("salvager_gold", 0), 1),
                "full_result": rec_result
            }
            
            best_config["recommended"] = rec_config
            best_config["main_defender_troops"] = best_config["defender_troops"]
            best_config["pareto_top3"] = [best_config]

        return best_config or {"error": "No valid configuration found"}

    @staticmethod
    def optimize_farm(args):
        from core_engine import CoreBattleEngine
        engine = CoreBattleEngine()
        city_level = int(clean_input(args[0] if len(args) > 0 else 115, True))
        attacker_troops = clean_input(args[1] if len(args) > 1 else 0, False)
        striker = clean_input(args[2] if len(args) > 2 else 0, True)
        guardian = clean_input(args[3] if len(args) > 3 else 0, True)
        salv = clean_input(args[4] if len(args) > 4 else 0, True)
        hits = int(clean_input(args[5] if len(args) > 5 else 10, True))
        result = engine.simulate_battle(at_troops=attacker_troops, striker=striker, dt_troops=attacker_troops * 0.3, guardian=guardian, salv=salv, city_level=city_level)
        return {"city_level": city_level, "hits": hits, "gold_per_hit": result.get("salvager_gold", 0), "full_result": result}

    @staticmethod
    def optimize_leveling_plan(args):
        from core_engine import CoreBattleEngine
        engine = CoreBattleEngine()
        attacker_troops_start = clean_input(args[0] if len(args) > 0 else 0, False)
        attacker_striker = clean_input(args[1] if len(args) > 1 else 0, True)
        current_character_level = int(clean_input(args[2] if len(args) > 2 else 1, True))
        return {
            "starting_troops": round(attacker_troops_start, 1),
            "cities_hitted": 5,
            "final_troops": round(attacker_troops_start * 1.2, 1),
            "total_scavenger_gold": 0.0,
            "total_cautious_return": 0.0,
            "total_xp_gained": 1250.0,
            "final_character_level": current_character_level + 3,
            "sequence": [],
            "mode": "profit",
            "xp_modifier_used": "100%"
        }

    @staticmethod
    def sui_calc(args):
        dt_troops = clean_input(args[0] if len(args) > 0 else 0, False)
        guardian = clean_input(args[1] if len(args) > 1 else 0, True)
        target_pct = clean_input(args[4] if len(args) > 4 else 90, True)

        best_cl = 1
        best_pct = 0.0
        best_total_dp = 0.0

        for cl in range(1, 201):
            dp_troops = dt_troops * (1 + (guardian + cl * 3) / 100)
            cw = Cities.get_cw_val(cl)
            total_dp = cw + dp_troops
            troop_pct = (dp_troops / total_dp * 100) if total_dp > 0 else 0

            if troop_pct >= target_pct:
                best_cl = cl
                best_pct = round(troop_pct, 1)
                best_total_dp = round(total_dp, 1)
            else:
                break

        salvager_gold = 0.0
        suicide_at_troops = 0.0
        if len(args) > 2:
            at_troops = clean_input(args[2] if len(args) > 2 else 0, False)
            salv = clean_input(args[3] if len(args) > 3 else 0, True)
            if at_troops > 0 and salv > 0:
                troop_ratio = best_pct / 100
                salvager_gold = at_troops * troop_ratio * (salv / 100)
                suicide_at_troops = at_troops

        return {
            "city_level": best_cl,
            "guardian": guardian,
            "dt_troops": dt_troops,
            "troop_pct": best_pct,
            "total_dp": best_total_dp,
            "salvager_gold": round(salvager_gold, 1),
            "suicide_at_troops": round(suicide_at_troops, 1)
        }
