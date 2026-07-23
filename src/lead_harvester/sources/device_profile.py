"""
Device Profile Manager
======================
Generates and PERMANENTLY stores a consistent fake device fingerprint
per burner account.

LinkedIn's anti-bot system cross-checks many device characteristics across
sessions. If your screen resolution changes from 1920x1080 one day to
1366x768 the next, that is a strong bot signal. A real human uses the
same device every day.

Covers:
  ✓ Browser identity  — User-Agent, viewport, screen resolution, color depth
  ✓ Hardware signals  — CPU core count, device memory, platform, architecture
  ✓ Font fingerprint  — consistent subset of installed fonts
  ✓ Network signals   — timezone matched to geolocation, locale, accept-language
  ✓ WebRTC            — disabled (prevents real IP leak through proxies)
  ✓ Canvas/WebGL      — seeded noise values to stay consistent per account
  ✓ Session start jitter — randomised start time within working hours
"""
from __future__ import annotations

import json
import random
import string
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


PROFILES_DIR = Path("sessions")

# ---------------------------------------------------------------------------
# Realistic device presets to pick from
# ---------------------------------------------------------------------------

_SCREEN_RESOLUTIONS = [
    (1920, 1080),
    (1920, 1080),   # weighted higher — most common
    (1920, 1080),
    (1440, 900),
    (1366, 768),
    (2560, 1440),
    (1280, 800),
]

# Each account gets a distinct Pakistani city identity
# (lat, lon, city_name, timezone)
_PAKISTAN_CITIES = [
    (33.6844,  73.0479, "Islamabad",   "Asia/Karachi"),
    (31.5204,  74.3587, "Lahore",      "Asia/Karachi"),
    (24.8607,  67.0011, "Karachi",     "Asia/Karachi"),
    (33.7215,  73.0433, "Rawalpindi",  "Asia/Karachi"),
    (30.1798,  66.9750, "Quetta",      "Asia/Karachi"),
    (34.0151,  71.5249, "Peshawar",    "Asia/Karachi"),
    (32.0836,  72.6711, "Sargodha",    "Asia/Karachi"),
    (31.4504,  73.1350, "Faisalabad",  "Asia/Karachi"),
    (30.1956,  71.4753, "Multan",      "Asia/Karachi"),
    (25.3960,  68.3578, "Hyderabad",   "Asia/Karachi"),
]

_USER_AGENTS = [
    # Camoufox uses Firefox engine — ONLY Firefox UAs are consistent with its TLS fingerprint.
    # Chrome UAs with a Firefox TLS handshake = instant bot flag.
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
]

_CPU_COUNTS    = [4, 4, 4, 8, 8, 8, 12, 16]   # weighted toward common values
_DEVICE_MEMORY = [4, 8, 8, 8, 16, 16]          # GB — weighted toward 8GB laptops

_ACCEPT_LANGUAGES = [
    "en-US,en;q=0.9",
    "en-US,en;q=0.9,ur;q=0.8",          # Pakistan-based user
    "en-GB,en;q=0.9",
    "en-US,en;q=0.9,ar;q=0.8",
]


@dataclass
class DeviceProfile:
    """
    A persistent, internally-consistent fake device fingerprint.
    All fields are generated once and reused every session for the same account.
    """
    account_id: str

    # --- Browser identity ---
    user_agent: str         = ""
    viewport_width: int     = 1280
    viewport_height: int    = 720
    screen_width: int       = 1920
    screen_height: int      = 1080
    color_depth: int        = 24
    pixel_ratio: float      = 1.0
    accept_language: str    = "en-US,en;q=0.9"

    # --- Hardware characteristics ---
    hardware_concurrency: int  = 8
    device_memory: int         = 8
    platform: str              = "Win32"
    architecture: str          = "x86_64"

    # --- Locale & timezone (matched to assigned city) ---
    timezone_id: str   = "Asia/Karachi"
    locale: str        = "en-US"
    city_name: str     = "Islamabad"

    # --- Geolocation (consistent per account, unique city) ---
    geo_latitude: float   = 33.6844
    geo_longitude: float  = 73.0479

    # --- Canvas noise seed (stable fingerprint) ---
    canvas_noise_seed: int = 0

    # --- Session timing ---
    # Preferred start hour (randomised within working hours, fixed per account)
    preferred_start_hour: int   = 10   # e.g. this account "usually" starts at 10 AM
    preferred_start_jitter: int = 30   # ±30 min variance around preferred hour

    # --- Misc ---
    fonts: list[str] = field(default_factory=list)


def generate_profile(account_id: str) -> DeviceProfile:
    """Generate a new randomised-but-realistic device profile for an account."""
    rng = random.Random(account_id)  # seeded by account ID for reproducibility

    sw, sh = rng.choice(_SCREEN_RESOLUTIONS)
    # Viewport MUST be smaller than screen (taskbar + browser chrome)
    # Violating this (viewport >= screen) is an impossible real-device state
    vw = sw - rng.randint(40, 120)
    vh = sh - rng.randint(100, 180)

    # Pick a unique city for this account (based on hash of account_id)
    city_idx = hash(account_id) % len(_PAKISTAN_CITIES)
    lat, lon, city, tz = _PAKISTAN_CITIES[city_idx]
    # Add tiny GPS jitter so coordinates look like a real device (not a pin-drop)
    lat += rng.uniform(-0.008, 0.008)
    lon += rng.uniform(-0.008, 0.008)

    return DeviceProfile(
        account_id=account_id,
        user_agent=rng.choice(_USER_AGENTS),
        viewport_width=vw,
        viewport_height=vh,
        screen_width=sw,
        screen_height=sh,
        color_depth=24,
        pixel_ratio=rng.choice([1.0, 1.0, 1.0, 1.25, 1.5, 2.0]),
        accept_language=rng.choice(_ACCEPT_LANGUAGES),
        hardware_concurrency=rng.choice(_CPU_COUNTS),
        device_memory=rng.choice(_DEVICE_MEMORY),
        platform="Win32",
        architecture="x86_64",
        timezone_id=tz,
        locale="en-US",
        city_name=city,
        geo_latitude=lat,
        geo_longitude=lon,
        canvas_noise_seed=rng.randint(10000, 99999),
        preferred_start_hour=rng.randint(9, 12),
        preferred_start_jitter=rng.randint(10, 45),
        fonts=[
            "Arial", "Calibri", "Times New Roman", "Verdana",
            "Georgia", "Segoe UI", "Tahoma", "Trebuchet MS",
        ],
    )


class DeviceProfileManager:
    """Load or create a persistent device profile for a burner account."""

    def __init__(self, base_dir: str | Path = PROFILES_DIR) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, account_id: str) -> Path:
        return self.base_dir / f"{account_id}_device.json"

    def load_or_create(self, account_id: str) -> DeviceProfile:
        """
        Load an existing device profile from disk, or generate a new one.
        Once created, the same profile is reused every session.
        """
        path = self._path(account_id)
        if path.exists():
            data = json.loads(path.read_text())
            return DeviceProfile(**data)

        profile = generate_profile(account_id)
        path.write_text(json.dumps(asdict(profile), indent=2))
        print(f"[DeviceProfile] Created new device profile for '{account_id}'.")
        return profile

    def get(self, account_id: str) -> DeviceProfile:
        return self.load_or_create(account_id)
