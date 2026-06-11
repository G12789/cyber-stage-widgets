# -*- coding: utf-8 -*-
"""反差玩具共用 UI：暗黑科技感 + 录屏定位 + 报告弹窗。"""
from __future__ import annotations

import random
import threading
import time
import tkinter as tk
from tkinter import ttk

RECORD_W, RECORD_H, RECORD_X, RECORD_Y = 730, 590, 890, 145
BG = "#0b0f14"
CYAN = "#00ffc8"
DIM = "#5a7a8a"
LIGHT = "#e8f4ff"
PANEL = "#121820"
LINE = "#1e3a4a"
GREEN = "#00ff88"


def dpi_fix() -> None:
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


def setup_cyber_style(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure(
        "Cyber.Horizontal.TProgressbar",
        troughcolor="#05080c",
        background=CYAN,
        bordercolor=LINE,
        lightcolor=CYAN,
        darkcolor=CYAN,
    )
    style.configure(
        "Cyber.TCombobox",
        fieldbackground=PANEL,
        background=PANEL,
        foreground=LIGHT,
        arrowcolor=CYAN,
        bordercolor=LINE,
        selectbackground=PANEL,
        selectforeground=CYAN,
        padding=4,
    )
    root.option_add("*TCombobox*Listbox.background", PANEL)
    root.option_add("*TCombobox*Listbox.foreground", LIGHT)
    root.option_add("*TCombobox*Listbox.selectBackground", "#004d40")
    root.option_add("*TCombobox*Listbox.selectForeground", CYAN)
    return style


def apply_record_frame(win: tk.Tk) -> None:
    win.geometry(f"{RECORD_W}x{RECORD_H}+{RECORD_X}+{RECORD_Y}")
    win.resizable(False, False)
    win.update_idletasks()
    win.geometry(f"{RECORD_W}x{RECORD_H}+{RECORD_X}+{RECORD_Y}")


def cyber_entry(parent: tk.Misc, **kw) -> tk.Entry:
    return tk.Entry(
        parent,
        font=("Consolas", 11),
        bg=PANEL,
        fg=LIGHT,
        insertbackground=CYAN,
        relief="flat",
        highlightthickness=1,
        highlightbackground=LINE,
        highlightcolor=CYAN,
        **kw,
    )


def cyber_combobox(parent: tk.Misc, var: tk.StringVar, values: list[str], width: int = 22) -> ttk.Combobox:
    cb = ttk.Combobox(parent, textvariable=var, values=values, state="readonly", width=width, style="Cyber.TCombobox")
    return cb


def build_shell(
    root: tk.Tk,
    *,
    app_name: str,
    version: str,
    subtitle: str,
    status_bar: str,
    btn_text: str,
    on_run,
) -> dict:
    """构建主界面，返回控件句柄。"""
    top = tk.Frame(root, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
    top.pack(fill="x", padx=14, pady=(10, 6))
    tk.Label(top, text=f"  {app_name}  ·  {version}  ", font=("Consolas", 11, "bold"), fg=CYAN, bg=PANEL).pack(
        side="left", padx=12, pady=8
    )
    tk.Label(top, text="● LIVE", font=("Consolas", 9, "bold"), fg="#ff4444", bg=PANEL).pack(side="right", padx=14)

    status = tk.Frame(root, bg="#001a14", height=24)
    status.pack(side="bottom", fill="x")
    status.pack_propagate(False)
    tk.Label(status, text=status_bar, font=("Consolas", 8), fg=CYAN, bg="#001a14", anchor="w", padx=10).pack(
        fill="both"
    )

    btn = tk.Button(
        root,
        text=btn_text,
        font=("Microsoft YaHei UI", 11, "bold"),
        bg="#004d40",
        fg=CYAN,
        activebackground="#00695c",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=8,
        command=on_run,
    )
    btn.pack(side="bottom", fill="x", padx=14, pady=(0, 8))

    progress = ttk.Progressbar(root, mode="determinate", maximum=100, style="Cyber.Horizontal.TProgressbar")
    progress.pack(fill="x", padx=14, pady=(4, 4))

    log_frame = tk.Frame(root, bg=BG)
    log_frame.pack(fill="both", expand=True, padx=14, pady=(0, 4))
    tk.Label(log_frame, text="▸ 大模型推理日志", font=("Consolas", 9), fg=DIM, bg=BG).pack(anchor="w")
    log = tk.Text(
        log_frame,
        font=("Consolas", 9),
        bg="#05080c",
        fg=GREEN,
        insertbackground=GREEN,
        relief="flat",
        wrap="word",
        height=7,
        padx=10,
        pady=6,
    )
    log.pack(fill="both", expand=True, pady=(4, 0))
    log.configure(state="disabled")

    body = tk.Frame(root, bg=BG)
    body.pack(fill="x", padx=14, pady=(0, 4))

    return {"body": body, "btn": btn, "progress": progress, "log": log, "btn_text": btn_text}


def log_line(log: tk.Text, msg: str) -> None:
    log.configure(state="normal")
    log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    log.see("end")
    log.configure(state="disabled")


def run_boot(root: tk.Tk, app_name: str, subtitle: str, msgs: list[str], on_done) -> None:
    boot = tk.Frame(root, bg=BG)
    boot.pack(fill="both", expand=True)
    tk.Label(boot, text="◈", font=("Segoe UI Symbol", 42), fg=CYAN, bg=BG).pack(pady=(90, 12))
    tk.Label(boot, text=app_name, font=("Consolas", 20, "bold"), fg=LIGHT, bg=BG).pack()
    tk.Label(boot, text=subtitle, font=("Consolas", 9), fg=DIM, bg=BG).pack(pady=(6, 24))
    bar = ttk.Progressbar(boot, mode="indeterminate", length=320, style="Cyber.Horizontal.TProgressbar")
    bar.pack(pady=8)
    bar.start(12)
    status = tk.Label(boot, text="正在初始化推理引擎…", font=("Microsoft YaHei UI", 10), fg=CYAN, bg=BG)
    status.pack(pady=12)

    def step(i: int) -> None:
        if i < len(msgs):
            status.configure(text=msgs[i])
            root.after(random.randint(350, 600), lambda: step(i + 1))
        else:
            bar.stop()
            boot.destroy()
            on_done()
            apply_record_frame(root)

    root.after(500, lambda: step(0))


def run_steps(root: tk.Tk, widgets: dict, steps: list[tuple[int, str]], on_done) -> None:
    widgets["btn"].configure(state="disabled", text="大模型思考计算中…")
    widgets["progress"]["value"] = 0

    def worker() -> None:
        ordered = sorted(steps, key=lambda x: x[0])
        for pct, msg in ordered:
            time.sleep(random.uniform(0.3, 0.65))
            root.after(0, lambda p=pct, m=msg: (widgets["progress"].configure(value=p), log_line(widgets["log"], m)))
        time.sleep(0.3)
        root.after(0, on_done)

    threading.Thread(target=worker, daemon=True).start()


def show_report(root: tk.Tk, header: str, rows: list[tuple[str, str]], punchline: str, easter: str) -> None:
    win = tk.Toplevel(root)
    win.title("计算结果 · CONFIDENTIAL")
    win.geometry("460x380")
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()
    win.configure(bg="#f4f4f4")

    win.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - 460) // 2
    y = root.winfo_y() + (root.winfo_height() - 380) // 2
    win.geometry(f"+{x}+{y}")

    head = tk.Frame(win, bg="#1a1a2e", height=56)
    head.pack(fill="x")
    head.pack_propagate(False)
    tk.Label(head, text=f"◈  {header}", font=("Microsoft YaHei UI", 13, "bold"), fg="#ffffff", bg="#1a1a2e").pack(
        pady=16
    )

    body = tk.Frame(win, bg="#ffffff", padx=24, pady=16)
    body.pack(fill="both", expand=True)

    for i, (k, v) in enumerate(rows):
        tk.Label(body, text=k, font=("Microsoft YaHei UI", 9), fg="#888", bg="#ffffff").grid(
            row=i, column=0, sticky="w", pady=4
        )
        bold = k in ("计算结果", "可 用 度", "称　　谓", "读　　音")
        color = "#c62828" if k in ("计算结果", "可 用 度", "读　　音") else "#222"
        tk.Label(
            body,
            text=v,
            font=("Microsoft YaHei UI", 10, "bold" if bold else "normal"),
            fg=color,
            bg="#ffffff",
            wraplength=260,
            justify="left",
        ).grid(row=i, column=1, sticky="w", padx=(16, 0), pady=4)

    tk.Label(
        body,
        text=punchline,
        font=("Microsoft YaHei UI", 10, "bold"),
        fg="#c62828",
        bg="#ffffff",
        wraplength=380,
        justify="left",
    ).grid(row=len(rows), column=0, columnspan=2, pady=(12, 4), sticky="w")
    tk.Label(body, text=easter, font=("Microsoft YaHei UI", 8), fg="#999", bg="#ffffff", wraplength=380, justify="left").grid(
        row=len(rows) + 1, column=0, columnspan=2, sticky="w"
    )

    tk.Button(
        win,
        text="阅后即焚",
        font=("Microsoft YaHei UI", 10),
        bg="#1a1a2e",
        fg="white",
        relief="flat",
        padx=20,
        pady=4,
        command=win.destroy,
    ).pack(pady=(0, 16))
