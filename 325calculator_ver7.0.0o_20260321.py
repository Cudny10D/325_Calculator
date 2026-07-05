# 最后编辑于2026/03/21
# 自动适配系统深浅色主题 - 视觉效果增强版

import tkinter as tk
from tkinter import messagebox, ttk
import time
import sys
import os
import platform
import subprocess

class ThemeManager:
    """主题管理器 - 无需外部依赖"""
    
    # 深色主题配色
    DARK_THEME = {
        'bg_dark': '#1a1a2e',
        'bg_medium': '#16213e',
        'bg_light': '#0f3460',
        'accent': '#e94560',
        'accent_light': '#ff6b6b',
        'text_primary': '#eeeeee',
        'text_secondary': '#a8b2c6',
        'success': '#4caf50',
        'warning': '#ffa500',
        'info': '#2196f3',
        'entry_bg': '#2a2a3e',
        'button_bg': '#2a2a3e',
        'frame_bg': '#1a1a2e',
        'scrollbar_bg': '#2a2a3e',
        'scrollbar_thumb': '#4a4a6e',
        'sash_color': '#e94560'
    }
    
    # 浅色主题配色
    LIGHT_THEME = {
        'bg_dark': '#f5f5f7',
        'bg_medium': '#ffffff',
        'bg_light': '#e8e8ec',
        'accent': '#e94560',
        'accent_light': '#ff6b6b',
        'text_primary': '#2c3e50',
        'text_secondary': '#7f8c8d',
        'success': '#27ae60',
        'warning': '#f39c12',
        'info': '#3498db',
        'entry_bg': '#ffffff',
        'button_bg': '#f0f0f0',
        'frame_bg': '#f5f5f7',
        'scrollbar_bg': '#e8e8ec',
        'scrollbar_thumb': '#c0c0d0',
        'sash_color': '#e94560'
    }
    
    @staticmethod
    def detect_system_theme():
        """检测系统主题"""
        if sys.platform == 'darwin':
            try:
                result = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                    capture_output=True, text=True
                )
                if result.returncode == 0 and result.stdout.strip() == 'Dark':
                    return 'dark'
                else:
                    return 'light'
            except:
                pass
        
        if sys.platform == 'win32':
            try:
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r'Software\Microsoft\Windows\CurrentVersion\Themes\Personalize')
                try:
                    value, _ = winreg.QueryValueEx(key, 'AppsUseLightTheme')
                    winreg.CloseKey(key)
                    return 'light' if value == 1 else 'dark'
                except:
                    winreg.CloseKey(key)
            except:
                pass
        
        if sys.platform.startswith('linux'):
            try:
                result = subprocess.run(
                    ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    theme = result.stdout.strip().lower().strip("'")
                    if 'dark' in theme or 'black' in theme:
                        return 'dark'
                    else:
                        return 'light'
            except:
                pass
        
        return 'dark'
    
    @staticmethod
    def get_theme(theme_name=None):
        """获取主题配色"""
        if theme_name is None:
            theme_name = ThemeManager.detect_system_theme()
        
        if theme_name == 'light':
            return ThemeManager.LIGHT_THEME.copy()
        else:
            return ThemeManager.DARK_THEME.copy()


class ModernScrollbar(ttk.Frame):
    """自定义现代滚动条"""
    
    def __init__(self, parent, orient=tk.VERTICAL, **kwargs):
        super().__init__(parent, **kwargs)
        self.orient = orient
        self.canvas = tk.Canvas(self, highlightthickness=0, width=8)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.thumb = None
        self.is_dragging = False
        self.drag_start_y = 0
        self.drag_start_scroll = 0
        self.text_widget = None
        
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.canvas.bind('<Enter>', self.on_enter)
        self.canvas.bind('<Leave>', self.on_leave)
        
        self.update_colors()
    
    def update_colors(self):
        colors = ThemeManager.get_theme()
        self.bg_color = colors['scrollbar_bg']
        self.thumb_color = colors['scrollbar_thumb']
        self.thumb_hover_color = colors['accent']
        self.canvas.configure(bg=self.bg_color)
        self.update()
    
    def attach(self, text_widget):
        self.text_widget = text_widget
        self.text_widget.bind('<Configure>', lambda e: self.update())
        self.text_widget.bind('<MouseWheel>', self.on_mousewheel)
        self.update()
    
    def update(self):
        if not self.text_widget or not self.canvas.winfo_exists():
            return
        
        try:
            first_line = self.text_widget.index('@0,0')
            last_line = self.text_widget.index('@0,{}'.format(self.text_widget.winfo_height()))
            total_lines = int(self.text_widget.index('end-1c').split('.')[0])
            visible_lines = int(last_line.split('.')[0]) - int(first_line.split('.')[0])
            
            if total_lines <= visible_lines or visible_lines <= 0:
                self.canvas.delete('all')
                return
            
            canvas_height = self.canvas.winfo_height()
            if canvas_height <= 0:
                return
                
            thumb_height = max(30, (visible_lines / total_lines) * canvas_height)
            scroll_pos = int(first_line.split('.')[0]) / total_lines
            thumb_y = scroll_pos * (canvas_height - thumb_height)
            thumb_y = max(0, min(canvas_height - thumb_height, thumb_y))
            
            self.canvas.delete('all')
            self.thumb = self.canvas.create_rectangle(
                2, thumb_y, self.canvas.winfo_width() - 2, thumb_y + thumb_height,
                fill=self.thumb_color, outline='', tags='thumb', width=0
            )
        except:
            pass
    
    def on_click(self, event):
        if not self.thumb or not self.text_widget:
            return
        
        thumb_coords = self.canvas.coords(self.thumb)
        if thumb_coords and len(thumb_coords) >= 4:
            if thumb_coords[1] <= event.y <= thumb_coords[3]:
                self.is_dragging = True
                self.drag_start_y = event.y
                try:
                    self.drag_start_scroll = float(self.text_widget.index('@0,0').split('.')[0])
                except:
                    self.drag_start_scroll = 0
                self.canvas.config(cursor='hand2')
    
    def on_drag(self, event):
        if not self.is_dragging or not self.thumb or not self.text_widget:
            return
        
        try:
            canvas_height = self.canvas.winfo_height()
            if canvas_height <= 0:
                return
                
            thumb_coords = self.canvas.coords(self.thumb)
            if not thumb_coords or len(thumb_coords) < 4:
                return
                
            thumb_height = thumb_coords[3] - thumb_coords[1]
            delta_y = event.y - self.drag_start_y
            
            if canvas_height > thumb_height:
                scroll_range = canvas_height - thumb_height
                scroll_percent = delta_y / scroll_range
                total_lines = int(self.text_widget.index('end-1c').split('.')[0])
                scroll_lines = int(scroll_percent * total_lines)
                new_position = self.drag_start_scroll + scroll_lines
                new_position = max(0, min(total_lines - 1, new_position))
                
                if total_lines > 0:
                    self.text_widget.yview_moveto(new_position / total_lines)
                    self.update()
        except:
            pass
    
    def on_release(self, event):
        self.is_dragging = False
        self.canvas.config(cursor='')
    
    def on_enter(self, event):
        if self.thumb:
            self.canvas.itemconfig(self.thumb, fill=self.thumb_hover_color)
    
    def on_leave(self, event):
        if self.thumb:
            self.canvas.itemconfig(self.thumb, fill=self.thumb_color)
        self.is_dragging = False
        self.canvas.config(cursor='')
    
    def on_mousewheel(self, event):
        if not self.text_widget:
            return
        
        try:
            if hasattr(event, 'delta'):
                self.text_widget.yview_scroll(int(-event.delta / 120), 'units')
            else:
                self.text_widget.yview_scroll(-1 * event.num, 'units')
            self.update()
        except:
            pass


class VisualEffects:
    """视觉效果管理器"""
    
    def __init__(self, root):
        self.root = root
        self.is_glass = False
        self.original_bg = None
        
    def toggle_glass_effect(self, intensity=0.92):
        """切换半透明毛玻璃效果"""
        try:
            if not self.is_glass:
                # 启用半透明效果
                self.original_bg = self.root.cget('bg')
                self.root.attributes('-alpha', intensity)
                self.is_glass = True
                return True
            else:
                # 禁用半透明效果
                self.root.attributes('-alpha', 1.0)
                self.is_glass = False
                return True
        except Exception as e:
            print(f"视觉效果切换失败: {e}")
            return False
    
    def set_glass_intensity(self, intensity):
        """设置透明度强度"""
        if self.is_glass:
            try:
                self.root.attributes('-alpha', intensity)
                return True
            except:
                return False
        return False


class ModernNumberTo325Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("数字转325计算公式 - 视觉增强版")
        
        # 窗口设置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1000
        window_height = 800
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(900, 700)
        self.root.resizable(True, True)
        
        # 主题
        self.current_theme = ThemeManager.detect_system_theme()
        self.colors = ThemeManager.get_theme(self.current_theme)
        self.root.configure(bg=self.colors['bg_dark'])
        
        # 视觉效果
        self.visual_effects = VisualEffects(root)
        
        # 使用 PanedWindow 作为主容器
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 上半部分：输入和结果区域
        self.top_container = tk.Frame(self.main_paned, bg=self.colors['bg_dark'])
        self.main_paned.add(self.top_container, weight=2)
        
        # 下半部分：历史记录区域
        self.bottom_container = tk.Frame(self.main_paned, bg=self.colors['bg_dark'])
        self.main_paned.add(self.bottom_container, weight=1)
        
        # 配置 PanedWindow 分割线样式
        self.setup_paned_style()
        
        # 创建上半部分的内容
        self.create_top_content()
        
        # 创建下半部分的内容
        self.create_bottom_content()
        
        # 创建底部状态栏
        self.create_footer()
        
        # 变量初始化
        self.history = []
        self.animation_id = None
        self.theme_monitor_id = None
        
        # 设置键盘快捷键
        self.setup_shortcuts()
        
        # 初始焦点
        self.entry.focus()
        
        # 启动主题监控
        self.start_theme_monitoring()
        
        # 淡入效果
        self.fade_in()
    
    def setup_paned_style(self):
        """设置 PanedWindow 分割线样式"""
        style = ttk.Style()
        
        # 配置分割线样式
        style.configure('Vertical.TPanedwindow', background=self.colors['bg_dark'])
        style.configure('Vertical.TPanedwindow.Sash', 
                       background=self.colors['sash_color'],
                       relief='flat',
                       borderwidth=2,
                       width=4)
        style.map('Vertical.TPanedwindow.Sash',
                 background=[('active', self.colors['accent_light'])])
    
    def create_top_content(self):
        """创建上半部分内容"""
        # 头部
        self.create_header()
        
        # 输入区域
        self.create_input_section()
        
        # 结果区域
        self.create_result_section()
    
    def create_bottom_content(self):
        """创建下半部分内容"""
        self.create_history_section()
    
    def setup_styles(self):
        """设置ttk样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 按钮样式
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('微软雅黑', 10, 'bold'))
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_light']),
                           ('pressed', self.colors['accent'])])
        
        style.configure('Modern.TButton',
                       background=self.colors['button_bg'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='flat',
                       font=('微软雅黑', 10))
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_light']),
                           ('pressed', self.colors['bg_light'])])
        
        # 输入框样式
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['entry_bg'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='flat',
                       font=('Consolas', 11))
        
        # 标签框样式
        style.configure('Modern.TLabelframe',
                       background=self.colors['bg_dark'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['accent'],
                       borderwidth=2,
                       relief='flat')
        style.configure('Modern.TLabelframe.Label',
                       background=self.colors['bg_dark'],
                       foreground=self.colors['accent'],
                       font=('微软雅黑', 11, 'bold'))
    
    def update_theme(self):
        """更新主题"""
        self.colors = ThemeManager.get_theme(self.current_theme)
        
        # 更新背景
        self.root.configure(bg=self.colors['bg_dark'])
        self.top_container.configure(bg=self.colors['bg_dark'])
        self.bottom_container.configure(bg=self.colors['bg_dark'])
        
        # 更新分割线样式
        style = ttk.Style()
        style.configure('Vertical.TPanedwindow.Sash', 
                       background=self.colors['sash_color'])
        style.map('Vertical.TPanedwindow.Sash',
                 background=[('active', self.colors['accent_light'])])
        
        # 更新样式
        self.setup_styles()
        
        # 更新滚动条
        if hasattr(self, 'result_scrollbar'):
            self.result_scrollbar.update_colors()
        if hasattr(self, 'history_scrollbar'):
            self.history_scrollbar.update_colors()
        
        # 更新所有组件颜色
        self.update_all_widgets_colors()
        
        # 更新状态栏
        theme_name = "深色" if self.current_theme == 'dark' else "浅色"
        glass_status = "🌫️ 玻璃效果" if self.visual_effects.is_glass else "✨ 标准模式"
        self.status_var.set(f"🎨 {theme_name}主题 | {glass_status}")
    
    def update_all_widgets_colors(self):
        """递归更新所有组件的颜色"""
        for widget in self.top_container.winfo_children():
            self.update_widget_color(widget)
        for widget in self.bottom_container.winfo_children():
            self.update_widget_color(widget)
        
        # 更新文本框标签
        self.result_text.tag_configure('title', font=('Consolas', 12, 'bold'), 
                                      foreground=self.colors['accent'])
        self.result_text.tag_configure('highlight', foreground=self.colors['success'])
        self.result_text.tag_configure('info', foreground=self.colors['info'])
        self.result_text.tag_configure('warning', foreground=self.colors['warning'])
    
    def update_widget_color(self, widget):
        """递归更新单个组件颜色"""
        try:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.colors['bg_dark'])
            elif isinstance(widget, tk.Label):
                current_bg = widget.cget('bg')
                if current_bg in ['#1a1a2e', '#f5f5f7', '#16213e', '#ffffff', '#0f3460', '#e8e8ec']:
                    widget.configure(bg=self.colors['bg_dark'])
                widget.configure(fg=self.colors['text_primary'])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.colors['button_bg'],
                               fg=self.colors['text_primary'],
                               activebackground=self.colors['accent_light'],
                               activeforeground='white')
            elif isinstance(widget, ttk.LabelFrame):
                widget.configure(style='Modern.TLabelframe')
                for child in widget.winfo_children():
                    self.update_widget_color(child)
            elif isinstance(widget, tk.Text):
                widget.configure(bg=self.colors['bg_medium'],
                               fg=self.colors['text_primary'])
            elif isinstance(widget, ttk.Entry):
                widget.configure(style='Modern.TEntry')
            
            for child in widget.winfo_children():
                self.update_widget_color(child)
        except:
            pass
    
    def toggle_theme(self):
        """手动切换主题"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.update_theme()
    
    def toggle_visual_effect(self):
        """切换视觉效果"""
        if self.visual_effects.toggle_glass_effect(0.92):
            status = "🌫️ 玻璃效果已开启" if self.visual_effects.is_glass else "✨ 标准模式已开启"
            self.status_var.set(status)
            self.root.after(2000, lambda: self.update_theme())
        else:
            self.status_var.set("⚠️ 视觉效果切换失败")
            self.root.after(2000, lambda: self.update_theme())
    
    def start_theme_monitoring(self):
        """启动主题监控"""
        def check_theme():
            try:
                new_theme = ThemeManager.detect_system_theme()
                if new_theme != self.current_theme:
                    self.current_theme = new_theme
                    self.update_theme()
            except:
                pass
            self.theme_monitor_id = self.root.after(3000, check_theme)
        
        self.theme_monitor_id = self.root.after(3000, check_theme)
    
    def create_header(self):
        """创建头部"""
        header_frame = tk.Frame(self.top_container, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_container = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        title_container.pack(fill=tk.X)
        
        title_label = tk.Label(title_container, 
                              text="✨ 数字转325计算公式 ✨", 
                              font=('微软雅黑', 20, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_dark'])
        title_label.pack(side=tk.LEFT)
        
        # 按钮容器
        button_container = tk.Frame(title_container, bg=self.colors['bg_dark'])
        button_container.pack(side=tk.RIGHT)
        
        # 视觉效果按钮
        glass_btn = tk.Button(button_container,
                             text="🌫️ 玻璃效果",
                             font=('微软雅黑', 9),
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_light'],
                             activebackground=self.colors['accent'],
                             activeforeground='white',
                             relief='flat',
                             cursor='hand2',
                             command=self.toggle_visual_effect)
        glass_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 主题切换按钮
        theme_btn = tk.Button(button_container,
                             text="🌓 切换主题",
                             font=('微软雅黑', 9),
                             fg=self.colors['text_primary'],
                             bg=self.colors['bg_light'],
                             activebackground=self.colors['accent'],
                             activeforeground='white',
                             relief='flat',
                             cursor='hand2',
                             command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)
        
        subtitle_label = tk.Label(header_frame,
                                 text="将任意整数转换为包含3、2、5的数学表达式 | 支持玻璃效果",
                                 font=('微软雅黑', 10),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(5, 0))
        
        separator = tk.Frame(header_frame, height=2, bg=self.colors['accent'])
        separator.pack(fill=tk.X, pady=(10, 0))
    
    def create_input_section(self):
        """创建输入区域"""
        input_frame = tk.Frame(self.top_container, bg=self.colors['bg_dark'])
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        label_frame = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        label_frame.pack(fill=tk.X)
        
        tk.Label(label_frame,
                text="📝 输入数字",
                font=('微软雅黑', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_dark']).pack(side=tk.LEFT)
        
        tk.Label(label_frame,
                text="支持任意长度整数 | 拖动分割线调整布局 | 玻璃效果",
                font=('微软雅黑', 9),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_dark']).pack(side=tk.RIGHT)
        
        entry_container = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        entry_container.pack(fill=tk.X, pady=(10, 10))
        
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(entry_container, 
                               textvariable=self.input_var,
                               style='Modern.TEntry',
                               font=('Consolas', 12))
        self.entry.pack(fill=tk.X, ipady=8)
        
        button_container = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        button_container.pack(fill=tk.X)
        
        buttons = [
            ("🔢 计算", self.calculate, 'Accent.TButton'),
            ("🗑️ 清除", self.clear_all, 'Modern.TButton'),
            ("📚 示例", self.show_examples, 'Modern.TButton'),
            ("❓ 关于", self.show_about, 'Modern.TButton')
        ]
        
        for text, command, style in buttons:
            btn = ttk.Button(button_container, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def create_result_section(self):
        """创建结果区域"""
        result_frame = ttk.LabelFrame(self.top_container, 
                                      text="📊 计算结果", 
                                      style='Modern.TLabelframe',
                                      padding="12")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        content_container = tk.Frame(result_frame, bg=self.colors['bg_dark'])
        content_container.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(content_container,
                                  font=('Consolas', 11),
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['text_primary'],
                                  selectbackground=self.colors['accent'],
                                  selectforeground='white',
                                  wrap=tk.WORD,
                                  relief='flat',
                                  borderwidth=0,
                                  padx=8,
                                  pady=8)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.result_scrollbar = ModernScrollbar(content_container, tk.VERTICAL)
        self.result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 0))
        self.result_scrollbar.attach(self.result_text)
        
        self.result_text.tag_configure('title', font=('Consolas', 12, 'bold'), 
                                      foreground=self.colors['accent'])
        self.result_text.tag_configure('highlight', foreground=self.colors['success'])
        self.result_text.tag_configure('info', foreground=self.colors['info'])
        self.result_text.tag_configure('warning', foreground=self.colors['warning'])
        
        copy_btn_frame = tk.Frame(result_frame, bg=self.colors['bg_dark'])
        copy_btn_frame.pack(fill=tk.X, pady=(8, 0))
        
        ttk.Button(copy_btn_frame,
                  text="📋 复制结果",
                  command=self.copy_result,
                  style='Modern.TButton').pack(side=tk.RIGHT)
    
    def create_history_section(self):
        """创建历史记录区域"""
        history_frame = ttk.LabelFrame(self.bottom_container,
                                      text="📜 历史记录 (最近10条)",
                                      style='Modern.TLabelframe',
                                      padding="12")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        content_container = tk.Frame(history_frame, bg=self.colors['bg_dark'])
        content_container.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(content_container,
                                   font=('Consolas', 10),
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['text_secondary'],
                                   wrap=tk.WORD,
                                   relief='flat',
                                   borderwidth=0,
                                   padx=8,
                                   pady=8)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.history_scrollbar = ModernScrollbar(content_container, tk.VERTICAL)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(2, 0))
        self.history_scrollbar.attach(self.history_text)
        
        history_btn_frame = tk.Frame(history_frame, bg=self.colors['bg_dark'])
        history_btn_frame.pack(fill=tk.X, pady=(8, 0))
        
        ttk.Button(history_btn_frame,
                  text="🗑️ 清空历史",
                  command=self.clear_history,
                  style='Modern.TButton').pack(side=tk.RIGHT)
        
        self.history_text.insert(1.0, "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录")
    
    def create_footer(self):
        """创建底部状态栏"""
        footer_frame = tk.Frame(self.root, bg=self.colors['bg_medium'], height=35)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        theme_name = "深色" if self.current_theme == 'dark' else "浅色"
        self.status_var.set(f"✨ {theme_name}主题 | 就绪 | 输入任意整数开始转换")
        status_label = tk.Label(footer_frame,
                               textvariable=self.status_var,
                               font=('微软雅黑', 9),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_medium'])
        status_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        self.time_var = tk.StringVar()
        self.update_time()
        time_label = tk.Label(footer_frame,
                             textvariable=self.time_var,
                             font=('Consolas', 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_medium'])
        time_label.pack(side=tk.RIGHT, padx=10, pady=8)
        
        indicator = tk.Label(footer_frame,
                           text="🔄 自动同步系统主题 | 🌫️ 玻璃效果 (Ctrl+G)",
                           font=('微软雅黑', 8),
                           fg=self.colors['success'],
                           bg=self.colors['bg_medium'])
        indicator.pack(side=tk.RIGHT, padx=10, pady=8)
    
    def setup_shortcuts(self):
        """设置键盘快捷键"""
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-h>', lambda e: self.clear_history())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<Control-g>', lambda e: self.toggle_visual_effect())  # Ctrl+G 切换玻璃效果
        self.root.bind('<Escape>', lambda e: self.clear_all())
        self.root.bind('<Return>', lambda e: self.calculate())
    
    def update_time(self):
        """更新时间显示"""
        current_time = time.strftime("%H:%M:%S")
        self.time_var.set(f"🕐 {current_time}")
        self.root.after(1000, self.update_time)
    
    def fade_in(self):
        """淡入效果"""
        alpha = 0
        while alpha <= 1:
            self.root.attributes('-alpha', alpha)
            alpha += 0.1
            self.root.update()
            time.sleep(0.02)
    
    def animate_result(self):
        """结果动画效果"""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        original_bg = self.result_text.cget('bg')
        self.result_text.configure(bg=self.colors['accent'])
        self.animation_id = self.root.after(200, lambda: self.result_text.configure(bg=original_bg))
    
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
            1: '(3*2-5)',
            2: '(3-2+5+3-2-5)',
            3: '(3+2+5+3-2*5)',
            4: '(-3+2+5)',
            5: '(3-2)*5',
            6: '(3-2+5)',
            7: '(-3+2*5)',
            8: '(3*2-5-3+2*5)',
            9: '3*(-2+5)'
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
            
            if len(input_str) > 100:
                if not messagebox.askyesno("确认", f"您输入了{len(input_str)}位数字，计算可能较慢，是否继续？"):
                    return
            
            result = self.number_to_325(input_num)
            breakdown = self.get_detailed_breakdown(input_num)
            
            self.result_text.delete(1.0, tk.END)
            
            self.result_text.insert(tk.END, "🎯 转换结果\n", 'title')
            self.result_text.insert(tk.END, "─" * 60 + "\n")
            self.result_text.insert(tk.END, f"{input_num} = {result}\n\n", 'highlight')
            
            self.result_text.insert(tk.END, "📊 详细信息\n", 'title')
            self.result_text.insert(tk.END, "─" * 60 + "\n")
            self.result_text.insert(tk.END, f"• 输入值: {input_num}\n", 'info')
            self.result_text.insert(tk.END, f"• 位数: {len(str(abs(input_num)))} 位\n", 'info')
            self.result_text.insert(tk.END, f"• 表达式长度: {len(result)} 字符\n\n", 'info')
            
            if breakdown:
                self.result_text.insert(tk.END, "🔢 数位分解\n", 'title')
                self.result_text.insert(tk.END, "─" * 60 + "\n")
                self.result_text.insert(tk.END, breakdown + "\n\n")
            
            self.result_text.insert(tk.END, "💡 说明\n", 'title')
            self.result_text.insert(tk.END, "─" * 60 + "\n")
            self.result_text.insert(tk.END, "• 每个数位的数字转换为等值的3、2、5组合\n")
            self.result_text.insert(tk.END, "• 乘以 (3+2+5)=10 来实现数位对齐\n")
            self.result_text.insert(tk.END, "• 最终将所有数位的表达式相加")
            
            history_entry = f"{input_num} = {result}"
            self.history.append(history_entry)
            if len(self.history) > 10:
                self.history.pop(0)
            
            self.update_history_display()
            
            self.status_var.set(f"✅ 计算完成 | {len(str(abs(input_num)))}位数")
            self.animate_result()
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
            self.history_text.insert(1.0, "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录")
            self.status_var.set("🗑️ 历史记录已清除")
    
    def update_history_display(self):
        """更新历史记录显示"""
        self.history_text.delete(1.0, tk.END)
        if not self.history:
            self.history_text.insert(1.0, "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录")
        else:
            for i, entry in enumerate(reversed(self.history), 1):
                display_entry = entry if len(entry) <= 90 else entry[:87] + "..."
                self.history_text.insert(tk.END, f"{i:2d}. {display_entry}\n")
        
        if hasattr(self, 'history_scrollbar'):
            self.history_scrollbar.update()
    
    def show_examples(self):
        """显示示例"""
        examples = """🎯 使用示例

基础示例：
• 输入 "0"     → 3+2-5
• 输入 "1"     → (3*2-5)
• 输入 "5"     → (3-2)*5
• 输入 "10"    → (3*2-5) + (3-2+5)
• 输入 "100"   → (3*2-5) × (3+2+5) × (3+2+5)

负数示例：
• 输入 "-42"   → -((3-2+5) + (3*2-5) × (3+2+5))

界面特性：
• 🌫️ 玻璃效果（点击顶部按钮或 Ctrl+G 切换）
• 彩色现代分割线（跟随主题色）
• 可拖动分割线调整上下区域大小
• 支持窗口缩放（最小900x700）
• 自定义现代滚动条
• 回车键直接计算
• Ctrl+T 切换主题
• Ctrl+G 切换玻璃效果

键盘快捷键：
• Ctrl+C  - 复制结果
• Ctrl+H  - 清空历史
• Ctrl+T  - 切换深浅色主题
• Ctrl+G  - 切换玻璃效果
• Enter   - 计算
• Esc     - 清除输入

💡 提示：玻璃效果使窗口呈现半透明视觉效果，提升使用体验"""
        
        messagebox.showinfo("使用示例", examples)
    
    def show_about(self):
        """显示关于对话框"""
        about_text = f"""✨ 数字转325计算公式 ✨
版本 6.1.0

🎨 主题特性：
• 自动检测系统深浅色主题
• 支持 macOS/Windows/Linux
• 实时跟随系统主题变化
• 手动切换主题 (Ctrl+T)
• 🌫️ 玻璃效果（Ctrl+G 切换）
• 彩色现代分割线设计
• 自定义现代滚动条

🎯 核心功能：
• 任意长度整数转换
• 详细的转换过程
• 历史记录管理
• 结果一键复制

🖥️ 界面优化：
• 🌫️ 玻璃半透明视觉效果
• 彩色分割线（主题色）
• 可拖动调整布局
• 响应式设计
• 美观的滚动条
• 稳定的 PanedWindow 布局

🔧 技术实现：
• Python + Tkinter
• 跨平台主题检测
• 动态主题切换
• 半透明视觉效果
• 优化的转换算法

👨‍💻 开发者：Shichi Neko
📅 最后更新：2026年3月21日

Enjoy! 🎉"""
        
        messagebox.showinfo("关于", about_text)
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'theme_monitor_id') and self.theme_monitor_id:
            try:
                self.root.after_cancel(self.theme_monitor_id)
            except:
                pass


def main():
    """主函数"""
    root = tk.Tk()
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    app = ModernNumberTo325Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()