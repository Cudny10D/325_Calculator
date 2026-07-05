# 最后编辑于2026/03/21 Ver2.0.7
# Windows 11 风格设计 + 完美深浅色主题

import tkinter as tk
from tkinter import messagebox, ttk
import time
import sys
import os

# 尝试导入系统主题检测库
try:
    import darkdetect
    HAS_DARKDETECT = True
except ImportError:
    HAS_DARKDETECT = False
    print("提示: 安装 darkdetect 可获得更好的系统主题检测 (pip install darkdetect)")

class Win11Theme:
    """Windows 11 风格主题"""
    
    # Windows 11 深色主题配色
    DARK_THEME = {
        # 背景色
        'bg_window': '#202020',      # 窗口背景
        'bg_card': '#2c2c2c',        # 卡片背景
        'bg_hover': '#3c3c3c',       # 悬停背景
        'bg_selected': '#4c4c4c',    # 选中背景
        
        # 文字颜色
        'text_primary': '#ffffff',    # 主要文字
        'text_secondary': '#9e9e9e',  # 次要文字
        'text_disabled': '#6c6c6c',   # 禁用文字
        
        # 强调色
        'accent': '#0078d4',          # Win11 蓝色
        'accent_light': '#1a8cff',    # 亮蓝色
        'accent_dark': '#005a9e',     # 深蓝色
        
        # 状态色
        'success': '#13a10e',         # 绿色
        'warning': '#f9a825',         # 橙色
        'error': '#d13438',           # 红色
        'info': '#3b88c3',            # 信息蓝
        
        # 边框和分隔线
        'border': '#3c3c3c',          # 边框颜色
        'separator': '#3c3c3c',       # 分隔线
        
        # 输入框
        'entry_bg': '#2c2c2c',
        'entry_fg': '#ffffff',
        'entry_border': '#3c3c3c',
        'entry_focus_border': '#0078d4',
        
        # 按钮
        'button_bg': '#2c2c2c',
        'button_fg': '#ffffff',
        'button_hover': '#3c3c3c',
        'button_pressed': '#4c4c4c',
        
        # 滚动条
        'scrollbar_bg': '#2c2c2c',
        'scrollbar_thumb': '#6c6c6c',
        'scrollbar_thumb_hover': '#9e9e9e',
        
        # 圆角
        'corner_radius': 8
    }
    
    # Windows 11 浅色主题配色
    LIGHT_THEME = {
        # 背景色
        'bg_window': '#f3f3f3',      # 窗口背景
        'bg_card': '#ffffff',        # 卡片背景
        'bg_hover': '#e5e5e5',       # 悬停背景
        'bg_selected': '#d4d4d4',    # 选中背景
        
        # 文字颜色
        'text_primary': '#000000',    # 主要文字
        'text_secondary': '#6c6c6c',  # 次要文字
        'text_disabled': '#9e9e9e',   # 禁用文字
        
        # 强调色
        'accent': '#0078d4',          # Win11 蓝色
        'accent_light': '#1a8cff',    # 亮蓝色
        'accent_dark': '#005a9e',     # 深蓝色
        
        # 状态色
        'success': '#0f7b0a',         # 绿色
        'warning': '#e68a2e',         # 橙色
        'error': '#c42b1c',           # 红色
        'info': '#2b7e9e',            # 信息蓝
        
        # 边框和分隔线
        'border': '#e5e5e5',          # 边框颜色
        'separator': '#e5e5e5',       # 分隔线
        
        # 输入框
        'entry_bg': '#ffffff',
        'entry_fg': '#000000',
        'entry_border': '#e5e5e5',
        'entry_focus_border': '#0078d4',
        
        # 按钮
        'button_bg': '#ffffff',
        'button_fg': '#000000',
        'button_hover': '#f3f3f3',
        'button_pressed': '#e5e5e5',
        
        # 滚动条
        'scrollbar_bg': '#f3f3f3',
        'scrollbar_thumb': '#c1c1c1',
        'scrollbar_thumb_hover': '#a8a8a8',
        
        # 圆角
        'corner_radius': 8
    }
    
    @staticmethod
    def detect_system_theme():
        """检测系统主题"""
        if HAS_DARKDETECT:
            try:
                is_dark = darkdetect.isDark()
                if is_dark is not None:
                    return 'dark' if is_dark else 'light'
            except:
                pass
        
        # Windows 注册表检测
        if sys.platform == 'win32':
            try:
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                winreg.CloseKey(key)
                return 'light' if value == 1 else 'dark'
            except:
                pass
        
        # macOS 检测
        if sys.platform == 'darwin':
            try:
                import subprocess
                result = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                    capture_output=True, text=True
                )
                if result.stdout.strip() == 'Dark':
                    return 'dark'
                return 'light'
            except:
                pass
        
        return 'light'  # 默认浅色
    
    @staticmethod
    def get_theme(theme_name=None):
        """获取主题配色"""
        if theme_name is None:
            theme_name = Win11Theme.detect_system_theme()
        
        if theme_name == 'light':
            return Win11Theme.LIGHT_THEME.copy()
        else:
            return Win11Theme.DARK_THEME.copy()


