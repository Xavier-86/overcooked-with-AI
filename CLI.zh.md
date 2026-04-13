# overcooked-with-AI CLI 文档

[English](CLI.md) | [中文](CLI.zh.md)

overcooked-with-AI 的完整命令行参考文档。

---

## 命令格式

```bash
overcooked-with-ai [选项]
```

---

## 参数说明

### 必需参数

| 参数 | 短选项 | 说明 | 示例 |
|------|--------|------|------|
| `--env` | `-e` | 环境名称 | `random0_m`, `random3_m` |
| `--algo` | `-a` | AI 算法 | `bach`, `fcp`, `mep` |

### 可选参数

| 参数 | 短选项 | 说明 | 默认值 | 示例 |
|------|--------|------|--------|------|
| `--human-player` | `-p` | 人类玩家位置 (0 或 1) | 0 | `-p 1` |
| `--policy-path` | | 自定义策略路径 | 自动检测 | `--policy-path /path/to/policy` |
| `--episodes` | `-n` | 测试局数 | 1 | `-n 5` |
| `--render-mode` | `-r` | 渲染模式: `cli` 或 `ascii` | cli | `-r ascii` |
| `--seed` | `-s` | 随机种子 | None | `-s 42` |
| `--dry-run` | | 仅检查环境 | False | `--dry-run` |
| `--help` | `-h` | 显示帮助 | - | `-h` |
| `--version` | `-v` | 显示版本 | - | `-v` |

### 列表命令

| 选项 | 说明 |
|------|------|
| `--list-envs` | 列出所有可用环境 |
| `--list-algos` | 列出所有可用算法 |

---

## 使用示例

### 基础用法

```bash
# 使用 BACH 算法在 random0_m 地图测试
overcooked-with-ai --env random0_m --algo bach

# 简写形式
overcooked-with-ai -e random0_m -a bach
```

### 指定人类玩家位置

```bash
# 人类作为 Player 0 (默认)
overcooked-with-ai -e random0_m -a bach -p 0

# 人类作为 Player 1
overcooked-with-ai -e random0_m -a bach -p 1
```

### 多局测试

```bash
# 连续测试 5 局
overcooked-with-ai -e random0_m -a bach -n 5
```

### 不同渲染模式

```bash
# CLI 模式 (默认，Unicode 边框)
overcooked-with-ai -e random0_m -a bach -r cli

# ASCII 模式 (兼容性更好)
overcooked-with-ai -e random0_m -a bach -r ascii
```

### 环境检查

```bash
# 验证环境配置和模型加载，不启动游戏
overcooked-with-ai -e random0_m -a bach --dry-run
```

### 自定义策略

```bash
# 加载自定义训练的策略
overcooked-with-ai -e random0_m --policy-path /path/to/your/policy.yml
```

---

## 可用环境

查看所有环境：
```bash
overcooked-with-ai --list-envs
```

常用环境：

| 环境 | 说明 |
|------|------|
| `random0_m` | 基础厨房 (推荐新手) |
| `random3_m` | 三原料厨房 |
| `forced_coordination` | 强制协作 |
| `asymmetric_advantages` | 非对称优势 |

---

## 可用算法

查看所有算法：
```bash
overcooked-with-ai --list-algos
```

常用算法：

| 算法 | 类型 |
|------|------|
| `bach` | BACH (推荐，SOTA 性能) |
| `fcp` | Fictitious Co-Play |
| `mep` | Maximum Entropy Population |
| `trajedi` | Trajectory Diversity |
| `hsp` | Hidden Utility Self-Play |
| `sp` | Self-Play (基线) |

---

## 环境变量

通过环境变量配置工具行为：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `POLICY_POOL` | 策略根目录 | `/path/to/policies` |
| `HUMAN_TEST_LOG_LEVEL` | 日志级别 | `DEBUG`, `INFO`, `WARNING` |
| `HUMAN_TEST_NO_COLOR` | 禁用颜色输出 | `1` 或 `true` |

示例：

```bash
# 使用自定义策略目录
export POLICY_POOL=/home/user/my_policies
overcooked-with-ai -e random0_m -a bach

# 禁用颜色输出
export HUMAN_TEST_NO_COLOR=1
overcooked-with-ai -e random0_m -a bach
```

---

## 游戏内控制

游戏运行时的键盘控制：

| 按键 | 动作 |
|------|------|
| `W` 或 `↑` | 向上移动 |
| `S` 或 `↓` | 向下移动 |
| `A` 或 `←` | 向左移动 |
| `D` 或 `→` | 向右移动 |
| `空格` | 交互（拾取/放下/烹饪） |
| `P` | 暂停/继续 |
| `Q` 或 `ESC` | 退出游戏 |

---

## 输出说明

游戏界面显示以下信息：

```
╔════════════════════════════════════════════════════════════╗
║ 地图: random0_m    算法: bach-S2    你: Player 0           ║
╠════════════════════════════════════════════════════════════╣
║  [厨房地图可视化]                                          ║
╠════════════════════════════════════════════════════════════╣
║  得分: 120  |  时间: 45s  |  局数: 1/3                     ║
╚════════════════════════════════════════════════════════════╝
```

- **得分**: 当前游戏得分
- **时间**: 游戏进行时间
- **局数**: 当前是第几局（如果 `-n > 1`）

---

## 退出代码

| 代码 | 含义 |
|------|------|
| 0 | 正常退出 |
| 1 | 参数错误 |
| 2 | 环境加载失败 |
| 3 | 策略加载失败 |
| 4 | 运行时错误 |
| 130 | 用户中断 (Ctrl+C) |

---

## 脚本示例

### 批量测试脚本

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

### Python 集成示例

```python
from human_test.core import HumanTest

# 创建测试实例
test = HumanTest(
    env_name="random0_m",
    algo="bach",
    human_player=0,
    episodes=5
)

# 运行测试
test.run()

# 获取结果
results = test.get_results()
print(f"平均得分: {results['avg_score']}")
```

---

## 故障排除

### 键盘输入无响应

**解决方案：**
- 确保终端窗口有焦点
- 尝试使用管理员权限运行 (Windows)
- 检查 pynput 是否安装: `pip install pynput`

**macOS 特有解决方案：**
```bash
# 1. 确保终端有输入监控权限
# 系统设置 → 隐私与安全性 → 输入监控 → 添加终端

# 2. 如果仍然无响应，尝试重置权限
sudo tccutil reset All com.apple.Terminal

# 3. 重启终端后重试
```

### 游戏画面显示异常

**解决方案：**
```bash
# 使用 ASCII 模式
overcooked-with-ai -e random0_m -a bach -r ascii

# 禁用颜色
export HUMAN_TEST_NO_COLOR=1
overcooked-with-ai -e random0_m -a bach
```

### 策略加载失败

**解决方案：**
```bash
# 检查策略路径
overcooked-with-ai -e random0_m -a bach --dry-run

# 使用自定义路径
overcooked-with-ai -e random0_m --policy-path /absolute/path/to/policy.yml
```

---

## 获取帮助

```bash
# 显示帮助
overcooked-with-ai --help

# 检查版本
overcooked-with-ai --version
```

更多信息请查看 [README.md](README.md) 或 [INSTALL.md](INSTALL.md)。