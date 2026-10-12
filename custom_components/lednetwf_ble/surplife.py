"""Surplife scene ("E1 21") effects for Surplife-app IOTBT string lights.

Product 0xC5 (Surplife-app string lights, sold as Dazzle Bright) silently ignores the integration's segment
("E1 01") and v3 ("E0 02") effect commands, but accepts the scene command the
Surplife app itself sends, and reports the effect id and speed back in its
EA 81 state reply (bytes 8 and 9), which is how this was verified remotely.

Payload, wrapped with cmd_family 0x0a:
    E1 21 00 [brightness 1-100] [effect_id] 00 01 64 [speed 1-100]
    00 00 00 00 00 00 [n] {[hue] [sat 0-100] [val 0-100] 00 00} * n

Effect ids and palettes are the app's own, from an HCI capture of the
Surplife app driving Surplife string lights (rabidpaperclip/magichome2-ble).
Palette hues are the device's non-linear 0-255 scale, NOT the packed hue/2
that the E0 01 static colour command uses - see device_hue().
"""
from __future__ import annotations

SURPLIFE_SCENE_PRODUCT_IDS = frozenset({0xC5})

# name: (effect_id, [(device_hue, saturation, value), ...])
SURPLIFE_EFFECTS: dict[str, tuple[int, list[tuple[int, int, int]]]] = {
    'Christmas1': (0x19, [(0, 100, 100), (120, 100, 100), (0, 100, 100), (0, 100, 100), (30, 100, 100)]),
    'Christmas2': (0x14, [(60, 100, 100), (135, 100, 100), (30, 100, 100), (11, 100, 100)]),
    'Christmas3': (0x0A, [(0, 100, 100), (30, 100, 100), (0, 100, 100), (30, 100, 100), (0, 100, 100), (30, 100, 100), (0, 0, 100)]),
    'Halloween1': (0x0B, [(0, 100, 100), (0, 100, 100), (0, 100, 100), (120, 100, 100)]),
    'Halloween2': (0x02, [(30, 100, 100), (14, 100, 100)]),
    'Halloween3': (0x20, [(120, 100, 100), (0, 100, 100), (120, 100, 100)]),
    "Valentine's Day": (0x0D, [(0, 100, 100), (23, 100, 100), (135, 100, 100), (165, 100, 100)]),
    'Thanksgiving': (0x16, [(150, 100, 100), (90, 100, 100), (14, 100, 100)]),
    "Mother's Day": (0x21, [(60, 100, 100), (56, 100, 100), (0, 100, 100), (60, 100, 100), (56, 100, 100), (56, 100, 100)]),
    "Father's Day": (0x11, [(10, 100, 100), (0, 100, 100), (10, 100, 100), (0, 100, 100), (10, 100, 100), (0, 100, 100), (10, 100, 100)]),
    'New Year': (0x0A, [(0, 100, 100), (60, 100, 100), (120, 100, 100), (30, 100, 100), (150, 100, 100), (90, 100, 100), (0, 0, 100)]),
    "Children's Day": (0x0E, [(90, 100, 100), (60, 100, 100), (30, 100, 100)]),
    'Easter': (0x0E, [(14, 100, 100), (0, 100, 100)]),
    'Birthday': (0x14, [(0, 100, 100), (0, 100, 100), (60, 100, 100), (30, 100, 100)]),
    "St. Patrick's Day": (0x13, [(90, 100, 100), (30, 100, 100)]),
    'Meteor Shower': (0x11, [(60, 100, 100), (30, 100, 100), (14, 100, 100), (90, 100, 100)]),
    'Fantasy Fireworks': (0x0F, [(14, 100, 100), (5, 100, 100)]),
    'Summer Wind': (0x0E, [(120, 100, 100), (75, 100, 100), (15, 100, 100), (75, 100, 100), (120, 100, 100)]),
    'Moonlight': (0x0F, [(120, 100, 100), (104, 100, 100), (90, 100, 100)]),
    'Dynamic Rhythm': (0x1D, [(60, 100, 100), (30, 100, 100)]),
    'Champagne Party': (0x0D, [(14, 100, 100)]),
    'Movie Night': (0x0D, [(0, 100, 100), (150, 100, 100), (120, 100, 100), (90, 100, 100), (60, 100, 100), (30, 100, 100)]),
    'Rainbow Cycle': (0x01, [(0, 100, 100), (150, 100, 100), (120, 100, 100), (90, 100, 100), (60, 100, 100), (30, 100, 100)]),
    'Rainbow Smooth': (0x16, [(0, 100, 100), (60, 100, 100), (120, 100, 100), (30, 100, 100), (150, 100, 100), (90, 100, 100), (0, 0, 100)]),
    'Color Chase': (0x19, [(0, 100, 100), (60, 100, 100), (120, 100, 100), (30, 100, 100), (150, 100, 100), (90, 100, 100), (0, 0, 100)]),
    'Two-Color Pulse': (0x1A, [(0, 100, 100), (135, 100, 100)]),
    'Gradient Shift': (0x1D, [(0, 100, 100), (60, 100, 100), (120, 100, 100), (150, 100, 100)]),
    'Smooth Transition': (0x20, [(0, 100, 100), (150, 100, 100), (120, 100, 100), (90, 100, 100), (60, 100, 100), (30, 100, 100)]),
    'Strobe Flash': (0x04, [(0, 100, 100), (60, 100, 100), (120, 100, 100)]),
    # Custom palettes on the app's animation ids, for the bedroom scenes.
    'Warm Twinkle': (0x0F, [(14, 100, 100), (23, 100, 100), (30, 60, 100)]),
    'Ember Breathe': (0x0B, [(5, 100, 100), (14, 100, 100)]),
    'Ocean Drift': (0x20, [(120, 100, 100), (135, 100, 100), (104, 100, 100)]),
    'Twilight Drift': (0x20, [(135, 100, 100), (176, 100, 100), (228, 80, 100)]),
}


def device_hue(hue_deg: float) -> int:
    """Map a standard 0-360 hue to the device's palette hue scale.

    Piecewise-linear fit measured by eye on real Surplife string lights:
    red 0, green 90, blue 135, back to red at 255 (green-blue compressed).
    """
    h = hue_deg % 360
    if h < 120:
        return int(h * 90 / 120)
    if h < 240:
        return 90 + int((h - 120) * 45 / 120)
    return 135 + int((h - 240) * 120 / 120)


def build_scene_payload(effect_name: str, speed: int, brightness_pct: int) -> bytes | None:
    """Return the raw E1 21 payload (unwrapped) for a named effect."""
    entry = SURPLIFE_EFFECTS.get(effect_name)
    if entry is None:
        return None
    effect_id, palette = entry
    payload = bytearray([
        0xE1, 0x21, 0x00,
        max(1, min(100, brightness_pct)),
        effect_id & 0xFF,
        0x00, 0x01, 0x64,
        max(1, min(100, speed)),
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        len(palette) & 0xFF,
    ])
    for h, s, v in palette:
        payload.extend([h & 0xFF, s & 0xFF, v & 0xFF, 0x00, 0x00])
    return bytes(payload)
