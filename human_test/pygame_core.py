#!/usr/bin/env python3
"""
Human-Test: Human-AI collaboration testing tool with Pygame rendering
使用原版 Overcooked AI 渲染
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import pygame
from typing import Optional, Dict, Any, Tuple

from zsceval.envs.overcooked.overcooked_ai_py.mdp.overcooked_env import OvercookedEnv
from zsceval.envs.overcooked.overcooked_ai_py.mdp.overcooked_mdp import OvercookedGridworld
from zsceval.envs.overcooked.overcooked_ai_py.visualization.state_visualizer import StateVisualizer
from zsceval.envs.overcooked.overcooked_ai_py.mdp.actions import Action


class PygameHumanTest:
    """人机交互测试主类 - 使用 Pygame 渲染"""
    
    # 动作映射 (键盘 -> Action)
    ACTION_MAP = {
        pygame.K_w: Action.NORTH,
        pygame.K_UP: Action.NORTH,
        pygame.K_s: Action.SOUTH,
        pygame.K_DOWN: Action.SOUTH,
        pygame.K_a: Action.WEST,
        pygame.K_LEFT: Action.WEST,
        pygame.K_d: Action.EAST,
        pygame.K_RIGHT: Action.EAST,
        pygame.K_SPACE: Action.INTERACT,
        pygame.K_e: Action.INTERACT,
    }
    
    def __init__(
        self,
        env_name: str,
        algo: str,
        human_player: int = 0,
        episodes: int = 1,
        tile_size: int = 75,
        fps: int = 30,
    ):
        self.env_name = env_name
        self.algo = algo
        self.human_player = human_player
        self.ai_player = 1 - human_player
        self.episodes = episodes
        self.tile_size = tile_size
        self.fps = fps
        
        # 结果记录
        self.results = {
            'scores': [],
            'durations': [],
            'soups_cooked': []
        }
        
        # 初始化 pygame
        pygame.init()
        pygame.display.set_caption(f"Overcooked - Human vs {algo.upper()}")
        
        # 创建环境
        self._setup_environment()
        
        # 创建渲染器
        self.visualizer = StateVisualizer(
            tile_size=tile_size,
            window_fps=fps,
        )
    
    def _setup_environment(self):
        """设置环境"""
        print(f"\n🎮 初始化游戏环境: {self.env_name}")
        
        # 从 layouts 目录加载地图
        layout_path = os.path.join(
            os.path.dirname(__file__), '..', '..',
            'zsceval', 'envs', 'overcooked', 'overcooked_ai_py', 'mdp', 'layouts',
            f'{self.env_name}.layout'
        )
        
        if not os.path.exists(layout_path):
            # 尝试其他路径
            layout_path = f"zsceval/envs/overcooked/overcooked_ai_py/mdp/layouts/{self.env_name}.layout"
        
        if os.path.exists(layout_path):
            mdp = OvercookedGridworld.from_layout_name(self.env_name)
        else:
            # 创建默认地图
            print(f"地图 {self.env_name} 未找到，使用默认地图")
            mdp = OvercookedGridworld.from_layout_name("cramped_room")
        
        self.env = OvercookedEnv(mdp, horizon=400)
        print(f"✓ 环境加载成功")
    
    def run(self):
        """运行测试"""
        print(f"\n{'='*60}")
        print(f"  Overcooked: Human vs AI")
        print(f"{'='*60}")
        print(f"  地图: {self.env_name}")
        print(f"  AI算法: {self.algo}")
        print(f"  你是: Player {self.human_player} (人类)")
        print(f"  AI是: Player {self.ai_player} (AI)")
        print(f"{'='*60}\n")
        
        print("控制说明:")
        print("  [WASD/方向键] 移动")
        print("  [空格/E] 交互 (拾取/放下/烹饪)")
        print("  [Q] 退出游戏")
        print()
        
        for episode in range(self.episodes):
            self._run_episode(episode + 1)
        
        self._print_summary()
    
    def _run_episode(self, episode_num: int):
        """运行单局游戏"""
        print(f"\n--- 第 {episode_num}/{self.episodes} 局 ---")
        
        # 重置环境
        self.env.reset()
        state = self.env.state
        
        # 创建显示窗口
        grid = self.env.mdp.terrain_mtx
        width = len(grid[0]) * self.tile_size
        height = len(grid) * self.tile_size + 100  # HUD空间
        
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        
        running = True
        step = 0
        max_steps = 400
        total_reward = 0
        start_time = pygame.time.get_ticks()
        
        while running and step < max_steps:
            # 处理事件
            human_action = Action.STAY
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        break
                    elif event.key in self.ACTION_MAP:
                        human_action = self.ACTION_MAP[event.key]
            
            if not running:
                break
            
            # AI 动作（随机策略，后续可替换为加载的策略）
            ai_action = np.random.choice(Action.ALL_ACTIONS)
            
            # 组合动作
            if self.human_player == 0:
                joint_action = (human_action, ai_action)
            else:
                joint_action = (ai_action, human_action)
            
            # 执行动作
            next_state, reward, done, info = self.env.step(joint_action)
            total_reward += reward
            state = next_state
            step += 1
            
            # 渲染
            self._render(screen, state, total_reward, step)
            
            # 控制帧率
            clock.tick(self.fps)
            
            if done:
                print(f"\n游戏结束! 得分: {total_reward}, 步数: {step}")
                break
        
        # 记录结果
        duration = (pygame.time.get_ticks() - start_time) / 1000
        self.results['scores'].append(total_reward)
        self.results['durations'].append(duration)
    
    def _render(self, screen, state, score: int, step: int):
        """渲染游戏画面"""
        # 使用原版 visualizer 渲染
        grid = self.env.mdp.terrain_mtx
        
        # HUD 数据
        hud_data = {
            'score': score,
            'time_left': max(0, 400 - step),
            'step': step,
        }
        
        # 渲染状态到 surface
        surface = self.visualizer.render_state(
            state=state,
            grid=grid,
            hud_data=hud_data,
        )
        
        # 显示到屏幕
        screen.blit(surface, (0, 0))
        pygame.display.flip()
    
    def _print_summary(self):
        """打印测试总结"""
        print(f"\n{'='*60}")
        print("  测试完成!")
        print(f"{'='*60}")
        
        if self.results['scores']:
            avg_score = np.mean(self.results['scores'])
            avg_duration = np.mean(self.results['durations'])
            
            print(f"  总局数: {len(self.results['scores'])}")
            print(f"  平均得分: {avg_score:.2f}")
            print(f"  平均时长: {avg_duration:.1f}s")
        
        print(f"{'='*60}\n")
        
        # 退出 pygame
        pygame.quit()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='overcooked-human-test',
        description='人机混合测试工具 - 使用 Pygame 渲染',
    )
    
    parser.add_argument('-e', '--env', type=str, default='random0_m',
                       help='游戏地图环境 (如: random0_m, random3_m)')
    parser.add_argument('-a', '--algo', type=str, default='bach',
                       help='AI 算法 (如: bach, fcp, mep)')
    parser.add_argument('-p', '--human-player', type=int, default=0, choices=[0, 1],
                       help='人类玩家位置 (0 或 1, 默认: 0)')
    parser.add_argument('-n', '--episodes', type=int, default=1,
                       help='测试局数 (默认: 1)')
    parser.add_argument('--tile-size', type=int, default=75,
                       help='图块大小 (默认: 75)')
    
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
        print("\n用户中断")
        pygame.quit()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()


if __name__ == '__main__':
    main()
