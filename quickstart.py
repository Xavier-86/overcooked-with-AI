#!/usr/bin/env python3
"""
快速开始脚本
一键测试 overcooked-with-ai 工具
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from human_test.utils import print_banner, check_environment


def main():
    """快速开始"""
    print_banner()
    
    print("欢迎使用 Human-Test 人机测试工具!\n")
    
    # 检查环境
    print("检查环境...")
    if not check_environment():
        print("\n⚠ 环境检查未完全通过，但可以继续尝试运行。")
        print("建议查看 INSTALL.md 解决环境问题。\n")
    
    print("\n快速开始命令:")
    print("-" * 50)
    print("1. 基础测试:")
    print("   overcooked-with-ai --env random0_m --algo bach")
    print()
    print("2. 指定人类位置 (Player 1):")
    print("   overcooked-with-ai -e random0_m -a bach -p 1")
    print()
    print("3. 测试多局:")
    print("   overcooked-with-ai -e random0_m -a bach -n 5")
    print()
    print("4. 列出支持的地图:")
    print("   overcooked-with-ai --list-envs")
    print()
    print("5. 列出支持的算法:")
    print("   overcooked-with-ai --list-algos")
    print("-" * 50)
    
    print("\n控制说明:")
    print("  [WASD/方向键] 移动")
    print("  [空格] 交互 (拾取/放下/烹饪)")
    print("  [Q/ESC] 退出游戏")
    
    print("\n更多信息请查看:")
    print("  - README.md  (快速开始)")
    print("  - INSTALL.md (安装指南)")
    print("  - CLI.md     (命令行文档)")
    
    # 询问是否开始测试
    print("\n" + "=" * 50)
    response = input("是否立即开始测试? (y/n): ").strip().lower()
    
    if response in ['y', 'yes', '是']:
        print("\n启动测试...")
        from human_test.core import HumanTest
        
        try:
            test = HumanTest(
                env_name="random0_m",
                algo="bach",
                episodes=1
            )
            test.run()
        except Exception as e:
            print(f"\n错误: {e}")
            print("\n可能的解决方案:")
            print("1. 确保在 ZSC-Eval 项目目录下运行")
            print("2. 检查是否安装了所有依赖: pip install -e .")
            print("3. 查看 INSTALL.md 获取详细安装说明")
            return 1
    else:
        print("\n已取消。随时可以运行 'overcooked-with-ai' 命令开始测试。")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())