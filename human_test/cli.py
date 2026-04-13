#!/usr/bin/env python3
"""
Human-Test CLI 入口
"""

import argparse
import sys
import os

# 添加父目录到路径以导入 zsceval
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from .core import HumanTest
from .utils import get_available_envs, get_available_algos


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog='human-test',
        description='人机混合测试工具 - 在 Overcooked 环境中与 AI 智能体协作',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  human-test --env random0_m --algo bach
  human-test -e random0_m -a fcp -p 1
  human-test --list-envs
        '''
    )
    
    # 主要参数
    parser.add_argument(
        '-e', '--env',
        type=str,
        help='游戏地图环境 (如: random0_m, random3_m)'
    )
    
    parser.add_argument(
        '-a', '--algo',
        type=str,
        help='AI 算法 (如: bach, fcp, mep)'
    )
    
    # 可选参数
    parser.add_argument(
        '-p', '--human-player',
        type=int,
        default=0,
        choices=[0, 1],
        help='人类玩家位置 (0 或 1, 默认: 0)'
    )
    
    parser.add_argument(
        '-n', '--episodes',
        type=int,
        default=1,
        help='测试局数 (默认: 1)'
    )
    
    parser.add_argument(
        '-r', '--render-mode',
        type=str,
        default='cli',
        choices=['cli', 'ascii'],
        help='渲染模式: cli (Unicode) 或 ascii (默认: cli)'
    )
    
    parser.add_argument(
        '--policy-path',
        type=str,
        help='自定义策略路径'
    )
    
    parser.add_argument(
        '-s', '--seed',
        type=int,
        help='随机种子'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅检查环境，不启动游戏'
    )
    
    # 列表参数
    parser.add_argument(
        '--list-envs',
        action='store_true',
        help='列出所有支持的地图环境'
    )
    
    parser.add_argument(
        '--list-algos',
        action='store_true',
        help='列出所有支持的 AI 算法'
    )
    
    # 其他
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    return parser


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 处理列表请求
    if args.list_envs:
        print("支持的地图环境:")
        for env in get_available_envs():
            print(f"  - {env}")
        return 0
    
    if args.list_algos:
        print("支持的 AI 算法:")
        for algo in get_available_algos():
            print(f"  - {algo}")
        return 0
    
    # 检查必需参数
    if not args.env or not args.algo:
        parser.print_help()
        print("\n错误: 必须指定 --env 和 --algo 参数")
        return 1
    
    # 创建测试实例
    try:
        test = HumanTest(
            env_name=args.env,
            algo=args.algo,
            human_player=args.human_player,
            episodes=args.episodes,
            render_mode=args.render_mode,
            policy_path=args.policy_path,
            seed=args.seed,
            dry_run=args.dry_run
        )
        
        if args.dry_run:
            print("✓ 环境检查通过")
            return 0
        
        # 运行测试
        test.run()
        return 0
        
    except KeyboardInterrupt:
        print("\n用户中断")
        return 130
    except Exception as e:
        print(f"错误: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
