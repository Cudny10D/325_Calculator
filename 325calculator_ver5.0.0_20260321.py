# 最后编辑于2026/03/21 Ver2.0.5
# 美化GUI版本 - 现代化界面设计

import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

class ModernNumberTo325Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("数字转325计算公式 - 优雅版")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 设置颜色主题
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'accent_light': '#ff6b6b',
            'text_primary': '#eeeeee',
            'text_secondary': '#a8b2c6',
            'success': '#4caf50',
            'warning': '#ffa500',
            'info': '#2196f3'
        }
        
        # 配置根窗口
        self.root.configure(bg=self.colors['bg_dark'])
        
        # 创建主容器
        self.main_container = tk.Frame(root, bg=self.colors['bg_dark'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建自定义样式
        self.setup_styles()
        
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
        
        # 添加淡入效果
        self.fade_in()
    
    def setup_styles(self):
        """设置ttk样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义按钮样式
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('微软雅黑', 10, 'bold'))
        style.map('Accent.TButton',
                 background=[('active', self.colors['accent_light']),
                           ('pressed', self.colors['accent'])])
        
        # 普通按钮样式
        style.configure('Modern.TButton',
                       background=self.colors['bg_light'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='flat',
                       font=('微软雅黑', 10))
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent']),
                           ('pressed', self.colors['bg_medium'])])
        
        # 输入框样式
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['bg_medium'],
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
        
        # 状态栏样式
        style.configure('Status.TLabel',
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text_secondary'],
                       font=('微软雅黑', 9))
    
    def create_header(self):
        """创建头部"""
        header_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 标题
        title_label = tk.Label(header_frame, 
                              text="✨ 数字转325计算公式 ✨", 
                              font=('微软雅黑', 20, 'bold'),
                              fg=self.colors['accent'],
                              bg=self.colors['bg_dark'])
        title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(header_frame,
                                 text="将任意整数转换为包含3、2、5的数学表达式",
                                 font=('微软雅黑', 10),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(5, 0))
        
        # 装饰线
        separator = tk.Frame(header_frame, height=2, bg=self.colors['accent'])
        separator.pack(fill=tk.X, pady=(10, 0))
    
    def create_input_section(self):
        """创建输入区域"""
        input_frame = tk.Frame(self.main_container, bg=self.colors['bg_dark'])
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 输入标签
        label_frame = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        label_frame.pack(fill=tk.X)
        
        tk.Label(label_frame,
                text="📝 输入数字",
                font=('微软雅黑', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_dark']).pack(side=tk.LEFT)
        
        tk.Label(label_frame,
                text="支持任意长度整数",
                font=('微软雅黑', 9),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_dark']).pack(side=tk.RIGHT)
        
        # 输入框容器
        entry_container = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        entry_container.pack(fill=tk.X, pady=(10, 10))
        
        # 输入框
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(entry_container, 
                               textvariable=self.input_var,
                               style='Modern.TEntry',
                               font=('Consolas', 12))
        self.entry.pack(fill=tk.X, ipady=8)
        
        # 按钮容器
        button_container = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        button_container.pack(fill=tk.X)
        
        # 创建按钮网格
        buttons = [
            ("🔢 计算", self.calculate, 'Accent.TButton'),
            ("🗑️ 清除", self.clear_all, 'Modern.TButton'),
            ("📚 示例", self.show_examples, 'Modern.TButton'),
            ("❓ 关于", self.show_about, 'Modern.TButton')
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            btn = ttk.Button(button_container, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def create_result_section(self):
        """创建结果区域"""
        result_frame = ttk.LabelFrame(self.main_container, 
                                      text="📊 计算结果", 
                                      style='Modern.TLabelframe',
                                      padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 结果文本框
        self.result_text = tk.Text(result_frame,
                                  height=12,
                                  font=('Consolas', 11),
                                  bg=self.colors['bg_medium'],
                                  fg=self.colors['text_primary'],
                                  selectbackground=self.colors['accent'],
                                  selectforeground='white',
                                  wrap=tk.WORD,
                                  relief='flat',
                                  borderwidth=0)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, 
                                 command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 配置文本框标签
        self.result_text.tag_configure('title', font=('Consolas', 12, 'bold'), 
                                      foreground=self.colors['accent'])
        self.result_text.tag_configure('highlight', foreground=self.colors['success'])
        self.result_text.tag_configure('info', foreground=self.colors['info'])
        self.result_text.tag_configure('warning', foreground=self.colors['warning'])
    
    def create_history_section(self):
        """创建历史记录区域"""
        history_frame = ttk.LabelFrame(self.main_container,
                                      text="📜 历史记录",
                                      style='Modern.TLabelframe',
                                      padding="15")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 历史记录文本框
        self.history_text = tk.Text(history_frame,
                                   height=6,
                                   font=('Consolas', 10),
                                   bg=self.colors['bg_medium'],
                                   fg=self.colors['text_secondary'],
                                   wrap=tk.WORD,
                                   relief='flat',
                                   borderwidth=0)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL,
                                         command=self.history_text.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        
        # 历史记录按钮
        history_btn_frame = tk.Frame(history_frame, bg=self.colors['bg_medium'])
        history_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(history_btn_frame,
                  text="🗑️ 清空历史",
                  command=self.clear_history,
                  style='Modern.TButton').pack(side=tk.RIGHT)
    
    def create_footer(self):
        """创建底部状态栏"""
        footer_frame = tk.Frame(self.main_container, bg=self.colors['bg_medium'])
        footer_frame.pack(fill=tk.X)
        
        # 状态标签
        self.status_var = tk.StringVar()
        self.status_var.set("✨ 就绪 | 输入任意整数开始转换")
        status_label = tk.Label(footer_frame,
                               textvariable=self.status_var,
                               font=('微软雅黑', 9),
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_medium'],
                               padx=10,
                               pady=5)
        status_label.pack(side=tk.LEFT)
        
        # 时间显示
        self.time_var = tk.StringVar()
        self.update_time()
        time_label = tk.Label(footer_frame,
                             textvariable=self.time_var,
                             font=('Consolas', 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['bg_medium'],
                             padx=10,
                             pady=5)
        time_label.pack(side=tk.RIGHT)
    
    def setup_shortcuts(self):
        """设置键盘快捷键"""
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-h>', lambda e: self.clear_history())
        self.root.bind('<Escape>', lambda e: self.clear_all())
    
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
        
        # 临时改变结果框颜色
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
            self.result_text.insert(tk.END, "🎯 转换结果\n", 'title')
            self.result_text.insert(tk.END, "─" * 50 + "\n")
            self.result_text.insert(tk.END, f"{input_num} = {result}\n\n", 'highlight')
            
            self.result_text.insert(tk.END, "📊 详细信息\n", 'title')
            self.result_text.insert(tk.END, "─" * 50 + "\n")
            self.result_text.insert(tk.END, f"• 输入值: {input_num}\n", 'info')
            self.result_text.insert(tk.END, f"• 位数: {len(str(abs(input_num)))} 位\n", 'info')
            self.result_text.insert(tk.END, f"• 表达式长度: {len(result)} 字符\n\n", 'info')
            
            if breakdown:
                self.result_text.insert(tk.END, "🔢 数位分解\n", 'title')
                self.result_text.insert(tk.END, "─" * 50 + "\n")
                self.result_text.insert(tk.END, breakdown + "\n\n")
            
            self.result_text.insert(tk.END, "💡 说明\n", 'title')
            self.result_text.insert(tk.END, "─" * 50 + "\n")
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
            self.status_var.set(f"✅ 计算完成 | {len(str(abs(input_num)))}位数 | {history_entry[:40]}...")
            
            # 动画效果
            self.animate_result()
            
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
                display_entry = entry if len(entry) <= 70 else entry[:67] + "..."
                self.history_text.insert(tk.END, f"{i:2d}. {display_entry}\n")
    
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

大数示例：
• 输入 "123456789" → 自动分解每一位并转换

键盘快捷键：
• Ctrl+C  - 复制结果
• Ctrl+H  - 清空历史
• Esc     - 清除输入

💡 提示：支持任意长度整数，但过长的数字（>100位）可能计算较慢"""
        
        messagebox.showinfo("使用示例", examples)
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """✨ 数字转325计算公式 ✨
版本 5.0.0 - GUI大变化！

🎨 特色功能：
• 现代化深色界面设计
• 动态动画效果
• 实时状态提示
• 键盘快捷键支持
• 详细转换过程展示

🔧 技术实现：
• Python + Tkinter
• 动态位数处理算法
• 支持任意长度整数
• 优雅的错误处理

📊 核心原理：
将每个数位的数字转换为等值的3、2、5表达式，
通过 (3+2+5)=10 来实现数位对齐。

👨‍💻 开发者：Shichi Neko
📅 最后更新：2026年3月21日

Enjoy! 🎉"""
        
        messagebox.showinfo("关于", about_text)


def main():
    """主函数"""
    root = tk.Tk()
    app = ModernNumberTo325Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()