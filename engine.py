# engine.py - Core logic for the Solar Mo Lang
import random


"""Engine: sensor simulation and checks for the SCADA Solar System."""
from typing import Dict, Any, Optional
import random


# =========================
# SENSOR DATA (SIMULATION)
# =========================

def get_data(seed: Optional[int] = None) -> Dict[str, Any]:
    """Return a simulated sensor reading dictionary.
    If seed is provided the values become deterministic (useful for tests).
    """
    rng = random.Random(seed)
    return {
        "battery": rng.randint(20, 100),
        "solar": rng.randint(0, 500),
        "voltage": rng.uniform(9, 15),
        "current": rng.uniform(1, 10),
    }


# =========================
# CHECK FUNCTIONS
# =========================

def _ensure_keys(data: Dict[str, Any]) -> None:
    required = {"battery", "solar", "voltage", "current"}
    missing = required - set(data.keys())
    if missing:
        raise KeyError(f"Missing data keys: {sorted(missing)}")


def check_battery(data: Dict[str, Any]) -> str:
    _ensure_keys(data)
    return "Good" if data["battery"] > 40 else "Low"


def check_solar(data: Dict[str, Any]) -> str:
    _ensure_keys(data)
    return "Good" if data["solar"] > 200 else "Weak"


def efficiency_check(data: Dict[str, Any]) -> bool:
    _ensure_keys(data)
    return data["battery"] > 50 and data["solar"] > 200


def blackout_check(data: Dict[str, Any]) -> bool:
    _ensure_keys(data)
    return data["voltage"] < 10


# =========================
# XP SYSTEM (GAME ELEMENT)
# =========================

def calculate_xp(data: Dict[str, Any]) -> int:
    """Calculate XP for the current tick. Positive for efficiency, negative for blackouts.

    Returns an integer XP delta for this tick.
    """
    _ensure_keys(data)
    xp = 0

    xp += 10 if efficiency_check(data) else 2
    if blackout_check(data):
        xp -= 5

    return int(xp)


# =========================
# DATA MODEL & SYNCHRONIZATION
# =========================
class DataModel:
    """Simple in-memory data model to store recent readings and provide helpers.

    Designed to be easy for freshmen to read and extend.
    """
    def __init__(self, maxlen: int = 300):
        self.maxlen = maxlen
        self.history = {"battery": [], "solar": [], "voltage": [], "current": []}

    def add_reading(self, data: Dict[str, Any]) -> None:
        _ensure_keys(data)
        for k in self.history:
            self.history[k].append(data[k])
            if len(self.history[k]) > self.maxlen:
                self.history[k].pop(0)

    def get_recent(self, key: str, length: int = 50):
        return self.history.get(key, [])[-length:]

    def average(self, key: str, length: int = 10) -> float:
        vals = self.get_recent(key, length)
        return sum(vals) / len(vals) if vals else 0.0


def sync_sensors(seed: Optional[int] = None) -> Dict[str, Any]:
    """Simulate reading sensors/inverter. In a real system this would call drivers or HTTP APIs."""
    return get_data(seed)


# =========================
# BACKUP / BLACKOUT HELPERS
# =========================

def estimate_backup_minutes(data: Dict[str, Any], battery_capacity_wh: float = 500.0) -> float:
    """Estimate backup minutes remaining using a simple model:
    battery_capacity_wh: assumed battery capacity in Wh for demo (default 500 Wh).

    Formula: remaining_wh = battery% * capacity / 100
             load_w = voltage * current
             minutes = (remaining_wh / load_w) * 60
    Returns minutes (float). If load_w is very small, returns a large number.
    """
    _ensure_keys(data)
    remaining_wh = (data["battery"] / 100.0) * battery_capacity_wh
    load_w = max(0.1, data["voltage"] * data["current"])  # avoid div by zero
    minutes = (remaining_wh / load_w) * 60.0
    return minutes


def tips_for_efficiency(data: Dict[str, Any]) -> list:
    """Return a short list of tips based on sensor readings."""
    _ensure_keys(data)
    tips = []
    if data["battery"] < 30:
        tips.append("Reduce non-critical loads or enable low-power mode.")
    if data["solar"] < 150:
        tips.append("Check panel orientation or clean panels to improve generation.")
    if data["voltage"] < 10:
        tips.append("Voltage low: check wiring and inverter settings.")
    if not tips:
        tips.append("System operating within normal parameters.")
    return tips


# =========================
# ACHIEVEMENTS & CLOUD SYNC (STUBS)
# =========================

def achievements_for_xp(total_xp: int) -> list:
    """Simple achievements mapping based on total XP."""
    badges = []
    if total_xp >= 100:
        badges.append("Rising Star")
    if total_xp >= 500:
        badges.append("Solar Champion")
    return badges


def sync_to_cloud(summary: Dict[str, Any], endpoint: Optional[str] = None) -> bool:
    """Stub function to sync data to cloud. In production replace with real HTTP requests.

    Returns True on success (always true here).
    """
    # For freshmen demo, just print what would be sent.
    try:
        print("[cloud sync] would send:", summary)
        return True
    except Exception:
        return False