class RoundedCanvas(tk.Canvas):
    """圆角矩形画布"""
    def __init__(self, parent, radius=8, **kwargs):
        super().__init__(parent, **kwargs)
        self.radius = radius
        self.configure(bg=kwargs.get('bg', '#ffffff'), highlightthickness=0)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=None, **kwargs):
        """创建圆角矩形"""
        if radius is None:
            radius = self.radius
        
        points = []
        # 左上角
        points.append(x1 + radius)
        points.append(y1)
        points.append(x2 - radius)
        points.append(y1)
        points.append(x2)
        points.append(y1)
        points.append(x2)
        points.append(y1 + radius)
        # 右上角
        points.append(x2)
        points.append(y2 - radius)
        points.append(x2)
        points.append(y2)
        points.append(x2 - radius)
        points.append(y2)
        # 右下角
        points.append(x1 + radius)
        points.append(y2)
        points.append(x1)
        points.append(y2)
        points.append(x1)
        points.append(y2 - radius)
        # 左下角
        points.append(x1)
        points.append(y1 + radius)
        points.append(x1)
        points.append(y1)
        points.append(x1 + radius)
        points.append(y1)
        
        return self.create_polygon(points, smooth=True, **kwargs)


class Win11Button(ttk.Button):
    """Windows 11 风格按钮"""
    def __init__(self, parent, text="", command=None, style="Win11", **kwargs):
        super().__init__(parent, text=text, command=command, style=style, **kwargs)


