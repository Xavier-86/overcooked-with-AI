#!/usr/bin/env python3
"""
工具函数模块
"""

import os
import sys
from typing import List, Optional

# 添加父目录到路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def get_available_envs() -> List[str]:
    """获取所有支持的环境/地图"""
    # 从 policy_pool 目录获取
    policy_root = os.path.join(parent_dir, 'policy_pool')
    if not os.path.exists(policy_root):
        return ['random0_m', 'random3_m']  # 默认值
    
    envs = []
    for item in os.listdir(policy_root):
        item_path = os.path.join(policy_root, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            envs.append(item)
    
    return sorted(envs) if envs else ['random0_m', 'random3_m']


def get_available_algos() -> List[str]:
    """获取所有支持的算法"""
    return [
        'bach',
        'fcp',
        'mep',
        'trajedi',
        'hsp',
        'cole',
        'e3t',
        'sp',
    ]


def get_policy_path(env_name: str, algo: str) -> str:
    """
    获取策略路径
    
    Args:
        env_name: 环境名称
        algo: 算法名称
    
    Returns:
        策略文件路径
    """
    policy_root = os.path.join(parent_dir, 'policy_pool')
    
    # 尝试不同的路径模式
    possible_paths = [
        os.path.join(policy_root, env_name, algo, 's2', 'policy.pt'),
        os.path.join(policy_root, env_name, algo, 'actor_checkpoint.pt'),
        os.path.join(policy_root, env_name, algo, 'policy_config.pkl'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 如果没有找到，返回第一个可能的路径（会报错）
    return possible_paths[0]


def load_policy_config(policy_path: str) -> Optional[dict]:
    """
    加载策略配置
    
    Args:
        policy_path: 策略文件路径
    
    Returns:
        配置字典或 None
    """
    try:
        import pickle
        with open(policy_path, 'rb') as f:
            config = pickle.load(f)
        return config
    except Exception as e:
        print(f"加载策略配置失败: {e}")
        return None


def get_project_root() -> str:
    """获取项目根目录"""
    return parent_dir


def check_environment() -> bool:
    """
    检查环境是否配置正确
    
    Returns:
        环境是否可用
    """
    checks = {
        'zsceval': False,
        'policy_pool': False,
        'pynput': False,
    }
    
    # 检查 zsceval
    try:
        import zsceval
        checks['zsceval'] = True
    except ImportError:
        pass
    
    # 检查 policy_pool
    policy_root = os.path.join(parent_dir, 'policy_pool')
    if os.path.exists(policy_root):
        checks['policy_pool'] = True
    
    # 检查 pynput
    try:
        import pynput
        checks['pynput'] = True
    except ImportError:
        pass
    
    # 打印检查结果
    print("环境检查:")
    for name, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"  {symbol} {name}")
    
    # 独立模式下，只要有 pynput 就可以运行（演示模式）
    if not checks['zsceval']:
        print("\n  ℹ️  提示: 未检测到 ZSC-Eval")
        print("      工具将以演示模式运行")
        print("      如需完整功能，请安装 ZSC-Eval\n")
    
    return checks['pynput']


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗              ║
║   ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║              ║
║   ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║              ║
║   ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║              ║
║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║              ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝              ║
║                                                               ║
║              ████████╗███████╗███████╗████████╗               ║
║              ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝               ║
║                 ██║   █████╗  ███████╗   ██║                  ║
║                 ██║   ██╔══╝  ╚════██║   ██║                  ║
║                 ██║   ███████╗███████║   ██║                  ║
║                 ╚═╝   ╚══════╝╚══════╝   ╚═╝                  ║
║                                                               ║
║         Human vs AI Testing Tool for Overcooked               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)
