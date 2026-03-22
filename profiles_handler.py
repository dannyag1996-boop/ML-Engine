import json
import os
from typing import Dict, List, Optional

MEMORY_FILE = "profiles.json"

class ProfilesHandler:
    def __init__(self):
        self.profiles: Dict = {}
        self.codes: Dict = {}
        self.permissions: Dict = {}
        self.loaded_profiles: Dict = {}

        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    data = json.load(f)
                    self.profiles = data.get("profiles", {})
                    self.codes = data.get("codes", {})
                    self.permissions = data.get("permissions", {})
                    self.loaded_profiles = data.get("loaded_profiles", {})
            except:
                pass

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump({
                "profiles": self.profiles,
                "codes": self.codes,
                "permissions": self.permissions,
                "loaded_profiles": self.loaded_profiles
            }, f, indent=4)

    def set_profile(self, profile_name: str, owner_id: str, profile_type: str = "attacker", **stats):
        profile_name = profile_name.strip()
        if profile_name in self.profiles and self.profiles[profile_name]["owner_id"] != owner_id:
            return False
        self.profiles[profile_name] = {
            "owner_id": owner_id,
            "type": profile_type.lower(),
            "striker": stats.get("striker", 0.0),
            "scavenger": stats.get("scavenger", 0.0),
            "fearless": stats.get("fearless", 75.0),
            "guardian": stats.get("guardian", 0.0),
            "salvager": stats.get("salvager", 0.0),
            "brave": stats.get("brave", 75.0),
            "cautious": stats.get("cautious", 50.0),
            "second_profile_name": None
        }
        self.save()
        return True

    def create_second_profile(self, main_profile_name: str, second_name: str, owner_id: str):
        if main_profile_name not in self.profiles or self.profiles[main_profile_name]["owner_id"] != owner_id:
            return False
        if second_name in self.profiles:
            return False
        main_stats = self.profiles[main_profile_name].copy()
        main_stats.pop("second_profile_name", None)
        success = self.set_profile(second_name, owner_id, main_stats["type"], **main_stats)
        if success:
            self.profiles[main_profile_name]["second_profile_name"] = second_name
            self.save()
        return success

    def adjust_profile_stats(self, profile_name: str, modifier_id: str, stats_dict: Dict[str, float]) -> bool:
        if profile_name not in self.profiles:
            return False
        owner = self.profiles[profile_name]["owner_id"]
        allowed = modifier_id == owner or modifier_id in self.permissions.get(profile_name, [])
        if not allowed:
            return False
        for v in stats_dict.values():
            if v < 0:
                return False
        self.profiles[profile_name].update(stats_dict)
        self.save()
        return True

    def grant_permission(self, profile_name: str, owner_id: str, target_id: str):
        if profile_name not in self.profiles or self.profiles[profile_name]["owner_id"] != owner_id:
            return False
        if profile_name not in self.permissions:
            self.permissions[profile_name] = []
        if target_id not in self.permissions[profile_name]:
            self.permissions[profile_name].append(target_id)
        self.save()
        return True

    def load_profile(self, discord_id: str, profile_name: str) -> bool:
        if profile_name in self.profiles:
            self.loaded_profiles[discord_id] = profile_name
            self.save()
            return True
        return False

    def unload_profile(self, discord_id: str):
        self.loaded_profiles.pop(discord_id, None)
        self.save()
        return True

    def get_loaded_profile(self, discord_id: str) -> Optional[str]:
        return self.loaded_profiles.get(discord_id)

    def clear_profile(self, profile_name: str, owner_id: str):
        if profile_name in self.profiles and self.profiles[profile_name]["owner_id"] == owner_id:
            del self.profiles[profile_name]
            self.save()
            return True
        return False

    def get_profile(self, profile_name: str) -> dict:
        return self.profiles.get(profile_name, {})

    def get_attacker_stats(self, profile_name: str):
        p = self.get_profile(profile_name)
        return {
            "striker": p.get("striker", 0.0),
            "scavenger": p.get("scavenger", 0.0),
            "fearless": p.get("fearless", 75.0)
        }

    def get_defender_stats(self, profile_name: str):
        p = self.get_profile(profile_name)
        return {
            "guardian": p.get("guardian", 0.0),
            "salvager": p.get("salvager", 0.0),
            "brave": p.get("brave", 75.0),
            "cautious": p.get("cautious", 50.0)
        }

    def list_all_profiles(self):
        return list(self.profiles.keys())

    def list_attackers(self):
        return [name for name, data in self.profiles.items() if data.get("type") in ["attacker", "both"]]

    def list_builders(self):
        return [name for name, data in self.profiles.items() if data.get("type") in ["defender", "both"]]

    def get_permissions(self, profile_name: str):
        return self.permissions.get(profile_name, [])

    def get_user_profiles(self, discord_id: str) -> List[str]:
        return [name for name, data in self.profiles.items() if data.get("owner_id") == discord_id]