#!/usr/bin/env python3
"""
使用自定义策略进行测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from human_test.core import HumanTest


def test_custom_policy(policy_path, env_name="random0_m"):
    """测试自定义策略"""
    
    print(f"加载自定义策略: {policy_path}")
    
    test = HumanTest(
        env_name=env_name,
        algo="custom",
        policy_path=policy_path,
        episodes=3
    )
    
    test.run()
    
    results = test.get_results()
    print(f"\n测试完成!")
    print(f"平均得分: {results['avg_score']:.2f}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='测试自定义策略')
    parser.add_argument('--policy', required=True, help='策略文件路径')
    parser.add_argument('--env', default='random0_m', help='环境名称')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.policy):
        print(f"错误: 策略文件不存在: {args.policy}")
        sys.exit(1)
    
    test_custom_policy(args.policy, args.env)


if __name__ == '__main__':
    main()