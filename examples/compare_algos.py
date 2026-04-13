#!/usr/bin/env python3
"""
对比测试不同算法
比较人类与不同 AI 算法的协作效果
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from human_test.core import HumanTest
import matplotlib.pyplot as plt


def compare_algorithms(env_name="random0_m", episodes=3):
    """对比不同算法"""
    
    algorithms = ['bach', 'fcp', 'mep']
    results = {}
    
    for algo in algorithms:
        print(f"\n测试算法: {algo}")
        print("=" * 40)
        
        test = HumanTest(
            env_name=env_name,
            algo=algo,
            episodes=episodes
        )
        
        test.run()
        results[algo] = test.get_results()
    
    # 打印对比结果
    print("\n" + "=" * 40)
    print("对比结果")
    print("=" * 40)
    
    for algo, result in results.items():
        print(f"{algo:10s}: 平均得分 = {result['avg_score']:.2f}")
    
    return results


def plot_results(results):
    """绘制结果图表"""
    try:
        import matplotlib.pyplot as plt
        
        algos = list(results.keys())
        scores = [results[a]['avg_score'] for a in algos]
        
        plt.figure(figsize=(10, 6))
        plt.bar(algos, scores)
        plt.xlabel('Algorithm')
        plt.ylabel('Average Score')
        plt.title('Human-AI Collaboration Performance')
        plt.savefig('comparison_results.png')
        print("\n结果图表已保存到 comparison_results.png")
    except ImportError:
        print("\n提示: 安装 matplotlib 可以生成对比图表")
        print("pip install matplotlib")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='对比不同算法')
    parser.add_argument('--env', default='random0_m', help='环境名称')
    parser.add_argument('-n', '--episodes', type=int, default=3, help='每算法测试局数')
    
    args = parser.parse_args()
    
    results = compare_algorithms(args.env, args.episodes)
    plot_results(results)


if __name__ == '__main__':
    main()