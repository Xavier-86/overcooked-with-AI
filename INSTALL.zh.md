# 安装指南

[English](INSTALL.md) | [中文](INSTALL.zh.md)

Windows、Ubuntu 和 macOS 的完整安装说明。

---

## 系统要求

- **操作系统**: Windows 10+ / Ubuntu 20.04+ / macOS 10.15+
- **Python**: 3.9 或更高版本
- **终端**: 支持 Unicode 和颜色的终端
  - Windows: Windows Terminal, PowerShell, CMD
  - Ubuntu: GNOME Terminal, Konsole, xterm
  - macOS: Terminal, iTerm2

## 快速安装

### 步骤 1: 进入项目目录

```bash
cd ~/ZSC/ZSC-Eval/human_test
```

### 步骤 2: 安装依赖

```bash
# 使用 pip 安装
pip install -e .

# 或者使用 conda
conda install -c conda-forge pynput
pip install -e .
```

### 步骤 3: 验证安装

```bash
overcooked-with-ai --help
```

## macOS 安装

### 方法 1: 直接安装 (推荐)

```bash
# 进入项目目录
cd ~/ZSC/ZSC-Eval/human_test

# 安装依赖
pip install -e .

# 验证安装
overcooked-with-ai --help
```

### 方法 2: 使用 Homebrew

```bash
# 确保已安装 Homebrew，然后安装 Python
brew install python@3.9

# 进入项目目录
cd ~/ZSC/ZSC-Eval/human_test

# 安装
pip3 install -e .

# 运行测试
overcooked-with-ai --env random0_m --algo bach
```

### 方法 3: 使用 conda

```bash
# 创建 conda 环境
conda create -n human_test python=3.9
conda activate human_test

# 安装
pip install -e .

# 运行
overcooked-with-ai --env random0_m --algo bach
```

### macOS 权限设置 (重要!)

**终端权限**: 首次运行时需要授予终端输入监控权限

1. 打开 **系统设置** → **隐私与安全性** → **输入监控**
2. 点击 **+** 添加你的终端应用 (Terminal 或 iTerm)
3. 勾选终端应用旁边的复选框
4. **重启终端**

或者通过命令行:
```bash
# 添加 Terminal 到输入监控 (需要管理员密码)
sudo tccutil reset All com.apple.Terminal

# 对于 iTerm2
sudo tccutil reset All com.googlecode.iterm2
```

**辅助功能权限** (如果使用 pynput 遇到问题):
1. 打开 **系统设置** → **隐私与安全性** → **辅助功能**
2. 添加终端应用并启用

### macOS 常见问题

**问题 1: 键盘输入无响应**

**解决方案:**
```bash
# 1. 确保终端有输入监控权限 (见上文)

# 2. 尝试在安全模式下运行
# 重启 Mac 并按住 Shift 键进入安全模式测试

# 3. 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**问题 2: pynput 安装失败**

**解决方案:**
```bash
# 安装 Xcode 命令行工具
xcode-select --install

# 然后重新安装 pynput
pip install --upgrade --force-reinstall pynput
```

**问题 3: 显示编码问题**

**解决方案:**
```bash
# 设置 UTF-8 编码
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 使用 ASCII 模式
overcooked-with-ai -e random0_m -a bach -r ascii
```

**问题 4: 游戏画面刷新闪烁**

**解决方案:**
```bash
# 使用 iTerm2 替代 Terminal
# 或者调整渲染速度
export HUMAN_TEST_RENDER_DELAY=0.2
```

## 详细安装说明

### Windows 安装

#### 方法 1: 使用 pip (推荐)

```powershell
# 打开 PowerShell 或 CMD
cd C:\path\to\ZSC-Eval\human_test

# 安装
pip install -e .

# 验证
overcooked-with-ai --help
```

#### 方法 2: 使用虚拟环境

```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装
pip install -e .

# 运行
overcooked-with-ai --env random0_m --algo bach
```

#### Windows 常见问题

**问题 1: `pynput` 安装失败**

```powershell
# 安装 Visual C++ 构建工具
# 下载地址: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 或者使用预编译版本
pip install pynput --only-binary :all:
```

**问题 2: 终端显示乱码**

```powershell
# 在 PowerShell 中设置编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 或者使用 Windows Terminal (推荐)
```

### Ubuntu 安装

#### 方法 1: 直接安装

```bash
cd ~/ZSC/ZSC-Eval/human_test

# 安装系统依赖
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip

# 安装 Python 包
pip3 install -e .

# 验证
overcooked-with-ai --help
```

#### 方法 2: 使用 conda 环境

```bash
# 创建 conda 环境
conda create -n human_test python=3.9
conda activate human_test

# 安装
pip install -e .

# 运行
overcooked-with-ai --env random0_m --algo bach
```

#### Ubuntu 常见问题

**问题 1: 权限错误**

```bash
# 使用 --user 安装
pip install --user -e .

# 或者使用 sudo
sudo pip install -e .
```

**问题 2: 键盘输入无响应**

```bash
# 确保有权限访问输入设备
sudo usermod -a -G input $USER

# 重新登录后生效
```

## 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| `pynput` | >=1.7.0 | 键盘监听 |
| `numpy` | >=1.20.0 | 数值计算 |
| `colorama` | >=0.4.0 | Windows 终端颜色支持 |
| `zsceval` | - | 核心评估框架 |

## 预训练模型

安装完成后，确保预训练模型已下载：

```bash
# 模型应该位于
~/ZSC/ZSC-Eval/policy_pool/

# 检查模型是否存在
ls ~/ZSC/ZSC-Eval/policy_pool/random0_m/
```

如果没有模型，请参考主项目的 [Training Guide](../TRAINING_GUIDE.md) 训练或下载。

## 验证安装

运行以下命令验证安装是否成功：

```bash
# 测试帮助信息
overcooked-with-ai --help

# 测试环境加载 (不启动游戏)
overcooked-with-ai --env random0_m --algo bach --dry-run

# 运行实际测试
overcooked-with-ai --env random0_m --algo bach
```

## 卸载

```bash
# 卸载包
pip uninstall overcooked-with-ai

# 删除源代码 (可选)
cd ~/ZSC/ZSC-Eval
rm -rf human_test
```

## 故障排除

### 问题: 命令未找到 (command not found)

**解决方案:**

```bash
# 检查 pip 安装位置
which pip

# 确保 pip 安装的脚本路径在 PATH 中
export PATH="$HOME/.local/bin:$PATH"

# 或者使用 Python 直接运行
python -m human_test --env random0_m --algo bach
```

### 问题: 导入错误 (ImportError)

**解决方案:**

```bash
# 确保在正确的目录
pwd  # 应该显示 .../human_test

# 重新安装
pip install -e . --force-reinstall
```

### 问题: 游戏画面不刷新

**解决方案:**

- 使用支持 ANSI 转义序列的终端
- Windows: 使用 Windows Terminal 而不是 CMD
- Linux: 使用 GNOME Terminal 或 Konsole
- macOS: 使用 iTerm2 而不是 Terminal

## 获取帮助

如果安装遇到问题：

1. 查看 [CLI.md](CLI.md) 了解使用方法
2. 查看主项目的 [README.md](../README.md)
3. 提交 Issue 到项目仓库

---

**支持的系统**: Windows 10+ | Ubuntu 20.04+ | macOS 10.15+