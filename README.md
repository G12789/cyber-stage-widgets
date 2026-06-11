# Cyber Stage Widgets · 赛博风桌面特效小组件

![License](https://img.shields.io/github/license/G12789/cyber-stage-widgets)
![Stars](https://img.shields.io/github/stars/G12789/cyber-stage-widgets?style=social)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)

> 一组**赛博朋克风格的桌面视觉特效小程序**（Python + tkinter）。
> 界面看起来像很专业的「AI 大模型软件」，但**不联网、不做任何真实计算**——输出全是预设/随机/马赛克化的搞笑结果。纯粹给短视频拍摄和整活用。
>
> A set of **novelty cyberpunk-style desktop visual-effect apps** (Python + tkinter). They look like serious "AI" tools but do **no real computation** — every output is fake/random by design. For fun and short-video content only.

---

## ⚠️ 重要声明 / Disclaimer

- 这些程序**没有任何真实功能**，不会处理、获取或存储任何真实数据。
- 所有"结果"都是写死的或随机生成的视觉效果（例如永远输出 `**********` 或满屏 `████`）。
- 仅供制作有趣的短视频，**请勿用于误导他人或冒充真实工具**。
- These apps have **no real functionality**, never touch real data, and exist purely for entertainment video content.

## 包含的特效 / Widgets

| 程序 | 看起来在做什么 | 实际效果 |
|------|----------------|----------|
| 翻译器 | 多语种 AI 翻译 | 不管输入什么，永远"翻译"成同一个梗 + 弹梗图 |
| 亲戚称呼学习器 | 大模型算亲戚称谓 | 一本正经算出搞笑的称呼（姥姥的弟弟→姥弟） |
| 生僻字发音器 | OCR + 神经 TTS 读生僻字 | 假装查字典，其实把你输入的字原样念回去 |
| 赛博解码特效 | 黑客风"解码"动画 | 进度跑满后结果永远是 `**********` |
| 赛博定位特效 | "机密信息"检索演出 | 所有字段都是 `████` 马赛克，纯视觉效果 |

## 运行 / Run

需要 **Windows + Python 3.10+**。

1. 双击 `00_检测环境.bat` 看缺什么（没装 Python 会给安装提示）
2. 双击 `00_安装依赖.bat` 安装依赖（见 `requirements.txt`）
3. 双击任意 `启动_xxx.bat` 运行对应特效
4. 大部分窗口按 `ESC` 退出；翻译器梗图弹窗点一下关闭

命令行运行（可选）：

```bash
pip install -r requirements.txt
python 抖音AI爆款/翻译器.py
```

## 技术栈 / Stack

`Python 3` · `tkinter`（GUI）· `Pillow`（部分弹窗素材）· 可选 `pywin32`（透明弹窗更稳）

## 目录结构 / Layout

```
启动_*.bat          一键启动各特效
00_*.bat            环境检测 / 依赖安装
抖音AI爆款/         全部 Python 源码与素材
requirements.txt    依赖清单
```

## License

[MIT](./LICENSE)
