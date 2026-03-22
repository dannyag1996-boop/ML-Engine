import math

EMOJI_CITY     = "<:city:1482969561039896676>"
EMOJI_ATTACK   = "<:attack:1483397242906742847>"
EMOJI_DEFENSE  = "<:defense:1483397677164134521>"
EMOJI_TROOPS   = "<:troops:1483397189840404572>"
EMOJI_STRIKER  = "<:striker:1482962198019182632>"
EMOJI_GUARDIAN = "<:guardian:1482962688391778304>"
EMOJI_SALVE    = "<:salve:1482962818092367993>"
EMOJI_CAUTIOUS = "<:cautious:1482962741491929179>"
EMOJI_BATTLE   = "<:battle:1482963407454994532>"
EMOJI_SCAV     = "<:scav:1483101069968933017>"
EMOJI_FEARLESS = "<:fearless:1482962777503956992>"
DIVIDER = "-----------------------"

STAT_ALIASES = {
    "striker": "striker", "str": "striker", "st": "striker",
    "scavenger": "scavenger", "scav": "scavenger", "sc": "scavenger",
    "fearless": "fearless", "fear": "fearless", "f": "fearless",
    "guardian": "guardian", "guard": "guardian", "g": "guardian",
    "salvager": "salvager", "salve": "salvager", "salv": "salvager", "s": "salvager",
    "brave": "brave", "b": "brave",
    "cautious": "cautious", "caut": "cautious", "c": "cautious"
}

def normalize_stat(raw: str) -> str:
    if not raw:
        return ""
    key = raw.lower().strip()
    return STAT_ALIASES.get(key, key)

def clean_input(val: str | float | None, is_stat: bool = False) -> float:
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val = str(val).upper().replace('%', '').replace(',', '').strip()
    multiplier = 1
    if val.endswith('P'): multiplier, val = 10**15, val[:-1]
    elif val.endswith('T'): multiplier, val = 10**12, val[:-1]
    elif val.endswith('G'): multiplier, val = 10**9,  val[:-1]
    elif val.endswith('M'): multiplier, val = 10**6,  val[:-1]
    elif val.endswith('K'): multiplier, val = 10**3,  val[:-1]
    clean_val = "".join(c for c in val if c.isdigit() or c == '.')
    try:
        num = float(clean_val) * multiplier
        if not is_stat and num < 10000 and num != 0:
            return num * 10**9
        return num
    except:
        return 0.0

def format_val(val):
    if val == 0:
        return "0"
    abs_val = abs(val)
    prefix = "-" if val < 0 else ""

    if abs_val >= 1e15:  # P
        p_val = abs_val / 1e15
        if p_val < 10:
            s = f"{p_val:.2f}".rstrip('0').rstrip('.')
        else:
            s = f"{math.floor(p_val)}"
        return f"{prefix}{s}p"
    
    elif abs_val >= 1e12:  # T
        t_val = abs_val / 1e12
        if t_val < 10:
            s = f"{t_val:.2f}".rstrip('0').rstrip('.')
        else:
            s = f"{math.floor(t_val)}"
        return f"{prefix}{s}t"
    
    elif abs_val >= 1e9:  # G
        g_val = abs_val / 1e9
        if g_val < 10:
            s = f"{g_val:.2f}".rstrip('0').rstrip('.')
        else:
            s = f"{math.floor(g_val)}"
        return f"{prefix}{s}g"
    
    elif abs_val >= 1e6:  # M
        m_val = abs_val / 1e6
        if m_val < 10:
            s = f"{m_val:.2f}".rstrip('0').rstrip('.')
        else:
            s = f"{math.floor(m_val)}"
        return f"{prefix}{s}m"
    
    elif abs_val >= 1e3:  # K
        k_val = abs_val / 1e3
        if k_val < 10:
            s = f"{k_val:.2f}".rstrip('0').rstrip('.')
        else:
            s = f"{math.floor(k_val)}"
        return f"{prefix}{s}k"
    
    else:
        s = f"{abs_val:.2f}"
        return f"{prefix}{s.rstrip('0').rstrip('.') if '.' in s else math.floor(abs_val)}"