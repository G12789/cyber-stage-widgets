# -*- coding: utf-8 -*-
"""赛博定位特效 BlackVer — 看起来很强，实际上啥也没有"""
from __future__ import annotations

import random
import threading
import time
import tkinter as tk
from tkinter import ttk

APP_NAME = "赛博定位特效"
VERSION = "BlackVer 4.2.1"
SECRET_BLOCK = "█" * 12

# 录屏画框区域（1920×1080 桌面实测，可按 OBS 选区微调 ±10）
RECORD_W = 730
RECORD_H = 590
RECORD_X = 890
RECORD_Y = 145


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME}  {VERSION}")
        self.configure(bg="#0b0f14")
        self._apply_record_frame()

        self._busy = False
        self._boot_then_main()

    def _apply_record_frame(self) -> None:
        """固定窗口到录屏选区，双击打开即落在画框内。"""
        self.geometry(f"{RECORD_W}x{RECORD_H}+{RECORD_X}+{RECORD_Y}")
        self.resizable(False, False)
        self.update_idletasks()
        self.geometry(f"{RECORD_W}x{RECORD_H}+{RECORD_X}+{RECORD_Y}")

    def _boot_then_main(self) -> None:
        self._boot = tk.Frame(self, bg="#0b0f14")
        self._boot.pack(fill="both", expand=True)

        tk.Label(
            self._boot,
            text="◈",
            font=("Segoe UI Symbol", 42),
            fg="#00ffc8",
            bg="#0b0f14",
        ).pack(pady=(80, 12))

        tk.Label(
            self._boot,
            text=APP_NAME,
            font=("Consolas", 20, "bold"),
            fg="#e8f4ff",
            bg="#0b0f14",
        ).pack()

        tk.Label(
            self._boot,
            text="CLASSIFIED · EYES ONLY · NOFORN",
            font=("Consolas", 9),
            fg="#5a7a8a",
            bg="#0b0f14",
        ).pack(pady=(6, 24))

        self._boot_bar = ttk.Progressbar(self._boot, mode="indeterminate", length=320)
        self._boot_bar.pack(pady=8)
        self._boot_bar.start(12)

        self._boot_status = tk.Label(
            self._boot,
            text="正在建立加密隧道…",
            font=("Microsoft YaHei UI", 10),
            fg="#00ffc8",
            bg="#0b0f14",
        )
        self._boot_status.pack(pady=12)

        msgs = [
            "握手 TOR 中继节点 #7…",
            "加载暗网指纹库 2.4TB…",
            "同步卫星 Ephemeris 数据…",
            "校验操作员权限：通过",
            "初始化量子哈希引擎…",
        ]
        self.after(600, lambda: self._run_boot(msgs, 0))

    def _run_boot(self, msgs: list[str], idx: int) -> None:
        if idx < len(msgs):
            self._boot_status.configure(text=msgs[idx])
            self.after(random.randint(400, 700), lambda: self._run_boot(msgs, idx + 1))
        else:
            self._boot_bar.stop()
            self._boot.destroy()
            self._build_main()
            self._apply_record_frame()

    def _build_main(self) -> None:
        # 先钉底：状态栏 + 按钮，避免被 expand 的日志区挤到画框外
        status = tk.Frame(self, bg="#001a14", height=24)
        status.pack(side="bottom", fill="x")
        status.pack_propagate(False)
        tk.Label(
            status,
            text="链路：加密  |  节点：47  |  延迟：12ms  |  可信度：看起来很高",
            font=("Consolas", 8),
            fg="#00ffc8",
            bg="#001a14",
            anchor="w",
            padx=10,
        ).pack(fill="both")

        self._btn = tk.Button(
            self,
            text="▶  执行穿透查询",
            font=("Microsoft YaHei UI", 11, "bold"),
            bg="#004d40",
            fg="#00ffc8",
            activebackground="#00695c",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
            command=self._start_query,
        )
        self._btn.pack(side="bottom", fill="x", padx=14, pady=(0, 8))

        top = tk.Frame(self, bg="#121820", highlightbackground="#1e3a4a", highlightthickness=1)
        top.pack(fill="x", padx=14, pady=(10, 6))

        tk.Label(
            top,
            text=f"  {APP_NAME}  ·  {VERSION}  ",
            font=("Consolas", 11, "bold"),
            fg="#00ffc8",
            bg="#121820",
        ).pack(side="left", padx=12, pady=8)

        tk.Label(
            top,
            text="● LIVE",
            font=("Consolas", 9, "bold"),
            fg="#ff4444",
            bg="#121820",
        ).pack(side="right", padx=14)

        form = tk.Frame(self, bg="#0b0f14")
        form.pack(fill="x", padx=14, pady=(0, 4))

        self._field(form, "查询目标", "target", "请输入手机号 / QQ / 昵称 / 任意字符")
        self._field(form, "关联密钥", "key", "可选 · 留空自动暴力匹配")

        opts = tk.Frame(form, bg="#0b0f14")
        opts.grid(row=2, column=0, columnspan=2, sticky="w", pady=(2, 0))

        self.opt_sat = tk.BooleanVar(value=True)
        self.opt_graph = tk.BooleanVar(value=True)
        self.opt_ai = tk.BooleanVar(value=True)
        for text, var in (
            ("卫星辅助定位", self.opt_sat),
            ("深度社交图谱", self.opt_graph),
            ("AI 行为预测", self.opt_ai),
        ):
            tk.Checkbutton(
                opts,
                text=text,
                variable=var,
                font=("Microsoft YaHei UI", 9),
                fg="#8ab4c7",
                bg="#0b0f14",
                activebackground="#0b0f14",
                activeforeground="#00ffc8",
                selectcolor="#1a2830",
            ).pack(side="left", padx=(0, 14))

        self.progress = ttk.Progressbar(self, mode="determinate", maximum=100)
        self.progress.pack(fill="x", padx=14, pady=(4, 4))

        log_frame = tk.Frame(self, bg="#0b0f14")
        log_frame.pack(fill="both", expand=True, padx=14, pady=(0, 4))

        tk.Label(
            log_frame,
            text="▸ 实时渗透日志",
            font=("Consolas", 9),
            fg="#5a7a8a",
            bg="#0b0f14",
        ).pack(anchor="w")

        self.log = tk.Text(
            log_frame,
            font=("Consolas", 9),
            bg="#05080c",
            fg="#00ff88",
            insertbackground="#00ff88",
            relief="flat",
            wrap="word",
            height=9,
            padx=10,
            pady=6,
        )
        self.log.pack(fill="both", expand=True, pady=(4, 0))
        self.log.configure(state="disabled")
        self._log("系统在线。等待目标输入…")

    def _field(self, parent: tk.Frame, label: str, attr: str, placeholder: str) -> None:
        row = getattr(self, "_form_row", 0)
        tk.Label(
            parent,
            text=label,
            font=("Microsoft YaHei UI", 10),
            fg="#8ab4c7",
            bg="#0b0f14",
        ).grid(row=row, column=0, sticky="w", pady=4)
        entry = tk.Entry(
            parent,
            font=("Consolas", 11),
            bg="#121820",
            fg="#e8f4ff",
            insertbackground="#00ffc8",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#1e3a4a",
            highlightcolor="#00ffc8",
            width=42,
        )
        entry.grid(row=row, column=1, sticky="ew", pady=4, padx=(10, 0))
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda e, ent=entry, ph=placeholder: self._clear_ph(ent, ph))
        setattr(self, attr, entry)
        parent.columnconfigure(1, weight=1)
        self._form_row = row + 1

    @staticmethod
    def _clear_ph(entry: tk.Entry, placeholder: str) -> None:
        if entry.get() == placeholder:
            entry.delete(0, "end")

    def _log(self, msg: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _start_query(self) -> None:
        if self._busy:
            return

        target = self.target.get().strip()
        if not target or target.startswith("请输入"):
            self._log("!! 错误：未指定查询目标")
            return

        self._busy = True
        self._btn.configure(state="disabled", text="穿透中… 请勿断开")
        self.progress["value"] = 0

        threading.Thread(target=self._run_query, args=(target,), daemon=True).start()

    def _run_query(self, target: str) -> None:
        steps = [
            (12, f"DNS 劫持 {random.randint(100, 255)}.{random.randint(0, 255)}.x.x … OK"),
            (25, f"对目标 [{target[:8]}…] 发起 SYN  flood（仿真）"),
            (38, "绕过 WAF · 注入 payload: ' OR 1=1 --"),
            (52, "接入低轨卫星链路 #3 … 信号强度 ████░"),
            (65, "爬取 14 个社交平台公开头像 … 匹配度 99.97%"),
            (78, "AI 模型推断：目标大概率是人类"),
            (90, "生成绝密报告 … AES-256 封装"),
            (100, "查询完成 · 报告已就绪"),
        ]
        if self.opt_sat.get():
            steps.insert(3, (32, "三角定位：误差半径 ± 6400km（地球级精度）"))
        if self.opt_graph.get():
            steps.insert(5, (58, "社交图谱：发现 1 个好友 —— 您自己"))
        if self.opt_ai.get():
            steps.insert(6, (72, "行为预测：未来 24h 内会吃饭、睡觉、怀疑本软件"))

        steps.sort(key=lambda x: x[0])
        for pct, msg in steps:
            time.sleep(random.uniform(0.35, 0.7))
            self.after(0, lambda p=pct, m=msg: (self.progress.configure(value=p), self._log(m)))

        time.sleep(0.35)
        self.after(0, lambda: self._show_report(target))

    def _show_report(self, target: str) -> None:
        self._busy = False
        self._btn.configure(state="normal", text="▶  执行穿透查询")

        win = tk.Toplevel(self)
        win.title("查询报告 · TOP SECRET")
        win.geometry("440x360")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        win.configure(bg="#f4f4f4")

        win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - 440) // 2
        y = self.winfo_y() + (self.winfo_height() - 360) // 2
        win.geometry(f"+{x}+{y}")

        header = tk.Frame(win, bg="#1a1a2e", height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="◈  赛博定位报告",
            font=("Microsoft YaHei UI", 13, "bold"),
            fg="#ffffff",
            bg="#1a1a2e",
        ).pack(pady=16)

        body = tk.Frame(win, bg="#ffffff", padx=24, pady=16)
        body.pack(fill="both", expand=True)

        short = target if len(target) <= 16 else target[:14] + "…"
        lines = [
            ("查询目标", short),
            ("真实身份", "地球 Online 注册玩家"),
            ("威胁等级", "会点外卖 · 会摸鱼"),
            ("物理坐标", "北纬 地球  东经 人类"),
            ("核心机密", SECRET_BLOCK),
            ("准确度", "100%"),
            ("可用度", "0%"),
        ]
        for i, (k, v) in enumerate(lines):
            tk.Label(body, text=k, font=("Microsoft YaHei UI", 9), fg="#888", bg="#ffffff").grid(
                row=i, column=0, sticky="w", pady=4
            )
            color = "#c62828" if k == "核心机密" else "#222"
            weight = "bold" if k in ("核心机密", "可用度") else "normal"
            tk.Label(
                body,
                text=v,
                font=("Consolas" if k == "核心机密" else "Microsoft YaHei UI", 10, weight),
                fg=color,
                bg="#ffffff",
            ).grid(row=i, column=1, sticky="w", padx=(16, 0), pady=4)

        tk.Label(
            body,
            text="机密已脱敏处理，符合《个人信息保护法》",
            font=("Microsoft YaHei UI", 9, "bold"),
            fg="#c62828",
            bg="#ffffff",
        ).grid(row=len(lines), column=0, columnspan=2, pady=(12, 4))

        tk.Label(
            body,
            text="（恍然大悟了吗？这 8 秒是你今天最接近黑客的时刻）",
            font=("Microsoft YaHei UI", 8),
            fg="#999",
            bg="#ffffff",
        ).grid(row=len(lines) + 1, column=0, columnspan=2)

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


def main() -> None:
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
