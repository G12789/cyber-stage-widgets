# -*- coding: utf-8 -*-
"""生僻字发音器 GlyphSpeak — 大模型语音推理，读出来就是原文。ESC 退出。"""
from __future__ import annotations

import random
import sys
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _cyber_toy_ui import (
    BG,
    CYAN,
    DIM,
    apply_record_frame,
    build_shell,
    cyber_entry,
    dpi_fix,
    log_line,
    run_boot,
    run_steps,
    setup_cyber_style,
    show_report,
)

APP_NAME = "生僻字发音器"
VERSION = "GlyphSpeak v3.0"


def _pick_reading(word: str) -> str:
    w = word.strip() or "龘"
    styles = [
        w,
        f"「{w}」",
        f"/{w}/",
        f"{w}（四声）",
    ]
    return random.choice(styles)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME}  {VERSION}")
        self.configure(bg=BG)
        setup_cyber_style(self)
        apply_record_frame(self)
        self.bind("<Escape>", lambda _e: self.destroy())

        self._busy = False
        self._widgets: dict = {}
        run_boot(
            self,
            APP_NAME,
            "OCR · TTS · 语义向量",
            [
                "挂载字形向量数据库 …",
                "预热语音合成大模型 …",
                "GlyphSpeak 引擎就绪",
            ],
            self._build_main,
        )

    def _build_main(self) -> None:
        self._widgets = build_shell(
            self,
            app_name=APP_NAME,
            version=VERSION,
            subtitle="",
            status_bar="引擎：在线  |  字库：17,042  |  采样率：48kHz  |  可信度：看起来很高",
            btn_text="▶  开始计算",
            on_run=self._start,
        )
        form = self._widgets["body"]

        tk.Label(form, text="生僻字", font=("Microsoft YaHei UI", 10), fg=DIM, bg=BG, width=8, anchor="e").grid(
            row=0, column=0, pady=10
        )
        self._word = cyber_entry(form, width=28)
        self._word.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=10)
        self._word.insert(0, "龘靐齉")
        form.columnconfigure(1, weight=1)

        self._tts = tk.BooleanVar(value=True)
        tk.Checkbutton(
            form,
            text="启用神经 TTS 合成",
            variable=self._tts,
            font=("Microsoft YaHei UI", 9),
            fg="#8ab4c7",
            bg=BG,
            activebackground=BG,
            activeforeground=CYAN,
            selectcolor="#1a2830",
        ).grid(row=1, column=0, columnspan=2, sticky="w")

        log_line(self._widgets["log"], "GlyphSpeak 在线。等待输入生僻字 …")

    def _start(self) -> None:
        if self._busy:
            return
        word = self._word.get().strip()
        if not word:
            log_line(self._widgets["log"], "!! 错误：未输入任何字符")
            return

        self._busy = True
        preview = word if len(word) <= 6 else word[:5] + "…"
        steps = [
            (10, "正在使用大模型思考计算 …"),
            (30, f"OCR 锁定字形 [{preview}] …"),
            (50, "检索《康熙字典》向量索引 …"),
            (72, "语义消歧 · 多音字排除 …"),
            (92, "TTS 波形合成中 …"),
            (100, "发音推理完成 · 报告就绪"),
        ]
        if self._tts.get():
            steps.insert(4, (62, "激活神经语音合成通道 …"))

        run_steps(self, self._widgets, steps, lambda: self._finish(word))

    def _finish(self, word: str) -> None:
        self._busy = False
        self._widgets["btn"].configure(state="normal", text="▶  开始计算")
        reading = _pick_reading(word)
        show_report(
            self,
            "字形发音推理报告",
            [
                ("输入字形", word if len(word) <= 12 else word[:10] + "…"),
                ("推理模型", "GlyphSpeak-7B"),
                ("读　　音", reading),
                ("推理耗时", f"{random.uniform(4.5, 8.2):.1f} 秒（含装样子）"),
                ("准 确 度", "100%"),
                ("可 用 度", "0%"),
            ],
            punchline=f"恭喜您，发音为：{reading}",
            easter="（其实没查字典，就是把您输入的字又念了一遍）",
        )


def main() -> None:
    dpi_fix()
    App().mainloop()


if __name__ == "__main__":
    main()
