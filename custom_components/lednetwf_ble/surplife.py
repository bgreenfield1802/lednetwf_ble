"""Surplife scene ("E1 21") effects for Surplife-app IOTBT string lights.

Product 0xC5 (Surplife-app string lights, sold as Dazzle Bright) silently ignores the integration's segment
("E1 01") and v3 ("E0 02") effect commands, but accepts the scene command the
Surplife app itself sends, and reports the effect id and speed back in its
EA 81 state reply (bytes 8 and 9), which is how this was verified remotely.

Payload, wrapped with cmd_family 0x0a:
    E1 21 00 [brightness 1-100] [animation id] 00 01 64 [speed 1-100]
    00 00 00 00 00 00 [n] {[hue] [sat 0-100] [val 0-100] 00 00} * n

An effect is an animation built into the firmware plus a palette of 1-7
colours and a speed - the motion itself cannot be programmed. Every effect
below is a custom design, each previewed and approved on the real lights; none
of the Surplife app's own presets is kept.

ANIMATION CATALOGUE - observed on the real lights with a red/green/blue palette
(ids 0x0C, 0x17, 0x18 and everything from 0x27 up leave the lights dark):
    01 breathe: whole string one colour, next palette colour after each fade-out
    02 twinkle: all palette colours at once, LEDs fading in and out
    03 jump: whole string steps colour to colour, no fade
    04 twinkle with hard on/off instead of fades
    05 crossfade: whole string fades smoothly colour to colour, never dark
    06 starlight: string fully lit in the palette, a few LEDs at a time subtly
       change colour; speed makes very little visible difference
    07 strobe: whole string flashes briefly then dark, next colour each flash
    08 sparkle: mostly dark, scattered LEDs strobe-flash
    09 background crossfades between two colours while the FIRST colour flashes
       on random LEDs - busy even at speed 1
    0A moving twinkling segments, one colour at a time
    0B meteor: LEDs chase around the string, one colour at a time
    0D meteor with fluctuating speed
    0E comet trails over a base: first colour is the trail head, second the
       base, third the tail
    0F colour wipe: each new colour sweeps over the previous one
    10, 23 stacking: single LEDs travel along and stick, building a line
    11, 16 multi breathe: whole string breathes, each LED a different colour
    12 multi blink: as 11 with hard on/off
    13 alternating breathe: sections breathe out of step (never all dark),
       each fading out fully before changing colour
    14 static mix: no motion, palette colours scattered along the string
    15 strobe with LEDs in mixed colours
    19 colour chase: each colour a segment, segments bounce off each other
    1A classic Christmas: neighbouring LEDs blink alternately, mixed colours
    1B two colours in a still mix, third flashes rapidly around - busy at any speed
    1C a mix of shimmer and segment stacking
    1D per-LED colour changes, hard switches; 1E the same on a dark string
    1F short multicolour segments travelling around, rest dark
    20 solid base, another colour flashes on some LEDs, base then switches
       to the third colour and back
    21 drifting glows: slow 3-LED segments fading in/out as they move, rest dark
    22 fireworks: rapid bursts around the string
    24 white runners over a background cycling the palette with slight dips;
       25 the same with runners a brighter shade of the background
    26 mixed breathe that keeps settling back to solid FIRST colour

COLOUR - palette hue is degrees / 2 (0-180, wraps at 180), not 0-255. On
these LEDs: red 0, orange 5, yellow 15, lime 30, green 60, light blue 90, deep
blue 120, indigo 150, magenta 165, hot pink 175. Saturation only matters
above ~88: 70 is barely-tinted white, 30 plain white, 90-95 a pastel, so a
paler look is made by adding white (sat 0) slots as much as by lowering
saturation. Per-colour value works only at the extremes (25 looks like 100,
3 is nearly off).
"""
from __future__ import annotations

SURPLIFE_SCENE_PRODUCT_IDS = frozenset({0xC5})

W = (0, 0, 100)  # white

