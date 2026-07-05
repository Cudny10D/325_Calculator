# 最后编辑于2026/03/21 Ver2.0.3
# 添加GUI界面

import tkinter as tk
from tkinter import messagebox, ttk

class NumberTo325Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("数字转325计算公式")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置样式
        self.root.configure(bg='#f0f0f0')
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="数字转325计算公式", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 输入框
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(input_frame, text="输入整数：", font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 10))
        
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(input_frame, textvariable=self.input_var, width=30, font=('Arial', 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', lambda e: self.calculate())
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        
        ttk.Button(button_frame, text="计算", command=self.calculate, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清除", command=self.clear_all, width=15).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding="10")
        result_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 使用Text组件显示结果（支持多行和滚动）
        self.result_text = tk.Text(result_frame, height=8, width=50, font=('Courier', 11), 
                                  wrap=tk.WORD, bg='white', relief=tk.SUNKEN)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 历史记录区域
        history_frame = ttk.LabelFrame(main_frame, text="历史记录", padding="10")
        history_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        self.history_text = tk.Text(history_frame, height=6, width=50, font=('Courier', 10), 
                                    wrap=tk.WORD, bg='#fafafa')
        self.history_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 历史记录滚动条
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        
        # 底部按钮
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=5, column=0, pady=(10, 0))
        
        ttk.Button(bottom_frame, text="清空历史", command=self.clear_history, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="关于", command=self.show_about, width=12).pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 | 输入绝对值小于1,000,000,000的整数")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 历史记录列表
        self.history = []
        
        # 初始化输入框焦点
        self.entry.focus()
        
        # 定义映射表
        self.mapping = {
            1:'(3*2-5)',
            2:'(3-2+5+3-2-5)',
            3:'(3+2+5+3-2*5)',
            4:'(-3+2+5)',
            5:'(3-2)*5',
            6:'(3-2+5)',
            7:'(-3+2*5)',
            8:'(3*2-5-3+2*5)',
            9:"3*(-2+5)"
        }
    
    def number_to_325(self, input_num):
        """将数字转换为325计算公式"""
        if input_num == 0:
            return "3+2-5"
        
        abs_input_num = abs(input_num)
        
        # 提取各位数字
        num1 = abs_input_num % 10
        num2 = (abs_input_num % 100) // 10
        num3 = (abs_input_num % 1000) // 100
        num4 = (abs_input_num % 10000) // 1000
        num5 = (abs_input_num % 100000) // 10000
        num6 = (abs_input_num % 1000000) // 100000
        num7 = (abs_input_num % 10000000) // 1000000
        num8 = (abs_input_num % 100000000) // 10000000
        num9 = abs_input_num // 100000000
        
        nums = [num9, num8, num7, num6, num5, num4, num3, num2, num1]
        out_nums = []
        
        for i, val in enumerate(nums):
            if val == 0:
                out_nums.append(None)
            elif val in self.mapping:
                if i == 8:  # 个位
                    out_nums.append(self.mapping[val])
                else:
                    base = '(3+2+5)'
                    power = 8 - i  # 实际位数
                    factors = [base] * power
                    out_nums.append(f"{self.mapping[val]} * " + ' * '.join(factors))
            else:
                out_nums.append(None)
        
        # 过滤None
        parts = [p for p in out_nums if p is not None]
        
        if not parts:
            return "0"
        
        result = " + ".join(parts)
        
        if input_num < 0:
            return f"-({result})"
        else:
            return result
    
    def calculate(self):
        """执行计算"""
        try:
            input_str = self.input_var.get().strip()
            if not input_str:
                self.status_var.set("错误：请输入数字")
                return
            
            input_num = int(input_str)
            
            # 验证输入范围
            if abs(input_num) >= 1000000000:
                messagebox.showerror("输入错误", "请输入绝对值小于1,000,000,000的整数！")
                self.status_var.set("错误：输入数值超出范围")
                return
            
            # 计算结果
            result = self.number_to_325(input_num)
            
            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, f"{input_num} = {result}\n\n")
            self.result_text.insert(tk.END, f"转换详情：\n")
            self.result_text.insert(tk.END, f"• 输入值: {input_num}\n")
            self.result_text.insert(tk.END, f"• 绝对值: {abs(input_num)}\n")
            self.result_text.insert(tk.END, f"• 表达式: {result}")
            
            # 添加到历史记录
            history_entry = f"{input_num} = {result}"
            self.history.append(history_entry)
            if len(self.history) > 10:  # 只保留最近10条记录
                self.history.pop(0)
            
            # 更新历史显示
            self.update_history_display()
            
            # 更新状态栏
            self.status_var.set(f"计算完成 | {history_entry}")
            
            # 清空输入框
            self.input_var.set("")
            self.entry.focus()
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的整数！")
            self.status_var.set("错误：输入格式无效")
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出现错误：{str(e)}")
            self.status_var.set(f"错误：{str(e)}")
    
    def clear_all(self):
        """清除所有输入和结果"""
        self.input_var.set("")
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("已清除 | 输入绝对值小于1,000,000,000的整数")
        self.entry.focus()
    
    def clear_history(self):
        """清除历史记录"""
        if messagebox.askyesno("确认", "确定要清除所有历史记录吗？"):
            self.history.clear()
            self.history_text.delete(1.0, tk.END)
            self.status_var.set("历史记录已清除")
    
    def update_history_display(self):
        """更新历史记录显示"""
        self.history_text.delete(1.0, tk.END)
        if not self.history:
            self.history_text.insert(1.0, "暂无历史记录")
        else:
            for i, entry in enumerate(reversed(self.history), 1):
                self.history_text.insert(tk.END, f"{i}. {entry}\n")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """数字转325计算公式 v3.0.0

一个将任意整数转换为包含数字3、2、5的数学表达式的小工具。

特性：
• 支持负整数
• 支持最多9位数
• 实时历史记录
• 友好的图形界面

算法原理：
将数字的每一位替换为等值的3、2、5表达式，
并通过(3+2+5)=10来实现数位对齐。

By Shichi Neko
2026"""
        messagebox.showinfo("关于", about_text)


def main():
    """主函数"""
    root = tk.Tk()
    app = NumberTo325Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()