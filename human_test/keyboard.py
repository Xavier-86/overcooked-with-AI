#!/usr/bin/env python3
"""
键盘输入处理模块
支持跨平台的键盘监听 (Windows / Linux / macOS)
"""

import threading
import queue
import platform
from typing import Optional

try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("警告: pynput 未安装，键盘输入功能受限")
    print("请运行: pip install pynput")


class KeyboardHandler:
    """键盘处理器 - 支持 Windows, Linux, macOS"""
    
    def __init__(self):
        self.action_queue = queue.Queue()
        self.listener = None
        self.running = False
        self.current_action = 'stay'
        self.system = platform.system()  # 'Windows', 'Linux', 'Darwin' (macOS)
        
    def start(self):
        """开始监听键盘"""
        if not PYNPUT_AVAILABLE:
            print("警告: pynput 不可用，键盘输入功能受限")
            print("在 macOS 上，请确保已授予终端'输入监控'权限")
            return
        
        # macOS 权限提示
        if self.system == 'Darwin':
            print("提示: macOS 用户请确保已授予终端'输入监控'权限")
            print("      系统设置 → 隐私与安全性 → 输入监控")
        
        self.running = True
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release,
                suppress=False  # 不阻止其他应用接收键盘事件
            )
            self.listener.start()
        except Exception as e:
            print(f"键盘监听启动失败: {e}")
            if self.system == 'Darwin':
                print("macOS 解决方法:")
                print("1. 打开 系统设置 → 隐私与安全性 → 输入监控")
                print("2. 添加并启用你的终端应用")
                print("3. 重启终端后重试")
    
    def stop(self):
        """停止监听键盘"""
        self.running = False
        if self.listener:
            try:
                self.listener.stop()
            except Exception:
                pass  # 忽略停止时的错误
    
    def _on_press(self, key):
        """按键按下回调"""
        try:
            # 方向键处理
            if key == keyboard.Key.up:
                self.current_action = 'up'
            elif key == keyboard.Key.down:
                self.current_action = 'down'
            elif key == keyboard.Key.left:
                self.current_action = 'left'
            elif key == keyboard.Key.right:
                self.current_action = 'right'
            elif key == keyboard.Key.space:
                self.current_action = 'interact'
            elif key == keyboard.Key.esc:
                self.current_action = 'quit'
            # 字符键处理
            elif hasattr(key, 'char') and key.char:
                char = key.char.lower()
                if char == 'w':
                    self.current_action = 'up'
                elif char == 's':
                    self.current_action = 'down'
                elif char == 'a':
                    self.current_action = 'left'
                elif char == 'd':
                    self.current_action = 'right'
                elif char == 'q':
                    self.current_action = 'quit'
                elif char == 'p':
                    self.current_action = 'pause'
        except AttributeError:
            pass
        except Exception as e:
            # macOS 上可能出现的权限错误
            if self.system == 'Darwin' and 'permissions' in str(e).lower():
                print("权限错误: 请授予终端'输入监控'权限")
    
    def _on_release(self, key):
        """按键释放回调"""
        # 移动类按键释放时重置为 stay
        if key in (keyboard.Key.up, keyboard.Key.down, 
                   keyboard.Key.left, keyboard.Key.right):
            self.current_action = 'stay'
        # 检查字符键
        try:
            if hasattr(key, 'char') and key.char:
                char = key.char.lower()
                if char in ('w', 'a', 's', 'd'):
                    self.current_action = 'stay'
        except AttributeError:
            pass
    
    def get_action(self) -> str:
        """获取当前动作"""
        action = self.current_action
        # 对于非持续动作，重置为 stay
        if action not in ['pause', 'quit']:
            self.current_action = 'stay'
        return action
    
    def get_action_blocking(self, timeout: Optional[float] = None) -> str:
        """阻塞方式获取动作"""
        try:
            return self.action_queue.get(timeout=timeout)
        except queue.Empty:
            return 'stay'
    
    def is_available(self) -> bool:
        """检查键盘输入是否可用"""
        return PYNPUT_AVAILABLE and self.running
