#!/usr/bin/env python3
"""
Human-Test: Standalone Human-AI collaboration testing tool with Pygame
独立版本，不依赖ZSC-Eval
"""

import sys
import os
import numpy as np
import pygame
from typing import Optional, Dict, Any, Tuple, List

# 动作定义
class Action:
    STAY = (0, 0)
    NORTH = (0, -1)
    SOUTH = (0, 1)
    WEST = (-1, 0)
    EAST = (1, 0)
    INTERACT = 'interact'
    
    ALL_ACTIONS = [NORTH, SOUTH, WEST, EAST, INTERACT, STAY]


class SimplePlayer:
    """简化版玩家"""
    def __init__(self, idx: int, position: Tuple[int, int]):
        self.idx = idx
        self.position = position
        self.orientation = (0, -1)  # 默认朝北
        self.held_object = None
    
    def has_object(self):
        return self.held_object is not None


class SimpleState:
    """简化版游戏状态"""
    def __init__(self, players: List[SimplePlayer], objects: Dict = None):
        self.players = players
        self.objects = objects or {}
        self.timestep = 0


class SimpleMDP:
    """简化版MDP环境"""
    
    # 地形类型
    EMPTY = ' '
    COUNTER = '#'
    ONION_DISPENSER = 'O'
    TOMATO_DISPENSER = 'T'
    POT = 'S'
    DISH_DISPENSER = 'D'
    SERVING_LOC = 'P'
    
    def __init__(self, env_name: str = "random0_m"):
        self.env_name = env_name
        self.terrain_mtx = self._load_layout(env_name)
        self.height = len(self.terrain_mtx)
        self.width = len(self.terrain_mtx[0])
        self.num_players = 2
        
    def _load_layout(self, env_name: str) -> List[List[str]]:
        """加载地图布局"""
        layouts = {
            "random0_m": [
                list('XXXXXXXXX'),
                list('X       X'),
                list('XO    SX X'),
                list('X   D   X'),
                list('XXXXXXXXX'),
            ],
            "random3_m": [
                list('XXXXXXXXXXX'),
                list('X         X'),
                list('XO  T   S X'),
                list('X   D     X'),
                list('XXXXXXXXXXX'),
            ],
            "cramped_room": [
                list('XXXXX'),
                list('X   X'),
                list('X O X'),
                list('XSPD X'),
                list('XXXXX'),
            ],
        }
        return layouts.get(env_name, layouts["random0_m"])
    
    def get_standard_start_state(self) -> SimpleState:
        """返回初始状态"""
        # 找到两个空位作为玩家起始位置
        players = []
        start_positions = [(1, 2), (7, 2)]  # 默认位置
        
        for i, pos in enumerate(start_positions[:2]):
            players.append(SimplePlayer(i, pos))
        
        return SimpleState(players)
    
    def get_state_transition(self, state: SimpleState, joint_action: Tuple):
        """执行动作，返回新状态"""
        # 复制玩家状态
        new_players = []
        for i, player in enumerate(state.players):
            new_player = SimplePlayer(i, player.position)
            new_player.orientation = player.orientation
            new_player.held_object = player.held_object
            new_players.append(new_player)
        
        new_state = SimpleState(new_players, state.objects.copy())
        new_state.timestep = state.timestep + 1
        
        # 执行每个玩家的动作
        for i, (player, action) in enumerate(zip(new_state.players, joint_action)):
            if action == Action.INTERACT:
                # 交互逻辑
                x, y = player.position
                terrain = self.terrain_mtx[y][x]
                if terrain == self.ONION_DISPENSER:
                    player.held_object = 'onion'
                elif terrain == self.DISH_DISPENSER:
                    player.held_object = 'dish'
                elif terrain == self.POT and player.held_object:
                    # 烹饪逻辑简化
                    pass
            elif action != Action.STAY:
                # 移动逻辑
                dx, dy = action
                new_x = player.position[0] + dx
                new_y = player.position[1] + dy
                
                # 检查边界和障碍物
                if (0 <= new_x < self.width and 
                    0 <= new_y < self.height and
                    self.terrain_mtx[new_y][new_x] != self.COUNTER):
                    player.position = (new_x, new_y)
                    player.orientation = action
        
        # 简化奖励计算
        reward = 0
        done = new_state.timestep >= 400
        info = {'episode_done': done}
        
        return new_state, reward, done, info


