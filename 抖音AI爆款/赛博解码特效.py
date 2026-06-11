# -*- coding: utf-8 -*-
"""赛博解码特效 CipherBreaker — 100% 没用，密码可见率 0%，仅供娱乐"""
from __future__ import annotations

import random
import threading
import time
import tkinter as tk
from tkinter import ttk

APP_NAME = "赛博解码特效"
VERSION = "CipherBreaker v7.3"
FAKE_PASSWORD = "**********"

# 录屏画框区域（1920×1080 桌面实测，与赛博定位特效同款选区，可按 OBS 选区微调 ±10）
RECORD_W = 730
RECORD_H = 590
RECORD_X = 890
RECORD_Y = 145

# 配色（暗黑骇客风）
BG = "#0b0f14"
CYAN = "#00ffc8"
DIM = "#5a7a8a"
LIGHT = "#e8f4ff"
PANEL = "#121820"
LINE = "#1e3a4a"
GREEN = "#00ff88"


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME}  {VERSION}")
        self.configure(bg=BG)
        self._setup_style()
        self._apply_record_frame()

        self._busy = False
        self._boot_then_main()

    # ---------- 样式 / 定位 ----------
    def _setup_style(self) -> None:
        style = ttk.Style(self)
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
        self.option_add("*TCombobox*Listbox.background", PANEL)
        self.option_add("*TCombobox*Listbox.foreground", LIGHT)
        self.option_add("*TCombobox*Listbox.selectBackground", "#004d40")
        self.option_add("*TCombobox*Listbox.selectForeground", CYAN)

    def _apply_record_frame(self) -> None:
        """固定窗口到录屏选区，双击打开即落在画框内。"""
        self.geometry(f"{RECORD_W}x{RECORD_H}+{RECORD_X}+{RECORD_Y}")
        self.resizable(False, False)
        self.update_idletasks()
        self.geometry(f"{RECORD_W}x{RECORD_H}+{RECORD_X}+{RECORD_Y}")

    # ---------- 开机自检 ----------
    def _boot_then_main(self) -> None:
        self._boot = tk.Frame(self, bg=BG)
        self._boot.pack(fill="both", expand=True)

        tk.Label(self._boot, text="◈", font=("Segoe UI Symbol", 42), fg=CYAN, bg=BG).pack(pady=(80, 12))
        tk.Label(self._boot, text=APP_NAME, font=("Consolas", 20, "bold"), fg=LIGHT, bg=BG).pack()
        tk.Label(
            self._boot,
            text="BRUTE-FORCE · RAINBOW TABLE · QUANTUM CORE",
            font=("Consolas", 9),
            fg=DIM,
            bg=BG,
        ).pack(pady=(6, 24))

        self._boot_bar = ttk.Progressbar(
            self._boot, mode="indeterminate", length=320, style="Cyber.Horizontal.TProgressbar"
        )
        self._boot_bar.pack(pady=8)
        self._boot_bar.start(12)

        self._boot_status = tk.Label(
            self._boot, text="正在初始化破解引擎…", font=("Microsoft YaHei UI", 10), fg=CYAN, bg=BG
        )
        self._boot_status.pack(pady=12)

        msgs = [
            "挂载 GPU 暴力破解集群 ×64…",
            "加载彩虹表 4.7TB…",
            "接入全球撞库数据库…",
            "校验操作员权限：通过",
            "唤醒量子退火协处理器…",
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

    # ---------- 主界面 ----------
    def _build_main(self) -> None:
        # 先钉底：状态栏 + 按钮
        status = tk.Frame(self, bg="#001a14", height=24)
        status.pack(side="bottom", fill="x")
        status.pack_propagate(False)
        tk.Label(
            status,
            text="引擎：在线  |  算力：9.2 亿组/秒  |  彩虹表：4.7TB  |  成功率：看起来很高",
            font=("Consolas", 8),
            fg=CYAN,
            bg="#001a14",
            anchor="w",
            padx=10,
        ).pack(fill="both")

        self._btn = tk.Button(
            self,
            text="▶  一 键 找 回 密 码",
            font=("Microsoft YaHei UI", 11, "bold"),
            bg="#004d40",
            fg=CYAN,
            activebackground="#00695c",
            activeforeground="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
            command=self._start,
        )
        self._btn.pack(side="bottom", fill="x", padx=14, pady=(0, 8))

        # 顶部标题条
        top = tk.Frame(self, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        top.pack(fill="x", padx=14, pady=(10, 6))
        tk.Label(
            top,
            text=f"  {APP_NAME}  ·  {VERSION}  ",
            font=("Consolas", 11, "bold"),
            fg=CYAN,
            bg=PANEL,
        ).pack(side="left", padx=12, pady=8)
        tk.Label(top, text="● LIVE", font=("Consolas", 9, "bold"), fg="#ff4444", bg=PANEL).pack(
            side="right", padx=14
        )

        # 表单
        form = tk.Frame(self, bg=BG)
        form.pack(fill="x", padx=14, pady=(0, 4))

        tk.Label(form, text="选择应用", font=("Microsoft YaHei UI", 10), fg=DIM, bg=BG).grid(
            row=0, column=0, sticky="w", pady=6
        )
        self.app_choice = ttk.Combobox(
            form,
            style="Cyber.TCombobox",
            values=[
                "微信",
                "QQ",
                "支付宝",
                "淘宝",
                "微博",
                "抖音",
                "网易云音乐",
                "Steam",
                "公司 OA",
                "老板脑子里的 WiFi 密码",
            ],
            state="readonly",
            font=("Microsoft YaHei UI", 10),
        )
        self.app_choice.set("请选择要找回的应用")
        self.app_choice.grid(row=0, column=1, sticky="ew", pady=6, padx=(10, 0))

        tk.Label(form, text="账　　号", font=("Microsoft YaHei UI", 10), fg=DIM, bg=BG).grid(
            row=1, column=0, sticky="w", pady=6
        )
        self.account = tk.Entry(
            form,
            font=("Consolas", 11),
            bg=PANEL,
            fg=LIGHT,
            insertbackground=CYAN,
            relief="flat",
            highlightthickness=1,
            highlightbackground=LINE,
            highlightcolor=CYAN,
        )
        self.account.grid(row=1, column=1, sticky="ew", pady=6, padx=(10, 0))
        form.columnconfigure(1, weight=1)

        # 选项
        opts = tk.Frame(form, bg=BG)
        opts.grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))
        self.opt_gpu = tk.BooleanVar(value=True)
        self.opt_rain = tk.BooleanVar(value=True)
        self.opt_quan = tk.BooleanVar(value=True)
        for text, var in (
            ("GPU 暴力破解", self.opt_gpu),
            ("彩虹表撞库", self.opt_rain),
            ("量子退火加速", self.opt_quan),
        ):
            tk.Checkbutton(
                opts,
                text=text,
                variable=var,
                font=("Microsoft YaHei UI", 9),
                fg="#8ab4c7",
                bg=BG,
                activebackground=BG,
                activeforeground=CYAN,
                selectcolor="#1a2830",
            ).pack(side="left", padx=(0, 14))

        # 进度条
        self.progress = ttk.Progressbar(
            self, mode="determinate", maximum=100, style="Cyber.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", padx=14, pady=(4, 4))

        # 实时日志
        log_frame = tk.Frame(self, bg=BG)
        log_frame.pack(fill="both", expand=True, padx=14, pady=(0, 4))
        tk.Label(log_frame, text="▸ 实时破解日志", font=("Consolas", 9), fg=DIM, bg=BG).pack(anchor="w")
        self.log = tk.Text(
            log_frame,
            font=("Consolas", 9),
            bg="#05080c",
            fg=GREEN,
            insertbackground=GREEN,
            relief="flat",
            wrap="word",
            height=8,
            padx=10,
            pady=6,
        )
        self.log.pack(fill="both", expand=True, pady=(4, 0))
        self.log.configure(state="disabled")
        self._log("引擎在线。等待目标账号…")

    # ---------- 日志 ----------
    def _log(self, msg: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---------- 执行 ----------
    def _start(self) -> None:
        if self._busy:
            return
        app_name = self.app_choice.get()
        if not app_name or app_name.startswith("请选择"):
            self._log("!! 错误：未选择要找回的应用")
            return
        account = self.account.get().strip()
        if not account:
            self._log("!! 错误：未填写账号，不知道找谁的")
            return

        self._busy = True
        self._btn.configure(state="disabled", text="破解中… 请勿断开")
        self.progress["value"] = 0
        threading.Thread(target=self._run, args=(app_name, account), daemon=True).start()

    def _run(self, app_name: str, account: str) -> None:
        acct = account if len(account) <= 10 else account[:9] + "…"
        steps = [
            (12, f"定位 {app_name} 登录节点 … OK"),
            (25, f"提取账号 [{acct}] 加密指纹 …"),
            (38, "比对彩虹表第 114514 组 …"),
            (52, "暴力枚举 9.2 亿组/秒 … ███░"),
            (65, "绕过二次验证（仿真）…"),
            (90, "命中候选密码，正在脱敏 …"),
            (100, "破解完成 · 报告就绪"),
        ]
        if self.opt_gpu.get():
            steps.insert(3, (45, "RTX 集群温度 87°C，风扇已起飞"))
        if self.opt_rain.get():
            steps.insert(5, (58, "彩虹表撞库：匹配度 99.99%"))
        if self.opt_quan.get():
            steps.insert(6, (72, "量子比特退相干，重试一次 … OK"))

        steps.sort(key=lambda x: x[0])
        for pct, msg in steps:
            time.sleep(random.uniform(0.35, 0.7))
            self.after(0, lambda p=pct, m=msg: (self.progress.configure(value=p), self._log(m)))

        time.sleep(0.35)
        self.after(0, lambda: self._show_report(app_name, account))

    # ---------- 报告弹窗 ----------
    def _show_report(self, app_name: str, account: str) -> None:
        self._busy = False
        self._btn.configure(state="normal", text="▶  一 键 找 回 密 码")

        win = tk.Toplevel(self)
        win.title("找回报告 · TOP SECRET")
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
            header, text="◈  赛博解码报告", font=("Microsoft YaHei UI", 13, "bold"), fg="#ffffff", bg="#1a1a2e"
        ).pack(pady=16)

        body = tk.Frame(win, bg="#ffffff", padx=24, pady=16)
        body.pack(fill="both", expand=True)

        acct = account if len(account) <= 16 else account[:14] + "…"
        lines = [
            ("目标应用", app_name),
            ("账　　号", acct),
            ("找回密码", FAKE_PASSWORD),
            ("加密算法", "MD5 + 盐 + 祖传玄学"),
            ("破解耗时", "8.0 秒（含装样子）"),
            ("准 确 度", "100%"),
            ("可 用 度", "0%"),
        ]
        for i, (k, v) in enumerate(lines):
            tk.Label(body, text=k, font=("Microsoft YaHei UI", 9), fg="#888", bg="#ffffff").grid(
                row=i, column=0, sticky="w", pady=4
            )
            color = "#c62828" if k == "找回密码" else "#222"
            weight = "bold" if k in ("找回密码", "可 用 度") else "normal"
            tk.Label(
                body,
                text=v,
                font=("Consolas" if k == "找回密码" else "Microsoft YaHei UI", 10, weight),
                fg=color,
                bg="#ffffff",
            ).grid(row=i, column=1, sticky="w", padx=(16, 0), pady=4)

        tk.Label(
            body,
            text="密码已脱敏处理，请妥善保管！",
            font=("Microsoft YaHei UI", 9, "bold"),
            fg="#c62828",
            bg="#ffffff",
        ).grid(row=len(lines), column=0, columnspan=2, pady=(12, 4))
        tk.Label(
            body,
            text="（其实啥也没破解，这 8 秒是你今天最像黑客的时刻）",
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

    App().mainloop()


if __name__ == "__main__":
    main()