class ModernNumberTo325Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("数字转325计算公式 - Windows 11 风格")
        self.root.geometry("900x750")
        self.root.minsize(800, 650)
        
        # 检测系统主题
        self.current_theme = Win11Theme.detect_system_theme()
        self.colors = Win11Theme.get_theme(self.current_theme)
        
        # 配置根窗口
        self.root.configure(bg=self.colors['bg_window'])
        
        # 设置窗口圆角（Windows 11 效果）
        self.apply_window_corners()
        
        # 创建自定义样式
        self.setup_styles()
        
        # 创建主容器
        self.create_main_container()
        
        # 创建界面组件
        self.create_header()
        self.create_input_section()
        self.create_result_section()
        self.create_history_section()
        self.create_footer()
        
        # 变量初始化
        self.history = []
        self.animation_id = None
        
        # 设置键盘快捷键
        self.setup_shortcuts()
        
        # 初始焦点
        self.entry.focus()
        
        # 监听系统主题变化（Windows）
        if sys.platform == 'win32':
            self.start_theme_monitoring()
        
        # 添加淡入效果
        self.fade_in()
    
    def apply_window_corners(self):
        """应用窗口圆角（Windows 11）"""
        if sys.platform == 'win32':
            try:
                import ctypes
                from ctypes import wintypes
                
                HWND = ctypes.windll.user32.GetParent(self.root.winfo_id())
                DWMWA_WINDOW_CORNER_PREFERENCE = 33
                DWM_WINDOW_CORNER_PREFERENCE = {
                    'round': 2,
                    'small_round': 1,
                    'square': 0
                }
                
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    HWND,
                    DWMWA_WINDOW_CORNER_PREFERENCE,
                    ctypes.byref(ctypes.c_int(DWM_WINDOW_CORNER_PREFERENCE['round'])),
                    ctypes.sizeof(ctypes.c_int)
                )
            except:
                pass
    
    def setup_styles(self):
        """设置 Windows 11 样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 移除默认边框
        style.configure('TFrame', background=self.colors['bg_window'])
        style.configure('TLabelframe', background=self.colors['bg_window'])
        
        # Windows 11 按钮样式
        style.configure('Win11.TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['button_fg'],
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10),
                       padding=(15, 8))
        style.map('Win11.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('pressed', self.colors['button_pressed'])])
        
        # 强调色按钮
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_light']),
                           ('pressed', self.colors['accent_dark'])])
        
        # 输入框样式
        style.configure('Win11.TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['entry_fg'],
                       borderwidth=1,
                       relief='solid',
                       font=('Consolas', 11))
        
        # 标签框样式
        style.configure('Win11.TLabelframe',
                       background=self.colors['bg_window'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       relief='flat')
        style.configure('Win11.TLabelframe.Label',
                       background=self.colors['bg_window'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 11, 'bold'))
        
        # 滚动条样式
        style.configure('Win11.Vertical.TScrollbar',
                       background=self.colors['scrollbar_bg'],
                       troughcolor=self.colors['scrollbar_bg'],
                       arrowcolor=self.colors['text_secondary'],
                       borderwidth=0)
    
    def create_main_container(self):
        """创建主容器"""
        # 主滚动区域
        self.main_canvas = tk.Canvas(self.root, bg=self.colors['bg_window'], highlightthickness=0)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, 
                                  command=self.main_canvas.yview, 
                                  style='Win11.Vertical.TScrollbar')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 内部框架
        self.main_container = tk.Frame(self.main_canvas, bg=self.colors['bg_window'])
        self.main_canvas.create_window((0, 0), window=self.main_container, anchor=tk.NW, width=self.main_canvas.winfo_reqwidth())
        
        self.main_container.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        
        # 内容容器
        self.content_frame = tk.Frame(self.main_container, bg=self.colors['bg_window'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def create_header(self):
        """创建头部"""
        header_frame = tk.Frame(self.content_frame, bg=self.colors['bg_window'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 标题区域
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_window'])
        title_frame.pack(fill=tk.X)
        
        # 标题和图标
        title_label = tk.Label(title_frame, 
                              text="数字转325计算公式", 
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_window'])
        title_label.pack(side=tk.LEFT)
        
        # 主题切换按钮
        theme_btn = tk.Button(title_frame,
                             text="🌓 主题",
                             font=('Segoe UI', 9),
                             fg=self.colors['text_primary'],
                             bg=self.colors['button_bg'],
                             activebackground=self.colors['button_hover'],
                             activeforeground=self.colors['text_primary'],
                             relief='flat',
                             cursor='hand2',
                             padx=12,
                             pady=5,
                             command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)
        
        # 副标题
        subtitle = tk.Label(header_frame,
                           text="将任意整数转换为包含 3、2、5 的数学表达式",
                           font=('Segoe UI', 11),
                           fg=self.colors['text_secondary'],
                           bg=self.colors['bg_window'])
        subtitle.pack(pady=(8, 0))
        
        # 装饰线
        separator = tk.Frame(header_frame, height=1, bg=self.colors['separator'])
        separator.pack(fill=tk.X, pady=(15, 0))
    
    def create_input_section(self):
        """创建输入区域"""
        input_card = tk.Frame(self.content_frame, bg=self.colors['bg_card'], relief='flat')
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        # 卡片内边距
        card_content = tk.Frame(input_card, bg=self.colors['bg_card'])
        card_content.pack(fill=tk.X, padx=20, pady=15)
        
        # 标题行
        title_frame = tk.Frame(card_content, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(title_frame,
                text="📝 输入数字",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        tk.Label(title_frame,
                text="支持任意长度整数",
                font=('Segoe UI', 9),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_card']).pack(side=tk.RIGHT)
        
        # 输入框
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(card_content, 
                               textvariable=self.input_var,
                               style='Win11.TEntry',
                               font=('Consolas', 12))
        self.entry.pack(fill=tk.X, ipady=10, pady=(0, 12))
        self.entry.bind('<Return>', lambda e: self.calculate())
        
        # 按钮行
        button_frame = tk.Frame(card_content, bg=self.colors['bg_card'])
        button_frame.pack(fill=tk.X)
        
        buttons = [
            ("🔢 计算", self.calculate, 'Accent.TButton'),
            ("🗑️ 清除", self.clear_all, 'Win11.TButton'),
            ("📚 示例", self.show_examples, 'Win11.TButton'),
            ("❓ 关于", self.show_about, 'Win11.TButton')
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)
    
    def create_result_section(self):
        """创建结果区域"""
        result_card = tk.Frame(self.content_frame, bg=self.colors['bg_card'], relief='flat')
        result_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 卡片内边距
        card_content = tk.Frame(result_card, bg=self.colors['bg_card'])
        card_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 标题行
        title_frame = tk.Frame(card_content, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(title_frame,
                text="📊 计算结果",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        # 复制按钮
        copy_btn = tk.Button(title_frame,
                            text="📋 复制",
                            font=('Segoe UI', 9),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['bg_card'],
                            activebackground=self.colors['bg_hover'],
                            relief='flat',
                            cursor='hand2',
                            command=self.copy_result)
        copy_btn.pack(side=tk.RIGHT)
        
        # 结果文本框
        self.result_text = tk.Text(card_content,
                                  height=14,
                                  font=('Consolas', 10),
                                  bg=self.colors['entry_bg'],
                                  fg=self.colors['entry_fg'],
                                  selectbackground=self.colors['accent'],
                                  selectforeground='white',
                                  wrap=tk.WORD,
                                  relief='flat',
                                  borderwidth=1,
                                  highlightthickness=1,
                                  highlightcolor=self.colors['accent'],
                                  highlightbackground=self.colors['border'])
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置文本框标签
        self.result_text.tag_configure('title', font=('Segoe UI', 11, 'bold'), 
                                      foreground=self.colors['accent'])
        self.result_text.tag_configure('highlight', foreground=self.colors['accent'])
        self.result_text.tag_configure('info', foreground=self.colors['info'])
        self.result_text.tag_configure('success', foreground=self.colors['success'])
        self.result_text.tag_configure('warning', foreground=self.colors['warning'])
    
    def create_history_section(self):
        """创建历史记录区域"""
        history_card = tk.Frame(self.content_frame, bg=self.colors['bg_card'], relief='flat')
        history_card.pack(fill=tk.BOTH, expand=True)
        
        # 卡片内边距
        card_content = tk.Frame(history_card, bg=self.colors['bg_card'])
        card_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 标题行
        title_frame = tk.Frame(card_content, bg=self.colors['bg_card'])
        title_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(title_frame,
                text="📜 历史记录",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_card']).pack(side=tk.LEFT)
        
        # 清空按钮
        clear_btn = tk.Button(title_frame,
                             text="🗑️ 清空",
                             font=('Segoe UI', 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_card'],
                             activebackground=self.colors['bg_hover'],
                             relief='flat',
                             cursor='hand2',
                             command=self.clear_history)
        clear_btn.pack(side=tk.RIGHT)
        
        # 历史记录文本框
        self.history_text = tk.Text(card_content,
                                   height=6,
                                   font=('Consolas', 9),
                                   bg=self.colors['entry_bg'],
                                   fg=self.colors['text_secondary'],
                                   wrap=tk.WORD,
                                   relief='flat',
                                   borderwidth=1,
                                   highlightthickness=1,
                                   highlightcolor=self.colors['accent'],
                                   highlightbackground=self.colors['border'])
        self.history_text.pack(fill=tk.BOTH, expand=True)
    
    def create_footer(self):
        """创建底部状态栏"""
        footer_frame = tk.Frame(self.content_frame, bg=self.colors['bg_window'])
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        # 分隔线
        separator = tk.Frame(footer_frame, height=1, bg=self.colors['separator'])
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # 状态栏内容
        status_frame = tk.Frame(footer_frame, bg=self.colors['bg_window'])
        status_frame.pack(fill=tk.X)
        
        # 状态标签
        self.status_var = tk.StringVar()
        theme_name = "深色" if self.current_theme == 'dark' else "浅色"
        self.status_var.set(f"✨ {theme_name}主题 | 就绪 | 输入任意整数开始转换")
        status_label = tk.Label(status_frame,
                               textvariable=self.status_var,
                               font=('Segoe UI', 9),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_window'])
        status_label.pack(side=tk.LEFT)
        
        # 时间显示
        self.time_var = tk.StringVar()
        self.update_time()
        time_label = tk.Label(status_frame,
                             textvariable=self.time_var,
                             font=('Segoe UI', 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_window'])
        time_label.pack(side=tk.RIGHT)
    
    def setup_shortcuts(self):
        """设置键盘快捷键"""
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-h>', lambda e: self.clear_history())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<Escape>', lambda e: self.clear_all())
    
    def update_time(self):
        """更新时间显示"""
        current_time = time.strftime("%H:%M:%S")
        self.time_var.set(f"🕐 {current_time}")
        self.root.after(1000, self.update_time)
    
    def fade_in(self):
        """淡入效果"""
        self.root.attributes('-alpha', 0)
        def fade():
            alpha = self.root.attributes('-alpha')
            if alpha < 1:
                alpha += 0.05
                self.root.attributes('-alpha', alpha)
                self.root.after(20, fade)
        fade()
    
    def update_theme(self):
        """更新主题"""
        self.colors = Win11Theme.get_theme(self.current_theme)
        
        # 更新根窗口背景
        self.root.configure(bg=self.colors['bg_window'])
        
        # 更新所有组件颜色
        for widget in [self.main_container, self.content_frame]:
            widget.configure(bg=self.colors['bg_window'])
        
        # 更新样式
        self.setup_styles()
        
        # 更新文本框
        self.result_text.configure(
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            highlightbackground=self.colors['border']
        )
        
        self.history_text.configure(
            bg=self.colors['entry_bg'],
            fg=self.colors['text_secondary'],
            highlightbackground=self.colors['border']
        )
        
        # 更新状态栏
        theme_name = "深色" if self.current_theme == 'dark' else "浅色"
        self.status_var.set(f"🎨 已切换到{theme_name}主题 | 就绪")
        
        # 重新创建标题等组件的颜色
        self.refresh_ui_colors()
    
    def refresh_ui_colors(self):
        """刷新所有UI组件的颜色"""
        # 重新创建头部颜色
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, tk.Frame):
                self.update_frame_colors(widget)
    
    def update_frame_colors(self, frame):
        """递归更新框架颜色"""
        try:
            if isinstance(frame, tk.Frame):
                frame.configure(bg=self.colors['bg_window'])
            for child in frame.winfo_children():
                self.update_frame_colors(child)
        except:
            pass
    
    def toggle_theme(self):
        """手动切换主题"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.update_theme()
    
    def start_theme_monitoring(self):
        """启动主题监控（Windows）"""
        def check_theme():
            new_theme = Win11Theme.detect_system_theme()
            if new_theme != self.current_theme:
                self.current_theme = new_theme
                self.update_theme()
            self.root.after(3000, check_theme)
        
        self.root.after(3000, check_theme)
    
    def copy_result(self):
        """复制结果到剪贴板"""
        result = self.result_text.get(1.0, tk.END).strip()
        if result and result != "等待输入...":
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.status_var.set("📋 结果已复制到剪贴板")
            self.root.after(2000, lambda: self.status_var.set("✨ 就绪 | 输入任意整数开始转换"))
    
    def digit_to_325(self, digit, position):
        """将单个数字转换为325表达式"""
        digit_mapping = {
            1: '(3×2-5)',
            2: '(3-2+5+3-2-5)',
            3: '(3+2+5+3-2×5)',
            4: '(-3+2+5)',
            5: '(3-2)×5',
            6: '(3-2+5)',
            7: '(-3+2×5)',
            8: '(3×2-5-3+2×5)',
            9: '3×(-2+5)'
        }
        
        if digit == 0:
            return None
        
        if digit not in digit_mapping:
            return str(digit)
        
        base_expr = digit_mapping[digit]
        
        if position == 0:
            return base_expr
        else:
            base10 = '(3+2+5)'
            factors = [base10] * position
            return f"{base_expr} × " + ' × '.join(factors)
    
    def number_to_325(self, input_num):
        """将数字转换为325计算公式"""
        if input_num == 0:
            return "3+2-5"
        
        abs_input_num = abs(input_num)
        num_str = str(abs_input_num)
        digits = [int(d) for d in num_str]
        num_digits = len(digits)
        
        parts = []
        for i, digit in enumerate(digits):
            position = num_digits - 1 - i
            expr = self.digit_to_325(digit, position)
            if expr:
                parts.append(expr)
        
        if not parts:
            return "0"
        
        result = " + ".join(parts)
        
        if input_num < 0:
            return f"-({result})"
        else:
            return result
    
    def get_detailed_breakdown(self, input_num):
        """获取详细的转换过程"""
        if input_num == 0:
            return "0 = 3+2-5"
        
        abs_input_num = abs(input_num)
        num_str = str(abs_input_num)
        digits = [int(d) for d in num_str]
        num_digits = len(digits)
        
        breakdown = []
        for i, digit in enumerate(digits):
            position = num_digits - 1 - i
            place_value = 10 ** position
            
            if digit != 0:
                expr = self.digit_to_325(digit, position)
                if expr:
                    breakdown.append(f"  📍 第{position+1}位 ({digit}×10^{position}) → {expr}")
        
        return "\n".join(breakdown)
    
    def calculate(self):
        """执行计算"""
        try:
            input_str = self.input_var.get().strip()
            if not input_str:
                self.status_var.set("⚠️ 请输入数字")
                return
            
            input_num = int(input_str)
            
            # 检查数字长度
            if len(input_str) > 100:
                if not messagebox.askyesno("确认", f"您输入了{len(input_str)}位数字，计算可能较慢，是否继续？"):
                    return
            
            # 计算结果
            result = self.number_to_325(input_num)
            breakdown = self.get_detailed_breakdown(input_num)
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            
            # 使用标签美化输出
            self.result_text.insert(tk.END, "转换结果\n", 'title')
            self.result_text.insert(tk.END, "─" * 55 + "\n")
            self.result_text.insert(tk.END, f"{input_num} = {result}\n\n", 'highlight')
            
            self.result_text.insert(tk.END, "详细信息\n", 'title')
            self.result_text.insert(tk.END, "─" * 55 + "\n")
            self.result_text.insert(tk.END, f"• 输入值: {input_num}\n", 'info')
            self.result_text.insert(tk.END, f"• 位数: {len(str(abs(input_num)))} 位\n", 'info')
            self.result_text.insert(tk.END, f"• 表达式长度: {len(result)} 字符\n\n", 'info')
            
            if breakdown:
                self.result_text.insert(tk.END, "数位分解\n", 'title')
                self.result_text.insert(tk.END, "─" * 55 + "\n")
                self.result_text.insert(tk.END, breakdown + "\n\n")
            
            self.result_text.insert(tk.END, "说明\n", 'title')
            self.result_text.insert(tk.END, "─" * 55 + "\n")
            self.result_text.insert(tk.END, "• 每个数位的数字转换为等值的3、2、5组合\n")
            self.result_text.insert(tk.END, "• 乘以 (3+2+5)=10 来实现数位对齐\n")
            self.result_text.insert(tk.END, "• 最终将所有数位的表达式相加")
            
            # 添加到历史记录
            history_entry = f"{input_num} = {result}"
            self.history.append(history_entry)
            if len(self.history) > 10:
                self.history.pop(0)
            
            self.update_history_display()
            
            # 更新状态栏
            self.status_var.set(f"✅ 计算完成 | {len(str(abs(input_num)))}位数")
            
            # 清空输入框
            self.input_var.set("")
            self.entry.focus()
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的整数！")
            self.status_var.set("❌ 输入格式无效")
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出现错误：{str(e)}")
            self.status_var.set(f"❌ {str(e)}")
    
    def clear_all(self):
        """清除所有输入和结果"""
        self.input_var.set("")
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("✨ 已清除 | 输入新数字开始转换")
        self.entry.focus()
    
    def clear_history(self):
        """清除历史记录"""
        if messagebox.askyesno("确认", "确定要清除所有历史记录吗？"):
            self.history.clear()
            self.history_text.delete(1.0, tk.END)
            self.status_var.set("🗑️ 历史记录已清除")
    
    def update_history_display(self):
        """更新历史记录显示"""
        self.history_text.delete(1.0, tk.END)
        if not self.history:
            self.history_text.insert(1.0, "暂无历史记录")
        else:
            for i, entry in enumerate(reversed(self.history), 1):
                display_entry = entry if len(entry) <= 80 else entry[:77] + "..."
                self.history_text.insert(tk.END, f"{i:2d}. {display_entry}\n")
    
    def show_examples(self):
        """显示示例"""
        examples = """Windows 11 风格 - 使用示例

基础示例：
• 输入 "0"     → 3+2-5
• 输入 "1"     → (3×2-5)
• 输入 "5"     → (3-2)×5
• 输入 "10"    → (3×2-5) + (3-2+5)
• 输入 "100"   → (3×2-5) × (3+2+5) × (3+2+5)

负数示例：
• 输入 "-42"   → -((3-2+5) + (3×2-5) × (3+2+5))

大数示例：
• 输入 "123456789" → 自动分解每一位并转换

键盘快捷键：
• Ctrl+C  - 复制结果
• Ctrl+H  - 清空历史
• Ctrl+T  - 切换深浅色主题
• Esc     - 清除输入

💡 提示：程序会自动检测并跟随 Windows 11 系统主题变化"""