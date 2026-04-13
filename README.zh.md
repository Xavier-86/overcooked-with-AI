# overcooked-with-AI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [中文](README.zh.md)

> 🎮 在 Overcooked 环境中进行人机协作测试的轻量级命令行工具。

overcooked-with-AI 让你可以直接在终端中与训练好的 AI 智能体一起玩 Overcooked。测试你与 BACH、FCP、MEP 等先进算法的协作能力！

---

## ✨ 特性

- 🚀 **安装简单** - 一条 pip 命令完成安装
- 🎮 **交互式游戏** - 实时键盘控制
- 🤖 **多种 AI 智能体** - 测试 BACH、FCP、MEP 等多种算法
- 💻 **跨平台** - 支持 Windows、Ubuntu 和 macOS
- 🖥️ **纯终端** - 无需 GUI，在任何终端中运行
- 📊 **结果追踪** - 自动计分和统计

---

## 📦 安装

### 环境要求

- Python 3.9+
- 支持 Unicode 的终端
- (macOS 额外) 终端需要输入监控权限

### 快速安装

```bash
cd ~/ZSC/ZSC-Eval/human_test
pip install -e .
```

### macOS 权限设置 (重要!)

在 macOS 上，需要授予终端输入监控权限：

1. 打开 **系统设置** → **隐私与安全性** → **输入监控**
2. 点击 **+** 添加终端应用 (Terminal 或 iTerm)
3. 勾选终端应用旁边的复选框
4. **重启终端**

---

## 🚀 快速开始

### 方式 1: 交互式快速开始

```bash
python quickstart.py
```

### 方式 2: 直接使用

```bash
# 基础测试
overcooked-with-ai --env random0_m --algo bach

# 人类作为 Player 1
overcooked-with-ai -e random0_m -a bach -p 1

# 多局测试
overcooked-with-ai -e random0_m -a bach -n 5
```

---

## 🎮 控制说明

| 按键 | 动作 |
|-----|------|
| `W` / `↑` | 向上移动 |
| `S` / `↓` | 向下移动 |
| `A` / `←` | 向左移动 |
| `D` / `→` | 向右移动 |
| `空格` | 交互 (拾取/放下/烹饪) |
| `P` | 暂停 |
| `Q` / `ESC` | 退出 |

---

## 🗺️ 可用环境

- `random0_m` - 基础厨房布局
- `random3_m` - 三原料厨房
- `forced_coordination` - 强制协作场景
- `asymmetric_advantages` - 非对称优势

查看所有环境：
```bash
overcooked-with-ai --list-envs
```

---

## 🤖 可用算法

| 算法 | 说明 |
|------|------|
| `bach` | **BACH** (推荐) - Büchi 自动机条件协调 |
| `fcp` | Fictitious Co-Play |
| `mep` | Maximum Entropy Population |
| `trajedi` | Trajectory Diversity |
| `hsp` | Hidden Utility Self-Play |
| `cole` | Open-Ended Learning |
| `sp` | Self-Play |

查看所有算法：
```bash
overcooked-with-ai --list-algos
```

---

## 📚 文档

- [CLI 文档](CLI.md) - 完整命令行参考
- [安装指南](INSTALL.md) - 各平台详细安装说明
- [English Docs](README.md) - 英文文档

---

## 🏗️ 项目结构

```
human_test/
├── README.md              # 本文件
├── README.zh.md           # 中文文档
├── INSTALL.md             # 安装指南
├── CLI.md                 # CLI 参考
├── setup.py               # 包配置
├── quickstart.py          # 交互式快速开始 ⭐
├── test_install.py        # 安装测试
├── configs/               # 配置文件
├── human_test/            # 核心源代码
│   ├── cli.py             # CLI 入口
│   ├── core.py            # 游戏逻辑
│   ├── keyboard.py        # 键盘处理
│   ├── renderer.py        # 终端渲染
│   └── utils.py           # 工具函数
└── examples/              # 示例脚本
    ├── batch_test.sh
    ├── compare_algos.py
    └── custom_policy.py
```

---

## 🐛 故障排除

### 键盘输入无响应 (macOS)

```bash
# 重置输入监控权限
sudo tccutil reset All com.apple.Terminal

# iTerm2 用户
sudo tccutil reset All com.googlecode.iterm2
```

然后在 系统设置 → 隐私与安全性 → 输入监控 中重新添加终端。

### 显示问题

```bash
# 使用 ASCII 模式获得更好兼容性
overcooked-with-ai -e random0_m -a bach -r ascii
```

### 策略加载失败

```bash
# 设置策略池路径
export POLICY_POOL=/path/to/policy_pool

# 或使用自定义配置
overcooked-with-ai -e random0_m -a bach --policy-path /path/to/config.yml
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License - 详见 [LICENSE](../LICENSE)

---

## 🙏 致谢

本工具是 [ZSC-Eval](https://github.com/your-org/ZSC-Eval) 多智能体零样本协调研究项目的一部分。