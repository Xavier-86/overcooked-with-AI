# overcooked-with-AI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [中文](README.zh.md)

> 🎮 Human-AI collaboration testing in Overcooked with Pygame rendering.

**overcooked-with-AI** allows you to play Overcooked with trained AI agents using the original game graphics. Test your coordination skills against state-of-the-art algorithms like BACH, FCP, and MEP!

---

## ✨ Features

- 🚀 **Easy to Install** - One-command installation with pip
- 🎮 **Pygame Rendering** - Uses original Overcooked AI graphics
- 🤖 **Multiple AI Agents** - Test against BACH, FCP, MEP, and more
- 💻 **Cross-Platform** - Works on Windows, Ubuntu, and macOS
- 🖱️ **Keyboard Controls** - Real-time WASD + Space controls
- 📊 **Result Tracking** - Automatic scoring and statistics

---

## 📦 Installation

### Requirements

- Python 3.9+
- Pygame (`pip install pygame`)
- ZSC-Eval project dependencies

### Quick Install

```bash
cd ~/ZSC/ZSC-Eval/human_test
pip install -e .
```

### Install Dependencies

```bash
pip install pygame numpy
```

---

## 🚀 Quick Start

### Run the Game

```bash
# Basic test (Human as Player 0)
python -m human_test.cli -e random0_m -a bach

# Human as Player 1
python -m human_test.cli -e random0_m -a bach -p 1

# Multiple episodes
python -m human_test.cli -e random0_m -a bach -n 5

# Larger tiles (easier to see)
python -m human_test.cli -e random0_m -a bach --tile-size 100
```

---

## 🎮 Controls

| Key | Action |
|-----|--------|
| `W` / `↑` | Move Up |
| `S` / `↓` | Move Down |
| `A` / `←` | Move Left |
| `D` / `→` | Move Right |
| `Space` / `E` | Interact (pick up / put down / cook) |
| `Q` | Quit |

---

## 🗺️ Available Environments

- `random0_m` - Basic kitchen layout
- `random3_m` - Three-ingredient kitchen
- `forced_coordination` - Forced cooperation scenario
- `asymmetric_advantages` - Asymmetric advantages
- `cramped_room` - Small kitchen

---

## 🤖 Available Algorithms

| Algorithm | Description |
|-----------|-------------|
| `bach` | **BACH** - Büchi Automata Conditioned Harmony |
| `fcp` | Fictitious Co-Play |
| `mep` | Maximum Entropy Population |
| `trajedi` | Trajectory Diversity |
| `hsp` | Hidden Utility Self-Play |
| `cole` | Open-Ended Learning |
| `sp` | Self-Play |

---

## 📚 Documentation

- [Installation Guide](INSTALL.md) - Detailed installation for all platforms
- [中文文档](README.zh.md) - Chinese documentation

---

## 🏗️ Project Structure

```
human_test/
├── README.md              # This file
├── README.zh.md           # Chinese documentation
├── INSTALL.md             # Installation guide
├── setup.py               # Package setup
├── requirements.txt       # Python dependencies
├── human_test/            # Core source code
│   ├── __init__.py
│   ├── cli.py             # CLI entry point
│   ├── pygame_core.py     # Pygame game logic ⭐
│   ├── keyboard.py        # Keyboard handling
│   └── utils.py           # Utilities
└── examples/              # Example scripts
```

---

## 🐛 Troubleshooting

### Pygame not found

```bash
pip install pygame
```

### ZSC-Eval not found

```bash
# Add ZSC-Eval to Python path
export PYTHONPATH="${PYTHONPATH}:~/ZSC/ZSC-Eval"
```

### Policy loading fails

```bash
# Set policy pool path
export POLICY_POOL=/path/to/policy_pool
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
