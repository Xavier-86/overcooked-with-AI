# overcooked-with-AI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [中文](README.zh.md)

> 🎮 使用 Pygame 渲染的 Overcooked 人机协作测试工具

**overcooked-with-AI** 让你可以用原始游戏画面与训练好的 AI 智能体一起玩 Overcooked。测试你与 BACH、FCP、MEP 等先进算法的协作能力！

---

## ✨ 特性

- 🚀 **易于安装** - 一行命令 pip 安装
- 🎮 **Pygame 渲染** - 使用原版 Overcooked AI 图形
- 🤖 **多种 AI 算法** - 支持 BACH、FCP、MEP 等
- 💻 **跨平台** - 支持 Windows、Ubuntu 和 macOS
- 🖱️ **键盘控制** - 实时 WASD + 空格控制
- 📊 **成绩追踪** - 自动记录分数和统计信息

---

## 📦 安装

### 环境要求

- Python 3.9+
- Pygame (`pip install pygame`)
- ZSC-Eval 项目依赖

### 快速安装

```bash
cd ~/ZSC/ZSC-Eval/human_test
pip install -e .
```

### 安装依赖

```bash
pip install pygame numpy
```

---

## 🚀 快速开始

### 运行游戏

```bash
# 基础测试（人类作为 Player 0）
python -m human_test.cli -e random0_m -a bach

# 人类作为 Player 1
python -m human_test.cli -e random0_m -a bach -p 1

# 多局测试
python -m human_test.cli -e random0_m -a bach -n 5

# 更大的图块（更容易看清）
python -m human_test.cli -e random0_m -a bach --tile-size 100
```

---

## 🎮 控制方式

| 按键 | 动作 |
|-----|--------|
| `W` / `↑` | 向上移动 |
| `S` / `↓` | 向下移动 |
| `A` / `←` | 向左移动 |
| `D` / `→` | 向右移动 |
| `空格` / `E` | 交互（拾取/放下/烹饪） |
| `Q` | 退出 |

---

## 🗺️ 可用地图

- `random0_m` - 基础厨房布局
- `random3_m` - 三种食材厨房
- `forced_coordination` - 强制协作场景
- `asymmetric_advantages` - 非对称优势
- `cramped_room` - 小厨房

---

## 🤖 可用算法

| 算法 | 说明 |
|-----------|-------------|
| `bach` | **BACH** - Büchi 自动机条件协调 |
| `fcp` | Fictitious Co-Play |
| `mep` | Maximum Entropy Population |
| `trajedi` | Trajectory Diversity |
| `hsp` | Hidden Utility Self-Play |
| `cole` | Open-Ended Learning |
| `sp` | Self-Play |

---

## 📄 许可证

MIT 许可证 - 详情见 [LICENSE](../LICENSE)
