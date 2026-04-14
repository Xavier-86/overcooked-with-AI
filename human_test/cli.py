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

from .pygame_core import PygameHumanTest


def main():
    """主入口函数 - Pygame版本"""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='overcooked-human-test',
        description='人机混合测试工具 - 使用Pygame渲染',
    )
    
    parser.add_argument('-e', '--env', type=str, default='random0_m',
                       help='游戏地图环境')
    parser.add_argument('-a', '--algo', type=str, default='bach',
                       help='AI算法')
    parser.add_argument('-p', '--human-player', type=int, default=0, choices=[0, 1],
                       help='人类玩家位置')
    parser.add_argument('-n', '--episodes', type=int, default=1,
                       help='测试局数')
    parser.add_argument('--tile-size', type=int, default=75,
                       help='图块大小')
    
    args = parser.parse_args()
    
    try:
        test = PygameHumanTest(
            env_name=args.env,
            algo=args.algo,
            human_player=args.human_player,
            episodes=args.episodes,
            tile_size=args.tile_size,
        )
        test.run()
    except KeyboardInterrupt:
        print("用户中断")
        import pygame
        pygame.quit()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        import pygame
        pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