# name: (animation_id, speed 1-100, [(hue, saturation, value), ...])
# Every effect runs at its own designed speed; the integration's effect-speed
# setting does not apply to these lights.
SURPLIFE_EFFECTS: dict[str, tuple[int, int, list[tuple[int, int, int]]]] = {
    # Weather skies, run in place of the curve colour on wet days.
    'Sky Rain': (0x06, 100, [(120, 92, 100), W, (90, 90, 100), W, (105, 88, 100)]),
    'Sky Storm': (0x05, 20, [(150, 100, 100), (120, 94, 100), (140, 100, 100)]),
    'Sky Snow': (0x06, 50, [W, (95, 88, 100), W, W, (100, 88, 100), W]),
    # Wake sunrise: stepped through 1-7 by Home Assistant over the wake cue,
    # each a slow crossfade between two neighbouring colours, red to warm white.
    'Wake Sunrise 1': (0x05, 20, [(0, 100, 100)]),
    'Wake Sunrise 2': (0x05, 20, [(0, 100, 100), (2, 100, 100)]),
    'Wake Sunrise 3': (0x05, 20, [(2, 100, 100), (5, 100, 100)]),
    'Wake Sunrise 4': (0x05, 20, [(5, 100, 100), (8, 100, 100)]),
    'Wake Sunrise 5': (0x05, 20, [(8, 100, 100), (12, 100, 100)]),
    'Wake Sunrise 6': (0x05, 20, [(12, 95, 100), (10, 92, 100)]),
    'Wake Sunrise 7': (0x05, 20, [(10, 90, 100), W]),
    'Wind Down': (0x13, 20, [(5, 100, 100), (3, 100, 100), (0, 100, 100)]),
    'Welcome Home': (0x0E, 40, [(10, 90, 100), (8, 100, 100), (5, 100, 100)]),
    # Alerts: a whole-string breathe, one colour per alert; weather is faster
    # and alternates red/orange. A strobe was tried and is too harsh.
    'Alert Doorbell': (0x01, 70, [(60, 100, 100)]),
    'Alert Dishwasher': (0x01, 70, [(90, 100, 100)]),
    'Alert Laundry': (0x01, 70, [(165, 100, 100)]),
    'Alert Weather': (0x01, 100, [(0, 100, 100), (5, 100, 100)]),
    # Holidays. Each runs for days or weeks, so all are calm; the fireworks
    # are only for the first minutes of January 1st.
    'New Year': (0x02, 1, [(12, 100, 100), W, (10, 92, 100)]),
    'New Year Midnight': (0x22, 50, [(12, 100, 100), W, (165, 100, 100)]),
    "Valentine's Day": (0x11, 20, [(0, 100, 100), (175, 100, 100), (175, 92, 100)]),
    "St. Patrick's Day": (0x13, 20, [(60, 100, 100), (30, 100, 100), (12, 100, 100)]),
    'Easter': (0x14, 50, [(175, 90, 100), W, (15, 90, 100), (30, 90, 100), W, (150, 90, 100), (90, 90, 100)]),
    'Birthday': (0x06, 50, [(0, 100, 100), (15, 100, 100), (60, 100, 100), (90, 100, 100), (165, 100, 100), (5, 100, 100)]),
    'Halloween1': (0x05, 8, [(5, 100, 100), (147, 100, 100), (3, 100, 100)]),
    'Halloween2': (0x14, 50, [(5, 100, 100), (147, 100, 100), (5, 100, 100)]),
    'Halloween3': (0x26, 20, [(5, 100, 100), (143, 100, 100), (3, 100, 100)]),
    'Thanksgiving': (0x11, 15, [(8, 100, 100), (5, 100, 100), (1, 100, 100), (12, 100, 100)]),
    'Christmas1': (0x1A, 20, [(0, 92, 100), (60, 92, 100), (120, 92, 100), (5, 92, 100), (15, 92, 100)]),
    'Christmas2': (0x14, 50, [(0, 100, 100), (60, 92, 100), (10, 90, 100)]),
    'Christmas3': (0x05, 10, [(0, 100, 100), (12, 100, 100), (2, 100, 100), (10, 92, 100)]),
}


def device_hue(hue_deg: float) -> int:
    """Map a standard 0-360 hue to the palette hue scale (degrees / 2)."""
    return int(hue_deg % 360) // 2


def build_scene_payload(effect_name: str, brightness_pct: int) -> bytes | None:
    """Return the raw E1 21 payload (unwrapped) for a named effect."""
    entry = SURPLIFE_EFFECTS.get(effect_name)
    if entry is None:
        return None
    effect_id, speed, palette = entry
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
