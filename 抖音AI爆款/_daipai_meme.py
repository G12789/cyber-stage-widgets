# -*- coding: utf-8 -*-
"""带派梗图：白底抠图 + 冻梨遮脸 + 色键透明弹窗（稳定可见）。"""
from __future__ import annotations

import random
import sys
from collections import deque
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"
SOURCE = ASSETS / "daipai_source.png"
CACHED = ASSETS / "daipai_popup.png"
_CACHE_VER = 9

CHROMA_RGB = (1, 0, 1)
CHROMA_HEX = "#010001"

# 脸在人物中部；红字「带派」在上方 — 冻梨只盖脸、不碰字
_FACE_X = 0.375
_FACE_Y = 0.395


def _is_bg_white(r: int, g: int, b: int, a: int) -> bool:
    if a < 8:
        return True
    return min(r, g, b) > 228 and max(r, g, b) - min(r, g, b) < 28


def _flood_white_bg(img):
    """从四角泛洪，只抠连到边缘的白底，不碰人物内部。"""
    w, h = img.size
    px = img.load()
    seen = set()
    q = deque()

    for seed in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if _is_bg_white(*px[seed]):
            q.append(seed)
            seen.add(seed)

    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and _is_bg_white(*px[nx, ny]):
                seen.add((nx, ny))
                q.append((nx, ny))

    return img


def _clean_white_fringe(img):
    """去掉抠图后残留的白边像素。"""
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and min(r, g, b) > 232 and max(r, g, b) - min(r, g, b) < 18:
                px[x, y] = (r, g, b, 0)
    return img


def _draw_frozen_pear(base, w: int, h: int):
    """东北冻梨：乌紫皱皮、白霜、梨形，盖住整张脸。"""
    from PIL import Image, ImageDraw

    cx = int(w * _FACE_X)
    cy = int(h * _FACE_Y)
    pw = int(w * 0.12)
    ph = int(h * 0.13)

    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    left = cx - pw // 2
    right = cx + pw // 2
    top = cy - int(ph * 0.42)
    bot = cy + int(ph * 0.58)

    draw.ellipse((left + pw // 6, top, right - pw // 6, bot), fill=(12, 4, 10, 255))
    draw.ellipse((left + 2, top + ph // 7, right - 2, bot - 2), fill=(24, 10, 18, 255))
    draw.ellipse((left + 5, top + ph // 5, right - 5, bot - 5), fill=(38, 16, 28, 240))
    draw.ellipse((left + 8, top + ph // 4, right - 8, bot - 8), fill=(20, 8, 14, 220))

    draw.arc((left + 4, top + ph // 6, right - 6, bot - 8), 205, 325, fill=(6, 2, 5, 255), width=2)
    draw.arc((left + 7, top + ph // 4, right - 9, bot - 12), 175, 285, fill=(50, 22, 36, 200), width=1)
    draw.arc((left + 3, top + ph // 3, right - 4, bot - 6), 30, 140, fill=(8, 3, 6, 255), width=2)

    rng = random.Random(20260604)
    for _ in range(32):
        fx = rng.randint(left + 6, right - 6)
        fy = rng.randint(top + ph // 5, bot - 8)
        fr = rng.randint(1, 3)
        frost = rng.choice([(195, 205, 220, 210), (170, 180, 200, 180), (220, 225, 235, 190)])
        draw.ellipse((fx - fr, fy - fr, fx + fr, fy + fr), fill=frost)

    sw = max(3, pw // 10)
    draw.rectangle((cx - sw // 2, top - ph // 5, cx + sw // 2, top + ph // 8), fill=(48, 32, 18, 255))

    return Image.alpha_composite(base, layer)


def _ensure_cached() -> Path:
    stamp = ASSETS / f".cache_v{_CACHE_VER}"
    if CACHED.exists() and stamp.exists() and CACHED.stat().st_mtime >= SOURCE.stat().st_mtime:
        return CACHED

    from PIL import Image

    img = Image.open(SOURCE).convert("RGBA")
    img = _flood_white_bg(img)
    img = _clean_white_fringe(img)
    w, h = img.size
    img = _draw_frozen_pear(img, w, h)

    alpha = img.split()[-1]
    bbox = alpha.point(lambda a: 255 if a > 30 else 0).getbbox()
    if bbox:
        l, t, r, b = bbox
        img = img.crop((max(0, l - 2), max(0, t - 2), min(w, r + 2), min(h, b + 2)))

    ASSETS.mkdir(parents=True, exist_ok=True)
    img.save(CACHED, "PNG")
    stamp.write_text("ok", encoding="utf-8")
    return CACHED


def load_rgba_image(*, max_width: int = 290):
    from PIL import Image

    path = _ensure_cached()
    img = Image.open(path).convert("RGBA")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.Resampling.LANCZOS)
        img = _clean_white_fringe(img)
    return img


def _to_chroma_photo(pil_rgba, master):
    """透明区铺色键，Windows transparentcolor 穿孔。"""
    from PIL import Image, ImageTk

    src = pil_rgba.convert("RGBA").copy()
    px = src.load()
    w, h = src.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 40 or (a < 220 and min(r, g, b) > 220):
                px[x, y] = CHROMA_RGB + (255,)

    flat = Image.alpha_composite(Image.new("RGBA", src.size, CHROMA_RGB + (255,)), src).convert("RGB")
    return ImageTk.PhotoImage(flat, master=master)


def show_transparent_meme(parent, pil_rgba, x: int, y: int, on_click):
    import tkinter as tk

    w, h = pil_rgba.size
    win = tk.Toplevel(parent)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(bg=CHROMA_HEX)
    win.attributes("-transparentcolor", CHROMA_HEX)
    win.geometry(f"{w}x{h}+{x}+{y}")

    closed = {"done": False}

    def _close(_e=None) -> None:
        if closed["done"]:
            return
        closed["done"] = True
        on_click()

    photo = _to_chroma_photo(pil_rgba, win)
    lbl = tk.Label(win, image=photo, bg=CHROMA_HEX, borderwidth=0, cursor="hand2")
    lbl.pack()
    lbl.bind("<Button-1>", _close)
    win.bind("<Button-1>", _close)
    win._meme_photo = photo  # type: ignore[attr-defined]

    win.update_idletasks()
    win.lift()
    win.attributes("-topmost", True)
    return win
