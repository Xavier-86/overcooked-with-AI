#!/usr/bin/env python3
"""
overcooked-with-AI 核心逻辑
支持独立演示模式和完整 ZSC-Eval 集成
"""

import sys
import os
import time
import numpy as np
from typing import Optional, Dict, Any, List

# 添加父目录到路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# 导入 ZSCEval 组件（可选）
try:
    from zsceval.human_exp.agent_pool import ZSCEvalAgentPool
    from zsceval.envs.overcooked.overcooked_ai_py.mdp.overcooked_mdp import OvercookedGridworld
    ZSCEVAL_AVAILABLE = True
except ImportError:
    ZSCEVAL_AVAILABLE = False

from .renderer import CLIRenderer, ASCIIRenderer
from .keyboard import KeyboardHandler


class DummyMDP:
    """演示模式使用的简化 MDP"""
    
    def __init__(self, env_name: str = "random0_m"):
        self.env_name = env_name
        # 简化地图 7x5
        self.terrain_mtx = [
            ['#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', 'O', ' ', 'S', ' ', '#'],
            ['#', ' ', ' ', 'D', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#'],
        ]
        self.height = len(self.terrain_mtx)
        self.width = len(self.terrain_mtx[0])
    
    def get_standard_start_state(self):
        """返回初始状态"""
        return DummyState()
    
    def get_state_transition(self, state, actions):
        """模拟状态转移"""
        # 简化：随机返回奖励和结束标志
        reward = np.random.choice([0, 0, 0, 5, 10], p=[0.7, 0.1, 0.1, 0.05, 0.05])
        done = False
        info = {'episode_done': False}
        return DummyState(), reward, done, info
    
    def get_valid_player_positions(self):
        """获取有效位置"""
        positions = []
        for y, row in enumerate(self.terrain_mtx):
            for x, cell in enumerate(row):
                if cell != '#':
                    positions.append((x, y))
        return positions


class DummyState:
    """演示模式使用的简化状态"""
    
    def __init__(self):
        self.players = [DummyPlayer(0), DummyPlayer(1)]
    
    def to_dict(self):
        return {
            'players': [
                {'position': p.position, 'orientation': p.orientation, 'held_object': None}
                for p in self.players
            ],
            'objects': {}
        }


class DummyPlayer:
    """演示模式使用的简化玩家"""
    
    def __init__(self, idx: int):
        self.idx = idx
        # 玩家0在左上，玩家1在右下
        self.position = (1, 1) if idx == 0 else (5, 3)
        self.orientation = (0, -1)  # 朝北
        self._held_object = None
    
    def has_object(self):
        return self._held_object is not None
    
    def get_object(self):
        return self._held_object


class HumanTest:
    """人机测试主类"""
    
    # 动作映射: 键盘输入 -> 动作ID
    ACTION_MAP = {
        'up': 0,      #  North
        'down': 1,    #  South
        'left': 2,    #  West
        'right': 3,   #  East
        'interact': 4, # Interact
        'stay': 5,    # Stay
    }
    
    # 动作名称映射
    ACTION_NAMES = {
        0: '↑',
        1: '↓',
        2: '←',
        3: '→',
        4: 'Interact',
        5: 'Stay',
    }
    
    def __init__(
        self,
        env_name: str,
        algo: str,
        human_player: int = 0,
        episodes: int = 1,
        render_mode: str = 'cli',
        policy_path: Optional[str] = None,
        seed: Optional[int] = None,
        dry_run: bool = False
    ):
        """
        初始化人机测试
        
        Args:
            env_name: 环境名称 (如: random0_m)
            algo: 算法名称 (如: bach)
            human_player: 人类玩家位置 (0 或 1)
            episodes: 测试局数
            render_mode: 渲染模式 ('cli' 或 'ascii')
            policy_path: 自定义策略配置文件路径 (YAML)
            seed: 随机种子
            dry_run: 是否仅检查环境
        """
        self.env_name = env_name
        self.algo = algo
        self.human_player = human_player
        self.ai_player = 1 - human_player
        self.episodes = episodes
        self.render_mode = render_mode
        self.seed = seed
        self.dry_run = dry_run
        self.policy_path = policy_path
        
        # 结果记录
        self.results = {
            'scores': [],
            'durations': [],
            'soups_cooked': []
        }
        
        # 初始化渲染器
        if render_mode == 'ascii':
            self.renderer = ASCIIRenderer()
        else:
            self.renderer = CLIRenderer()
        
        # 初始化键盘处理器
        self.keyboard = KeyboardHandler()
        
        if not dry_run:
            self._setup_environment()
    
    def _setup_environment(self):
        """设置环境和策略"""
        self.demo_mode = False
        
        if not ZSCEVAL_AVAILABLE:
            print("\n⚠️  演示模式: 未检测到 ZSC-Eval 环境")
            print("    将使用模拟环境运行，AI 将采用随机策略")
            print("    如需完整功能，请安装 ZSC-Eval:\n")
            print("    git clone <ZSC-Eval-repo>")
            print("    cd ZSC-Eval")
            print("    pip install -e .\n")
            self.demo_mode = True
            self.mdp = DummyMDP(self.env_name)
            self.ai_agent = None
            return
        
        # 正常模式：尝试加载 ZSC-Eval
        try:
            # 加载策略池配置
            policy_pool_path = os.environ.get('POLICY_POOL', os.path.join(parent_dir, 'policy_pool'))
            
            # 确定YAML配置文件路径
            if self.policy_path:
                yaml_path = self.policy_path
            else:
                # 默认从 benchmark_configs 加载
                yaml_path = os.path.join(
                    parent_dir, 'zsceval', 'human_exp', 'configs', 'benchmark_configs',
                    f"{self.env_name}_benchmark.yml"
                )
                # 如果不存在，尝试其他路径
                if not os.path.exists(yaml_path):
                    yaml_path = os.path.join(
                        parent_dir, 'human_test', 'configs',
                        f"{self.env_name}_{self.algo}.yml"
                    )
            
            if not os.path.exists(yaml_path):
                print(f"⚠️  警告: 找不到策略配置文件: {yaml_path}")
                print(f"    将使用随机策略运行...")
                self.agent_pool = None
            else:
                print(f"正在加载策略池: {yaml_path}")
                self.agent_pool = ZSCEvalAgentPool(
                    yaml_path,
                    self.env_name,
                    deterministic=True,
                    epsilon=0.0  # 完全确定性，无探索
                )
                print(f"✓ 策略池加载成功")
                print(f"  可用算法: {list(self.agent_pool.policy_pool.keys())}")
        
        except Exception as e:
            print(f"⚠️  警告: 环境加载失败: {e}")
            print("    切换到演示模式...")
            self.demo_mode = True
            self.agent_pool = None
        
        # 创建 MDP 用于状态处理
        try:
            if not self.demo_mode:
                self.mdp = OvercookedGridworld.from_layout_name(self.env_name)
                print(f"✓ 地图加载成功: {self.env_name}")
        except Exception as e:
            print(f"⚠️  警告: 地图加载失败: {e}")
            print("    使用演示模式...")
            self.demo_mode = True
            self.mdp = DummyMDP(self.env_name)
        
        # 获取AI策略
        self.ai_agent = None
        if not self.demo_mode and self.agent_pool and self.algo in self.agent_pool.policy_pool:
            try:
                self.ai_agent = self.agent_pool.get_agent(self.algo)
                print(f"✓ AI 策略加载成功: {self.algo}")
            except Exception as e:
                print(f"⚠️  警告: AI 策略加载失败: {e}")
    
    def run(self):
        """运行测试"""
        print(f"\n{'='*60}")
        if self.demo_mode:
            print(f"  overcooked-with-AI: 演示模式")
        else:
            print(f"  overcooked-with-AI: 人机混合测试")
        print(f"{'='*60}")
        print(f"  地图: {self.env_name}")
        print(f"  AI算法: {self.algo}")
        print(f"  你是: Player {self.human_player} (人类)")
        print(f"  AI是: Player {self.ai_player} (AI)")
        if self.demo_mode:
            print(f"  模式: 🎮 演示 (AI 随机行动)")
        print(f"{'='*60}\n")
        
        print("控制说明:")
        print("  [WASD/方向键] 移动")
        print("  [空格] 交互 (拾取/放下/烹饪)")
        print("  [Q/ESC] 退出游戏")
        print()
        
        input("按 Enter 开始游戏...")
        
        for episode in range(self.episodes):
            self._run_episode(episode + 1)
        
        self._print_summary()
    
    def _run_episode(self, episode_num: int):
        """运行单局游戏"""
        print(f"\n--- 第 {episode_num}/{self.episodes} 局 ---")
        
        # 初始化游戏状态
        state = self.mdp.get_standard_start_state()
        
        # 开始监听键盘
        self.keyboard.start()
        
        try:
            step = 0
            max_steps = 1000  # 最大步数
            total_reward = 0
            soups_cooked = 0
            start_time = time.time()
            
            while step < max_steps:
                # 渲染当前状态
                self._render(state, step, total_reward, soups_cooked)
                
                # 获取人类动作
                human_action_name = self._get_human_action()
                
                if human_action_name == 'quit':
                    print("用户退出游戏")
                    break
                
                human_action = self.ACTION_MAP.get(human_action_name, 5)
                
                # 获取 AI 动作
                ai_action = self._get_ai_action(state)
                
                # 组合动作
                actions = [0, 0]
                actions[self.human_player] = human_action
                actions[self.ai_player] = ai_action
                
                # 执行动作
                try:
                    new_state, reward, done, info = self.mdp.get_state_transition(
                        state, tuple(actions)
                    )
                    
                    total_reward += reward
                    if reward > 0:
                        soups_cooked += 1
                    
                    state = new_state
                    step += 1
                    
                    # 检查游戏是否结束
                    if done or info.get('episode_done', False):
                        print(f"\n游戏结束! 得分: {total_reward}, 步数: {step}")
                        break
                    
                    # 控制游戏速度
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"执行动作出错: {e}")
                    break
            
            # 记录结果
            duration = time.time() - start_time
            self.results['scores'].append(total_reward)
            self.results['durations'].append(duration)
            self.results['soups_cooked'].append(soups_cooked)
            
        finally:
            self.keyboard.stop()
    
    def _get_human_action(self) -> str:
        """获取人类玩家的动作"""
        return self.keyboard.get_action()
    
    def _get_ai_action(self, state) -> int:
        """获取 AI 的动作"""
        if self.ai_agent is None:
            # 随机策略（演示模式）
            return np.random.randint(0, 6)
        
        try:
            # 使用策略获取动作
            action = self.ai_agent(state.to_dict(), self.ai_player)
            return int(action)
        except Exception as e:
            print(f"AI 推理出错: {e}")
            return np.random.randint(0, 6)
    
    def _render(self, state, step: int, score: int, soups: int):
        """渲染游戏画面"""
        try:
            # 转换为可视化网格
            if self.demo_mode:
                grid = self._get_dummy_grid()
            else:
                grid = self._state_to_grid(state)
            
            game_state = {
                'grid': grid,
                'score': score,
                'time': step,
                'soups': soups,
            }
            self.renderer.render(game_state)
        except Exception as e:
            pass  # 渲染失败不中断游戏
    
    def _state_to_grid(self, state) -> List[List[str]]:
        """将 OvercookedState 转换为可视化网格"""
        # 简化的网格表示
        grid = []
        
        # 获取地图尺寸
        if hasattr(self.mdp, 'terrain_mtx'):
            height = len(self.mdp.terrain_mtx)
            width = len(self.mdp.terrain_mtx[0])
            
            # 复制地形
            for y in range(height):
                row = []
                for x in range(width):
                    terrain = self.mdp.terrain_mtx[y][x]
                    row.append(terrain if terrain != ' ' else ' ')
                grid.append(row)
            
            # 添加玩家位置
            if hasattr(state, 'players'):
                for i, player in enumerate(state.players):
                    x, y = player.position
                    if 0 <= y < height and 0 <= x < width:
                        symbol = 'P' if i == self.human_player else 'A'
                        if player.has_object():
                            symbol = symbol.lower()
                        grid[y][x] = symbol
        else:
            grid = self._get_dummy_grid()
        
        return grid
    
    def _get_dummy_grid(self) -> List[List[str]]:
        """获取示例网格"""
        return [
            ['#', '#', '#', '#', '#', '#', '#'],
            ['#', 'P', ' ', ' ', ' ', 'A', '#'],
            ['#', ' ', 'O', ' ', 'S', ' ', '#'],
            ['#', ' ', ' ', 'D', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#', '#', '#'],
        ]
    
    def _print_summary(self):
        """打印测试总结"""
        print(f"\n{'='*60}")
        print("  测试完成!")
        print(f"{'='*60}")
        
        if self.results['scores']:
            avg_score = np.mean(self.results['scores'])
            avg_duration = np.mean(self.results['durations'])
            total_soups = sum(self.results['soups_cooked'])
            
            print(f"  总局数: {len(self.results['scores'])}")
            print(f"  平均得分: {avg_score:.2f}")
            print(f"  平均时长: {avg_duration:.1f}s")
            print(f"  总汤数: {total_soups}")
        
        if self.demo_mode:
            print(f"\n  💡 提示: 这是演示模式")
            print(f"     如需完整体验，请安装 ZSC-Eval 项目")
        
        print(f"{'='*60}\n")
    
    def get_results(self) -> Dict[str, Any]:
        """获取测试结果"""
        return {
            **self.results,
            'avg_score': np.mean(self.results['scores']) if self.results['scores'] else 0,
            'avg_duration': np.mean(self.results['durations']) if self.results['durations'] else 0,
            'total_soups': sum(self.results['soups_cooked']),
        }