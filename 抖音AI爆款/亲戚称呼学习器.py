# -*- coding: utf-8 -*-
"""亲戚称呼学习器 KinshipLearn — 大模型族谱学习，学出来全是梗。ESC 退出。"""
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
    cyber_combobox,
    dpi_fix,
    log_line,
    run_boot,
    run_steps,
    setup_cyber_style,
    show_report,
)

APP_NAME = "亲戚称呼学习器"
VERSION = "KinshipLearn v2.1"
PLACEHOLDER_REL = "请选择"
PLACEHOLDER_MODEL = "请选择模型"
RELATIVES = ["老公", "老婆", "爸爸", "妈妈", "弟弟", "妹妹", "爷爷", "奶奶", "姥姥", "姥爷", "哥哥", "姐姐", "儿子", "女儿"]
MODELS = [
    "Claude Opus 4.8",
    "GPT-5.2 Pro",
    "Gemini 3 Ultra",
    "DeepSeek-R1 · 671B",
    "Qwen-Max 3.0",
    "Grok-4 Heavy",
]


def _is_empty_choice(value: str, placeholder: str) -> bool:
    return not value or value.strip() == "" or value == placeholder


def _pick_title(r1: str, r2: str) -> str:
    if r1 == "姥姥" and r2 == "弟弟":
        return "姥弟"
    if r1 == "妈妈" and r2 == "爷爷":
        return "妈耶！"
    if r1 == "奶奶" and r2 == "弟弟":
        return "奶奶滴！"
    pool = [
        f"{r1[:1]}{r2[-1:] if r2 else '弟'}",
        f"{r2}{r1[-1:] if r1 else ''}",
        f"{r1}他{r2}",
        f"{r1}{r2}",
        "亲戚关系断绝",
        "建议直接喊「喂」",
    ]
    return random.choice(pool)


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
            "LLM · 族谱图谱 · 推理链",
            [
                "加载大模型亲属权重 …",
                "同步全国族谱节点 8.4 万 …",
                "学习引擎就绪",
            ],
            self._build_main,
        )

    def _build_main(self) -> None:
        self._widgets = build_shell(
            self,
            app_name=APP_NAME,
            version=VERSION,
            subtitle="",
            status_bar="引擎：在线  |  族谱节点：84,127  |  推理深度：7  |  可信度：看起来很高",
            btn_text="▶  开始计算",
            on_run=self._start,
        )
        form = self._widgets["body"]

        tk.Label(form, text="亲戚 1", font=("Microsoft YaHei UI", 10), fg=DIM, bg=BG, width=8, anchor="e").grid(
            row=0, column=0, pady=8
        )
        self._r1 = tk.StringVar(value=PLACEHOLDER_REL)
        cyber_combobox(form, self._r1, [PLACEHOLDER_REL] + RELATIVES).grid(row=0, column=1, sticky="w", padx=(8, 0))

        tk.Label(form, text="亲戚 2", font=("Microsoft YaHei UI", 10), fg=DIM, bg=BG, width=8, anchor="e").grid(
            row=1, column=0, pady=8
        )
        self._r2 = tk.StringVar(value=PLACEHOLDER_REL)
        cyber_combobox(form, self._r2, [PLACEHOLDER_REL] + RELATIVES).grid(row=1, column=1, sticky="w", padx=(8, 0))

        tk.Label(form, text="模　型", font=("Microsoft YaHei UI", 10), fg=DIM, bg=BG, width=8, anchor="e").grid(
            row=2, column=0, pady=8
        )
        self._model = tk.StringVar(value=PLACEHOLDER_MODEL)
        cyber_combobox(form, self._model, [PLACEHOLDER_MODEL] + MODELS).grid(row=2, column=1, sticky="w", padx=(8, 0))

        self._deep = tk.BooleanVar(value=False)
        tk.Checkbutton(
            form,
            text="大模型深度推理",
            variable=self._deep,
            font=("Microsoft YaHei UI", 9),
            fg="#8ab4c7",
            bg=BG,
            activebackground=BG,
            activeforeground=CYAN,
            selectcolor="#1a2830",
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(4, 0))

        log_line(self._widgets["log"], "KinshipLearn 在线。等待亲属关系输入 …")

    def _start(self) -> None:
        if self._busy:
            return

        r1, r2 = self._r1.get().strip(), self._r2.get().strip()
        model = self._model.get().strip()

        if _is_empty_choice(r1, PLACEHOLDER_REL):
            log_line(self._widgets["log"], "!! 错误：请先选择亲戚 1")
            return
        if _is_empty_choice(r2, PLACEHOLDER_REL):
            log_line(self._widgets["log"], "!! 错误：请先选择亲戚 2")
            return
        if _is_empty_choice(model, PLACEHOLDER_MODEL):
            log_line(self._widgets["log"], "!! 错误：请先选择推理模型")
            return

        self._busy = True
        steps = [
            (10, "正在使用大模型思考计算 …"),
            (20, f"接入 {model} 推理核心 … OK"),
            (28, f"解析节点 [{r1}] → [{r2}] …"),
            (48, "拓扑排序姻亲分支 …"),
            (68, "生成称谓候选池 …"),
            (88, "交叉验证伦理约束（已通过）…"),
            (100, "学习完成 · 报告就绪"),
        ]
        if self._deep.get():
            steps.insert(3, (55, "激活 7 层 Transformer 亲属注意力 …"))

        run_steps(self, self._widgets, steps, lambda: self._finish(r1, r2, model))

    def _finish(self, r1: str, r2: str, model: str) -> None:
        self._busy = False
        self._widgets["btn"].configure(state="normal", text="▶  开始计算")
        title = _pick_title(r1, r2)
        show_report(
            self,
            "亲属称谓学习报告",
            [
                ("亲戚 1", r1),
                ("亲戚 2", r2),
                ("推理模型", model),
                ("称　　谓", title),
                ("准 确 度", "100%"),
                ("可 用 度", "0%"),
            ],
            punchline=f"恭喜您，{r1}的{r2}叫：{title}",
            easter="（族谱没学明白，但大模型看起来很专业）",
        )


def main() -> None:
    dpi_fix()
    App().mainloop()


if __name__ == "__main__":
    main()
