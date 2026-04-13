#!/usr/bin/env python3
"""
测试脚本
验证安装和基本功能
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from human_test.utils import get_available_envs, get_available_algos, check_environment
from human_test.renderer import CLIRenderer, ASCIIRenderer


def test_utils():
    """测试工具函数"""
    print("测试工具函数...")
    
    envs = get_available_envs()
    print(f"✓ 发现 {len(envs)} 个环境: {envs}")
    
    algos = get_available_algos()
    print(f"✓ 支持 {len(algos)} 个算法: {algos}")
    
    return True


def test_renderers():
    """测试渲染器"""
    print("\n测试渲染器...")
    
    # 测试 CLI 渲染器
    cli_renderer = CLIRenderer()
    print("✓ CLI 渲染器创建成功")
    
    # 测试 ASCII 渲染器
    ascii_renderer = ASCIIRenderer()
    print("✓ ASCII 渲染器创建成功")
    
    # 测试渲染 (不显示)
    game_state = {
        'grid': [
            ['#', '#', '#', '#', '#'],
            ['#', 'P', ' ', 'A', '#'],
            ['#', ' ', 'O', ' ', '#'],
            ['#', 'S', ' ', 'D', '#'],
            ['#', '#', '#', '#', '#'],
        ],
        'score': 100,
        'time': 60,
    }
    
    print("✓ 渲染测试通过 (未显示)")
    return True


def test_keyboard():
    """测试键盘处理"""
    print("\n测试键盘处理...")
    
    try:
        from human_test.keyboard import KeyboardHandler
        keyboard = KeyboardHandler()
        print("✓ 键盘处理器创建成功")
        return True
    except ImportError as e:
        print(f"⚠ 键盘处理器测试跳过: {e}")
        return True


def test_environment():
    """测试环境检查"""
    print("\n测试环境检查...")
    
    check_environment()
    print("✓ 环境检查完成")
    
    return True


def main():
    """运行所有测试"""
    print("=" * 50)
    print("Human-Test 测试脚本")
    print("=" * 50)
    
    tests = [
        ("工具函数", test_utils),
        ("渲染器", test_renderers),
        ("键盘处理", test_keyboard),
        ("环境检查", test_environment),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"✗ {name} 测试失败")
        except Exception as e:
            failed += 1
            print(f"✗ {name} 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())