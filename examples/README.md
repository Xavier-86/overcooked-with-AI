# 示例脚本目录

此目录包含使用 Human-Test 的示例脚本。

## 示例脚本

### 1. 批量测试 (`batch_test.sh`)

测试多个环境和算法组合。

```bash
chmod +x examples/batch_test.sh
./examples/batch_test.sh
```

### 2. 对比测试 (`compare_algos.py`)

比较不同算法的性能。

```bash
python examples/compare_algos.py
```

### 3. 自定义策略测试 (`custom_policy.py`)

加载自定义训练的策略进行测试。

```bash
python examples/custom_policy.py --policy /path/to/policy.pkl
```

## 创建自己的脚本

参考 `custom_policy.py` 创建你自己的测试脚本：

```python
from human_test.core import HumanTest

# 创建测试实例
test = HumanTest(
    env_name="random0_m",
    algo="bach",
    human_player=0,
    episodes=3
)

# 运行测试
test.run()

# 获取结果
results = test.get_results()
print(f"平均得分: {results['avg_score']}")
```

## 更多示例

更多示例请参考项目文档。