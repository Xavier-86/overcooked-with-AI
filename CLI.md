# overcooked-with-AI CLI Documentation

[English](CLI.md) | [中文](CLI.zh.md)

Complete command-line reference for overcooked-with-AI.

---

## Synopsis

```bash
overcooked-with-ai [OPTIONS]
```

---

## Options

### Required Arguments

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--env` | `-e` | Environment name | `random0_m`, `random3_m` |
| `--algo` | `-a` | AI algorithm | `bach`, `fcp`, `mep` |

### Optional Arguments

| Option | Short | Description | Default | Example |
|--------|-------|-------------|---------|---------|
| `--human-player` | `-p` | Human player position (0 or 1) | 0 | `-p 1` |
| `--policy-path` | | Custom policy path | Auto | `--policy-path /path/to/policy` |
| `--episodes` | `-n` | Number of episodes | 1 | `-n 5` |
| `--render-mode` | `-r` | Render mode: `cli` or `ascii` | cli | `-r ascii` |
| `--seed` | `-s` | Random seed | None | `-s 42` |
| `--dry-run` | | Check environment only | False | `--dry-run` |
| `--help` | `-h` | Show help | - | `-h` |
| `--version` | `-v` | Show version | - | `-v` |

### List Commands

| Option | Description |
|--------|-------------|
| `--list-envs` | List all available environments |
| `--list-algos` | List all available algorithms |

---

## Usage Examples

### Basic Usage

```bash
# Test with BACH algorithm on random0_m
overcooked-with-ai --env random0_m --algo bach

# Shorthand
overcooked-with-ai -e random0_m -a bach
```

### Specify Human Player Position

```bash
# Human as Player 0 (default)
overcooked-with-ai -e random0_m -a bach -p 0

# Human as Player 1
overcooked-with-ai -e random0_m -a bach -p 1
```

### Multiple Episodes

```bash
# Run 5 episodes continuously
overcooked-with-ai -e random0_m -a bach -n 5
```

### Different Render Modes

```bash
# CLI mode (default, Unicode borders)
overcooked-with-ai -e random0_m -a bach -r cli

# ASCII mode (better compatibility)
overcooked-with-ai -e random0_m -a bach -r ascii
```

### Environment Check

```bash
# Verify environment and model loading without starting game
overcooked-with-ai -e random0_m -a bach --dry-run
```

### Custom Policy

```bash
# Load your own trained policy
overcooked-with-ai -e random0_m --policy-path /path/to/your/policy.yml
```

---

## Available Environments

List all environments:
```bash
overcooked-with-ai --list-envs
```

Common environments:

| Environment | Description |
|-------------|-------------|
| `random0_m` | Basic kitchen (recommended for beginners) |
| `random3_m` | Three-ingredient kitchen |
| `forced_coordination` | Forced cooperation |
| `asymmetric_advantages` | Asymmetric advantages |

---

## Available Algorithms

List all algorithms:
```bash
overcooked-with-ai --list-algos
```

Common algorithms:

| Algorithm | Type |
|-----------|------|
| `bach` | BACH (recommended, SOTA performance) |
| `fcp` | Fictitious Co-Play |
| `mep` | Maximum Entropy Population |
| `trajedi` | Trajectory Diversity |
| `hsp` | Hidden Utility Self-Play |
| `sp` | Self-Play (baseline) |

---

## Environment Variables

Configure tool behavior via environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `POLICY_POOL` | Policy root directory | `/path/to/policies` |
| `HUMAN_TEST_LOG_LEVEL` | Log level | `DEBUG`, `INFO`, `WARNING` |
| `HUMAN_TEST_NO_COLOR` | Disable color output | `1` or `true` |

Example:

```bash
# Use custom policy directory
export POLICY_POOL=/home/user/my_policies
overcooked-with-ai -e random0_m -a bach

# Disable color output
export HUMAN_TEST_NO_COLOR=1
overcooked-with-ai -e random0_m -a bach
```

---

## In-Game Controls

During gameplay:

| Key | Action |
|-----|--------|
| `W` or `↑` | Move Up |
| `S` or `↓` | Move Down |
| `A` or `←` | Move Left |
| `D` or `→` | Move Right |
| `Space` | Interact (pick up / put down / cook) |
| `P` | Pause/Resume |
| `Q` or `ESC` | Quit |

---

## Output Explanation

Game interface displays:

```
╔════════════════════════════════════════════════════════════╗
║ Map: random0_m    Algo: bach-S2    You: Player 0           ║
╠════════════════════════════════════════════════════════════╣
║  [Kitchen visualization]                                   ║
╠════════════════════════════════════════════════════════════╣
║  Score: 120  |  Time: 45s  |  Episode: 1/3                 ║
╚════════════════════════════════════════════════════════════╝
```

- **Score**: Current game score
- **Time**: Elapsed time
- **Episode**: Current episode (if `-n > 1`)

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Normal exit |
| 1 | Argument error |
| 2 | Environment loading failed |
| 3 | Policy loading failed |
| 4 | Runtime error |
| 130 | User interrupt (Ctrl+C) |

---

## Script Examples

### Batch Test Script

```bash
#!/bin/bash
# test_all_algos.sh

ENVS=("random0_m" "random3_m")
ALGOS=("bach" "fcp" "mep")

for env in "${ENVS[@]}"; do
    for algo in "${ALGOS[@]}"; do
        echo "Testing $algo on $env..."
        overcooked-with-ai -e "$env" -a "$algo" -n 3
    done
done
```

### Python Integration

```python
from human_test.core import HumanTest

# Create test instance
test = HumanTest(
    env_name="random0_m",
    algo="bach",
    human_player=0,
    episodes=5
)

# Run test
test.run()

# Get results
results = test.get_results()
print(f"Average score: {results['avg_score']}")
```

---

## Troubleshooting

### Keyboard Input Not Responding

**Solution:**
- Ensure terminal window has focus
- Try running with administrator privileges (Windows)
- Check if pynput is installed: `pip install pynput`

**macOS Specific:**
```bash
# 1. Ensure terminal has Input Monitoring permission
# System Settings → Privacy & Security → Input Monitoring → Add terminal

# 2. If still not working, try resetting permissions
sudo tccutil reset All com.apple.Terminal

# 3. Restart terminal and retry
```

### Game Display Issues

**Solution:**
```bash
# Use ASCII mode
overcooked-with-ai -e random0_m -a bach -r ascii

# Disable color
export HUMAN_TEST_NO_COLOR=1
overcooked-with-ai -e random0_m -a bach
```

### Policy Loading Fails

**Solution:**
```bash
# Check policy path
overcooked-with-ai -e random0_m -a bach --dry-run

# Use custom path
overcooked-with-ai -e random0_m --policy-path /absolute/path/to/policy.yml
```

---

## Getting Help

```bash
# Show help
overcooked-with-ai --help

# Check version
overcooked-with-ai --version
```

For more information, see [README.md](README.md) or [INSTALL.md](INSTALL.md).