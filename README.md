# overcooked-with-AI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [中文](README.zh.md)

> 🎮 A lightweight CLI tool for human-AI collaboration testing in Overcooked environments.

overcooked-with-AI allows you to play Overcooked with trained AI agents directly from your terminal. Test your coordination skills against state-of-the-art algorithms like BACH, FCP, and MEP!

---

## ✨ Features

- 🚀 **Easy to Install** - One-command installation with pip
- 🎮 **Interactive Gameplay** - Real-time keyboard controls
- 🤖 **Multiple AI Agents** - Test against BACH, FCP, MEP, and more
- 💻 **Cross-Platform** - Works on Windows, Ubuntu, and macOS
- 🖥️ **Terminal-Based** - No GUI required, runs in any terminal
- 📊 **Result Tracking** - Automatic scoring and statistics

---

## 📦 Installation

### Requirements

- Python 3.9+
- Terminal with Unicode support
- (macOS only) Input Monitoring permission for your terminal

### Quick Install

```bash
cd ~/ZSC/ZSC-Eval/human_test
pip install -e .
```

### macOS Permission Setup (Important!)

On macOS, you need to grant Input Monitoring permission to your terminal:

1. Open **System Settings** → **Privacy & Security** → **Input Monitoring**
2. Click **+** to add your terminal app (Terminal or iTerm)
3. Check the box next to your terminal app
4. **Restart your terminal**

---

## 🚀 Quick Start

### Option 1: Interactive Quickstart

```bash
python quickstart.py
```

### Option 2: Direct Usage

```bash
# Basic test
overcooked-with-ai --env random0_m --algo bach

# Human as Player 1
overcooked-with-ai -e random0_m -a bach -p 1

# Multiple episodes
overcooked-with-ai -e random0_m -a bach -n 5
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move Up |
| `S` / `↓` | Move Down |
| `A` / `←` | Move Left |
| `D` / `→` | Move Right |
| `Space` | Interact (pick up / put down / cook) |
| `P` | Pause |
| `Q` / `ESC` | Quit |

---

## 🗺️ Available Environments

- `random0_m` - Basic kitchen layout
- `random3_m` - Three-ingredient kitchen
- `forced_coordination` - Forced cooperation scenario
- `asymmetric_advantages` - Asymmetric advantages

List all environments:
```bash
overcooked-with-ai --list-envs
```

---

## 🤖 Available Algorithms

| Algorithm | Description |
|-----------|-------------|
| `bach` | **BACH** (Recommended) - Büchi Automata Conditioned Harmony |
| `fcp` | Fictitious Co-Play |
| `mep` | Maximum Entropy Population |
| `trajedi` | Trajectory Diversity |
| `hsp` | Hidden Utility Self-Play |
| `cole` | Open-Ended Learning |
| `sp` | Self-Play |

List all algorithms:
```bash
overcooked-with-ai --list-algos
```

---

## 📚 Documentation

- [CLI Documentation](CLI.md) - Full command-line reference
- [Installation Guide](INSTALL.md) - Detailed installation for all platforms
- [中文文档](README.zh.md) - Chinese documentation

---

## 🏗️ Project Structure

```
human_test/
├── README.md              # This file
├── README.zh.md           # Chinese documentation
├── INSTALL.md             # Installation guide
├── CLI.md                 # CLI reference
├── setup.py               # Package setup
├── quickstart.py          # Interactive quickstart ⭐
├── test_install.py        # Installation test
├── configs/               # Configuration files
├── human_test/            # Core source code
│   ├── cli.py             # CLI entry point
│   ├── core.py            # Game logic
│   ├── keyboard.py        # Keyboard handling
│   ├── renderer.py        # Terminal rendering
│   └── utils.py           # Utilities
└── examples/              # Example scripts
    ├── batch_test.sh
    ├── compare_algos.py
    └── custom_policy.py
```

---

## 🐛 Troubleshooting

### Keyboard input not working (macOS)

```bash
# Reset Input Monitoring permissions
sudo tccutil reset All com.apple.Terminal

# Or for iTerm2
sudo tccutil reset All com.googlecode.iterm2
```

Then re-add your terminal in System Settings → Privacy & Security → Input Monitoring.

### Display issues

```bash
# Use ASCII mode for better compatibility
overcooked-with-ai -e random0_m -a bach -r ascii
```

### Policy loading fails

```bash
# Set policy pool path
export POLICY_POOL=/path/to/policy_pool

# Or use custom config
overcooked-with-ai -e random0_m -a bach --policy-path /path/to/config.yml
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.

---

## 🙏 Acknowledgments

This tool is part of the [ZSC-Eval](https://github.com/your-org/ZSC-Eval) project for multi-agent zero-shot coordination research.