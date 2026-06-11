# -*- coding: utf-8 -*-
"""翻译器 — 看着像外语翻译，出来带派不老铁。ESC 退出。"""
from __future__ import annotations

import sys
import threading
import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _cyber_toy_ui import (
    BG,
    CYAN,
    DIM,
    GREEN,
    LIGHT,
    LINE,
    PANEL,
    apply_record_frame,
    cyber_combobox,
    dpi_fix,
    log_line,
    run_boot,
    setup_cyber_style,
)
from _daipai_meme import load_rgba_image, show_transparent_meme

APP_NAME = "翻译器"
VERSION = "TransCore v1.0"
RESULT_TEXT = "带派不老铁"
PLACEHOLDER_MODEL = "请选择模型"
MODELS = [
    "Claude Opus 4.8",
    "GPT-5.2 Pro",
    "Gemini 3 Ultra",
    "DeepSeek-R1 · 671B",
    "Qwen-Max 3.0",
    "Grok-4 Heavy",
]


def _empty_model(value: str) -> bool:
    return not value or value.strip() == "" or value == PLACEHOLDER_MODEL


def _text_box(parent: tk.Misc, *, height: int, readonly: bool = False) -> tk.Text:
    box = tk.Text(
        parent,
        font=("Microsoft YaHei UI", 14),
        bg=PANEL,
        fg=LIGHT if not readonly else GREEN,
        insertbackground=CYAN,
        relief="flat",
        highlightthickness=1,
        highlightbackground=LINE,
        highlightcolor=CYAN,
        wrap="word",
        height=height,
        padx=10,
        pady=8,
    )
    if readonly:
        box.configure(state="disabled")
    return box


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME}  {VERSION}")
        self.configure(bg=BG)
        setup_cyber_style(self)
        apply_record_frame(self)
        self.bind("<Escape>", self._on_escape)

        self._busy = False
        self._widgets: dict = {}
        self._meme_photo = None
        self._overlay_win: tk.Toplevel | None = None
        run_boot(
            self,
            APP_NAME,
            "NMT · MULTILINGUAL · NEURAL CORE",
            [
                "加载多语种平行语料库 …",
                "初始化神经机器翻译 …",
                "TransCore 引擎就绪",
            ],
            self._build_main,
        )

    def _build_main(self) -> None:
        top = tk.Frame(self, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        top.pack(fill="x", padx=12, pady=(8, 4))
        tk.Label(top, text=f"  {APP_NAME}  ·  {VERSION}  ", font=("Consolas", 11, "bold"), fg=CYAN, bg=PANEL).pack(
            side="left", padx=10, pady=6
        )
        tk.Label(top, text="● LIVE", font=("Consolas", 9, "bold"), fg="#ff4444", bg=PANEL).pack(side="right", padx=12)

        opts = tk.Frame(self, bg=BG)
        opts.pack(fill="x", padx=14, pady=(4, 2))

        tk.Label(opts, text="模型", font=("Microsoft YaHei UI", 9), fg=DIM, bg=BG).grid(row=0, column=0, padx=(0, 4))
        self._model = tk.StringVar(value=PLACEHOLDER_MODEL)
        cyber_combobox(opts, self._model, [PLACEHOLDER_MODEL] + MODELS, width=22).grid(row=0, column=1, sticky="w")

        self._deep = tk.BooleanVar(value=False)
        tk.Checkbutton(
            opts,
            text="大模型深度推理",
            variable=self._deep,
            font=("Microsoft YaHei UI", 9),
            fg="#8ab4c7",
            bg=BG,
            activebackground=BG,
            activeforeground=CYAN,
            selectcolor="#1a2830",
        ).grid(row=0, column=2, padx=(16, 0), sticky="w")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="x", padx=14, pady=(4, 0))

        tk.Label(body, text="文字输入：", font=("Microsoft YaHei UI", 12, "bold"), fg=LIGHT, bg=BG, anchor="w").pack(
            fill="x", pady=(0, 4)
        )
        self._input = _text_box(body, height=2)
        self._input.pack(fill="x")

        tk.Label(body, text="翻译显示：", font=("Microsoft YaHei UI", 12, "bold"), fg=LIGHT, bg=BG, anchor="w").pack(
            fill="x", pady=(10, 4)
        )
        self._output = _text_box(body, height=2, readonly=True)
        self._output.pack(fill="x")

        self.progress = ttk.Progressbar(self, mode="determinate", maximum=100, style="Cyber.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=14, pady=(8, 4))

        log_frame = tk.Frame(self, bg=BG)
        log_frame.pack(fill="x", padx=14, pady=(0, 2))
        tk.Label(log_frame, text="▸ 推理日志", font=("Consolas", 8), fg=DIM, bg=BG).pack(anchor="w")
        self.log = tk.Text(
            log_frame,
            font=("Consolas", 8),
            bg="#05080c",
            fg=GREEN,
            relief="flat",
            wrap="word",
            height=2,
            padx=8,
            pady=4,
        )
        self.log.pack(fill="x", pady=(2, 0))
        self.log.configure(state="disabled")

        status = tk.Frame(self, bg="#001a14", height=22)
        status.pack(side="bottom", fill="x")
        status.pack_propagate(False)
        tk.Label(
            status,
            text="引擎：在线  |  模式：神经机器翻译  |  延迟：12ms  |  可信度：看起来很高",
            font=("Consolas", 8),
            fg=CYAN,
            bg="#001a14",
            anchor="w",
            padx=10,
        ).pack(fill="both")

        self._btn = tk.Button(
            self,
            text="▶  开始翻译",
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
        self._btn.pack(side="bottom", fill="x", padx=14, pady=(0, 6))

        self._widgets = {"btn": self._btn, "progress": self.progress, "log": self.log}
        log_line(self.log, "TransCore 在线。等待文字输入 …")

    def _set_output(self, text: str) -> None:
        self._output.configure(state="normal")
        self._output.delete("1.0", tk.END)
        if text:
            self._output.insert("1.0", text)
        self._output.configure(state="disabled")

    def _run_fast(self, model: str, on_done) -> None:
        self._btn.configure(state="disabled", text="大模型思考计算中…")
        self.progress["value"] = 0

        def worker() -> None:
            steps = [(55, "正在使用大模型思考计算 …"), (100, "翻译完成")]
            if self._deep.get():
                steps.insert(1, (85, f"接入 {model} 深度推理 …"))
            for pct, msg in steps:
                time.sleep(0.12)
                self.after(0, lambda p=pct, m=msg: (self.progress.configure(value=p), log_line(self.log, m)))
            self.after(0, on_done)

        threading.Thread(target=worker, daemon=True).start()

    def _on_escape(self, _e=None) -> None:
        self._dismiss_overlay()
        self.destroy()

    def _dismiss_overlay(self) -> None:
        if self._overlay_win and self._overlay_win.winfo_exists():
            self._overlay_win.destroy()
        self._overlay_win = None

    def _show_meme_popup(self) -> None:
        """透明浮层：只留人物+带派字，后面翻译器可见；点一下关闭。"""
        self._dismiss_overlay()

        try:
            img = load_rgba_image(max_width=290)
            iw, ih = img.size
            self.update_idletasks()
            ox, oy = self.winfo_rootx(), self.winfo_rooty()
            ow, oh = self.winfo_width(), self.winfo_height()
            px = ox + (ow - iw) // 2
            py = oy + int(oh * 0.32) - ih // 2

            win = show_transparent_meme(self, img, px, py, self._dismiss_overlay)
            if win is None:
                raise RuntimeError("透明浮层仅支持 Windows")
            self._overlay_win = win
            log_line(self.log, "梗图已弹出 · 点击关闭")
        except Exception as exc:
            log_line(self.log, f"!! 梗图弹出失败：{exc}")
            self._dismiss_overlay()

    def _start(self) -> None:
        if self._busy:
            return

        src = self._input.get("1.0", tk.END).strip()
        model = self._model.get()

        if not src:
            log_line(self.log, "!! 错误：文字输入不能为空")
            return
        if _empty_model(model):
            log_line(self.log, "!! 错误：请选择推理模型")
            return

        self._set_output("")
        self._busy = True
        self._run_fast(model, self._finish)

    def _finish(self) -> None:
        self._busy = False
        self._btn.configure(state="normal", text="▶  开始翻译")
        self._set_output(RESULT_TEXT)
        log_line(self.log, "输出已写入翻译显示区")
        self.after(1000, self._show_meme_popup)


def main() -> None:
    dpi_fix()
    App().mainloop()


if __name__ == "__main__":
    main()
