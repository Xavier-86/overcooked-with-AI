# Installation Guide

[English](INSTALL.md) | [中文](INSTALL.zh.md)

Complete installation instructions for Windows, Ubuntu, and macOS.

---

## System Requirements

- **OS**: Windows 10+ / Ubuntu 20.04+ / macOS 10.15+
- **Python**: 3.9 or higher
- **Terminal**: Unicode and color support
  - Windows: Windows Terminal, PowerShell, CMD
  - Ubuntu: GNOME Terminal, Konsole, xterm
  - macOS: Terminal, iTerm2

## Quick Installation

### Step 1: Navigate to Project Directory

```bash
cd ~/ZSC/ZSC-Eval/human_test
```

### Step 2: Install Dependencies

```bash
# Using pip
pip install -e .

# Or using conda
conda install -c conda-forge pynput
pip install -e .
```

### Step 3: Verify Installation

```bash
overcooked-with-ai --help
```

## macOS Installation

### Method 1: Direct Install (Recommended)

```bash
# Navigate to project directory
cd ~/ZSC/ZSC-Eval/human_test

# Install dependencies
pip install -e .

# Verify installation
overcooked-with-ai --help
```

### Method 2: Using Homebrew

```bash
# Ensure Homebrew is installed, then install Python
brew install python@3.9

# Navigate to project directory
cd ~/ZSC/ZSC-Eval/human_test

# Install
pip3 install -e .

# Run test
overcooked-with-ai --env random0_m --algo bach
```

### Method 3: Using Conda

```bash
# Create conda environment
conda create -n human_test python=3.9
conda activate human_test

# Install
pip install -e .

# Run
overcooked-with-ai --env random0_m --algo bach
```

### macOS Permission Setup (Important!)

**Input Monitoring Permission**: Required on first run

1. Open **System Settings** → **Privacy & Security** → **Input Monitoring**
2. Click **+** to add your terminal app (Terminal or iTerm)
3. Check the box next to your terminal app
4. **Restart your terminal**

Or via command line:
```bash
# Add Terminal to Input Monitoring (requires admin password)
sudo tccutil reset All com.apple.Terminal

# For iTerm2
sudo tccutil reset All com.googlecode.iterm2
```

**Accessibility Permission** (if pynput has issues):
1. Open **System Settings** → **Privacy & Security** → **Accessibility**
2. Add and enable your terminal app

### macOS Common Issues

**Issue 1: Keyboard input not responding**

**Solution:**
```bash
# 1. Ensure terminal has Input Monitoring permission (see above)

# 2. Try running in safe mode
# Restart Mac and hold Shift key to enter safe mode for testing

# 3. Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**Issue 2: pynput installation fails**

**Solution:**
```bash
# Install Xcode command line tools
xcode-select --install

# Then reinstall pynput
pip install --upgrade --force-reinstall pynput
```

**Issue 3: Display encoding issues**

**Solution:**
```bash
# Set UTF-8 encoding
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Use ASCII mode
overcooked-with-ai -e random0_m -a bach -r ascii
```

**Issue 4: Game display flickering**

**Solution:**
```bash
# Use iTerm2 instead of Terminal
# Or adjust render speed
export HUMAN_TEST_RENDER_DELAY=0.2
```

## Detailed Installation

### Windows Installation

#### Method 1: Using pip (Recommended)

```powershell
# Open PowerShell or CMD
cd C:\path\to\ZSC-Eval\human_test

# Install
pip install -e .

# Verify
overcooked-with-ai --help
```

#### Method 2: Using Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install
pip install -e .

# Run
overcooked-with-ai --env random0_m --algo bach
```

#### Windows Common Issues

**Issue 1: `pynput` installation fails**

```powershell
# Install Visual C++ Build Tools
# Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use precompiled version
pip install pynput --only-binary :all:
```

**Issue 2: Terminal display garbled**

```powershell
# Set encoding in PowerShell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Or use Windows Terminal (recommended)
```

### Ubuntu Installation

#### Method 1: Direct Install

```bash
cd ~/ZSC/ZSC-Eval/human_test

# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip

# Install Python packages
pip3 install -e .

# Verify
overcooked-with-ai --help
```

#### Method 2: Using Conda Environment

```bash
# Create conda environment
conda create -n human_test python=3.9
conda activate human_test

# Install
pip install -e .

# Run
overcooked-with-ai --env random0_m --algo bach
```

#### Ubuntu Common Issues

**Issue 1: Permission denied**

```bash
# Install with --user
pip install --user -e .

# Or use sudo
sudo pip install -e .
```

**Issue 2: Keyboard input not responding**

```bash
# Ensure permission to access input devices
sudo usermod -a -G input $USER

# Takes effect after re-login
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `pynput` | >=1.7.0 | Keyboard monitoring |
| `numpy` | >=1.20.0 | Numerical computation |
| `colorama` | >=0.4.0 | Windows terminal color support |
| `zsceval` | - | Core evaluation framework |

## Pre-trained Models

After installation, ensure pre-trained models are downloaded:

```bash
# Models should be located at
~/ZSC/ZSC-Eval/policy_pool/

# Check if models exist
ls ~/ZSC/ZSC-Eval/policy_pool/random0_m/
```

If no models, please refer to the main project's [Training Guide](../TRAINING_GUIDE.md) for training or downloading.

## Verify Installation

Run the following commands to verify successful installation:

```bash
# Test help message
overcooked-with-ai --help

# Test environment loading (without starting game)
overcooked-with-ai --env random0_m --algo bach --dry-run

# Run actual test
overcooked-with-ai --env random0_m --algo bach
```

## Uninstall

```bash
# Uninstall package
pip uninstall overcooked-with-ai

# Delete source code (optional)
cd ~/ZSC/ZSC-Eval
rm -rf human_test
```

## Troubleshooting

### Issue: command not found

**Solution:**

```bash
# Check pip installation location
which pip

# Ensure pip scripts path is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Or run directly with Python
python -m human_test --env random0_m --algo bach
```

### Issue: ImportError

**Solution:**

```bash
# Ensure you're in the correct directory
pwd  # Should show .../human_test

# Reinstall
pip install -e . --force-reinstall
```

### Issue: Game display not refreshing

**Solution:**

- Use terminal with ANSI escape sequence support
- Windows: Use Windows Terminal instead of CMD
- Linux: Use GNOME Terminal or Konsole
- macOS: Use iTerm2 instead of Terminal

## Getting Help

If you encounter installation issues:

1. Check [CLI.md](CLI.md) for usage instructions
2. Check the main project's [README.md](../README.md)
3. Submit an Issue to the project repository

---

**Supported Systems**: Windows 10+ | Ubuntu 20.04+ | macOS 10.15+