class StandaloneHumanTest:
    """独立版人机交互测试"""
    
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
    
    # 颜色定义
    COLORS = {
        'floor': (200, 200, 200),
        'counter': (139, 69, 19),
        'onions': (255, 165, 0),
        'tomatoes': (255, 99, 71),
        'pot': (128, 128, 128),
        'dishes': (255, 255, 255),
        'serve': (0, 255, 0),
        'player0': (0, 0, 255),
        'player1': (255, 0, 0),
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
        
        self.results = {'scores': [], 'durations': []}
        
        # 初始化Pygame
        pygame.init()
        pygame.display.set_caption(f"Overcooked - Human vs {algo.upper()}")
        
        # 创建环境
        self.mdp = SimpleMDP(env_name)
        
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
        print("  [空格/E] 交互")
        print("  [Q] 退出游戏")
        print()
        
        for episode in range(self.episodes):
            self._run_episode(episode + 1)
        
        self._print_summary()
    
    def _run_episode(self, episode_num: int):
        """运行单局游戏"""
        print(f"\n--- 第 {episode_num}/{self.episodes} 局 ---")
        
        state = self.mdp.get_standard_start_state()
        
        # 创建窗口
        width = self.mdp.width * self.tile_size
        height = self.mdp.height * self.tile_size + 50  # HUD空间
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
            
            # AI动作（随机）
            ai_action_idx = np.random.randint(0, len(Action.ALL_ACTIONS))
            ai_action = Action.ALL_ACTIONS[ai_action_idx]
            
            # 组合动作
            if self.human_player == 0:
                joint_action = (human_action, ai_action)
            else:
                joint_action = (ai_action, human_action)
            
            # 执行
            state, reward, done, info = self.mdp.get_state_transition(state, joint_action)
            total_reward += reward
            step += 1
            
            # 渲染
            self._render(screen, state, total_reward, step)
            clock.tick(self.fps)
            
            if done:
                print(f"\n游戏结束! 得分: {total_reward}, 步数: {step}")
                break
        
        duration = (pygame.time.get_ticks() - start_time) / 1000
        self.results['scores'].append(total_reward)
        self.results['durations'].append(duration)
    
    def _render(self, screen, state, score: int, step: int):
        """渲染游戏"""
        screen.fill((0, 0, 0))
        
        # 渲染地图
        for y, row in enumerate(self.mdp.terrain_mtx):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                
                if cell == 'X':
                    pygame.draw.rect(screen, self.COLORS['counter'], rect)
                elif cell == 'O':
                    pygame.draw.rect(screen, self.COLORS['onions'], rect)
                elif cell == 'T':
                    pygame.draw.rect(screen, self.COLORS['tomatoes'], rect)
                elif cell == 'S':
                    pygame.draw.rect(screen, self.COLORS['pot'], rect)
                elif cell == 'D':
                    pygame.draw.rect(screen, self.COLORS['dishes'], rect)
                else:
                    pygame.draw.rect(screen, self.COLORS['floor'], rect)
                
                # 画边框
                pygame.draw.rect(screen, (100, 100, 100), rect, 1)
        
        # 渲染玩家
        for i, player in enumerate(state.players):
            x, y = player.position
            center = (
                x * self.tile_size + self.tile_size // 2,
                y * self.tile_size + self.tile_size // 2
            )
            color = self.COLORS['player0'] if i == 0 else self.COLORS['player1']
            radius = self.tile_size // 3
            pygame.draw.circle(screen, color, center, radius)
            
            # 显示持有的物品
            if player.held_object:
                pygame.draw.circle(screen, (255, 255, 0), center, radius // 2)
        
        # HUD
        font = pygame.font.SysFont(None, 24)
        hud_text = f"Score: {score} | Step: {step}"
        text_surface = font.render(hud_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, self.mdp.height * self.tile_size + 10))
        
        pygame.display.flip()
    
    def _print_summary(self):
        """打印总结"""
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
        pygame.quit()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='overcooked-human-test',
        description='人机混合测试工具 - 独立版',
    )
    
    parser.add_argument('-e', '--env', type=str, default='random0_m',
                       help='游戏地图')
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
        test = StandaloneHumanTest(
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
