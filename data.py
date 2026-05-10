# engine.py
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

# =========================
# XP SYSTEM 
# =========================

def calculate_xp(data: Dict[str, Any]) -> int:
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

def sync_sensors(seed: Optional[int] = None) -> Dict[str, Any]:
    """Simulate reading sensors/inverter. In a real system this would call drivers or HTTP APIs."""
    return get_data(seed)
