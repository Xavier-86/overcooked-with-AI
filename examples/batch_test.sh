#!/bin/bash
# 批量测试脚本
# 测试多个环境和算法组合

echo "=========================================="
echo "批量测试脚本"
echo "=========================================="

# 配置
ENVS=("random0_m" "random3_m")
ALGOS=("bach" "fcp" "mep")
EPISODES=3

# 测试计数
TOTAL_TESTS=$((${#ENVS[@]} * ${#ALGOS[@]}))
CURRENT=0

for env in "${ENVS[@]}"; do
    for algo in "${ALGOS[@]}"; do
        CURRENT=$((CURRENT + 1))
        echo ""
        echo "[$CURRENT/$TOTAL_TESTS] 测试: $algo on $env"
        echo "------------------------------------------"
        
        # 运行测试
        human-test -e "$env" -a "$algo" -n $EPISODES
        
        if [ $? -eq 0 ]; then
            echo "✓ 测试成功"
        else
            echo "✗ 测试失败"
        fi
        
        # 等待一下
        sleep 1
    done
done

echo ""
echo "=========================================="
echo "批量测试完成"
echo "=========================================="