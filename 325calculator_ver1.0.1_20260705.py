# 数字转325计算公式 
# 你猜开头为什么空三行

import tkinter as tk
from tkinter import messagebox, ttk
import time
import webbrowser


COLORS = {
    'bg_dark': '#f5f5f7', 'bg_medium': '#ffffff', 'bg_light': '#e8e8ec',
    'accent': '#e94560', 'accent_light': '#ff6b6b',
    'text_primary': '#2c3e50', 'text_secondary': '#7f8c8d',
    'success': '#27ae60', 'warning': '#f39c12', 'info': '#3498db',
    'entry_bg': '#ffffff', 'button_bg': '#f0f0f0',
    'scrollbar_bg': '#e8e8ec', 'scrollbar_thumb': '#c0c0d0',
}

DIGIT_EXPR = {
    1: '(3*2-5)', 2: '(3-2+5+3-2-5)', 3: '(3+2+5+3-2*5)',
    4: '(-3+2+5)', 5: '(3-2)*5', 6: '(3-2+5)',
    7: '(-3+2*5)', 8: '(3*2-5-3+2*5)', 9: '3*(-2+5)'
}
BASE10 = '(3+2+5)'

def number_to_325(num):
    if num == 0: return "3+2-5"
    neg, s = num < 0, str(abs(num))
    parts = [
        f"{DIGIT_EXPR[int(d)]}{' × ' + ' × '.join([BASE10]*pos) if pos else ''}"
        for pos, d in enumerate(reversed(s)) if d != '0'
    ]
    if not parts: return "0"
    expr = ' + '.join(reversed(parts))
    return f"-({expr})" if neg else expr

class ModernScrollbar(ttk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent)
        c = colors
        self.canvas = tk.Canvas(self, highlightthickness=0, width=8, bg=c['scrollbar_bg'])
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.thumb_id = None
        self.text_widget = None
        self._dragging = False
        self._drag_y = 0
        self._drag_scroll = 0.0
        self.canvas.bind('<Button-1>', self._on_click)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)

    def attach(self, text_widget):
        self.text_widget = text_widget
        text_widget.bind('<Configure>', lambda e: self._update())
        text_widget.bind('<MouseWheel>', self._on_mousewheel)
        self._update()

    def _update(self):
        if not self.text_widget or not self.canvas.winfo_exists(): return
        try:
            first = float(self.text_widget.index('@0,0').split('.')[0])
            last = float(self.text_widget.index(f'@0,{self.text_widget.winfo_height()}').split('.')[0])
            total = float(self.text_widget.index('end-1c').split('.')[0])
            visible = last - first
            if total <= visible or visible <= 0: self.canvas.delete('all'); return
            ch = self.canvas.winfo_height()
            thumb_h = max(30, visible / total * ch)
            thumb_y = first / total * (ch - thumb_h)
            self.canvas.delete('all')
            self.thumb_id = self.canvas.create_rectangle(
                2, thumb_y, self.canvas.winfo_width()-2, thumb_y+thumb_h,
                fill=self.colors['scrollbar_thumb'], outline='')
        except: pass

    def _on_click(self, event):
        if not self.thumb_id: return
        coords = self.canvas.coords(self.thumb_id)
        if coords and coords[1] <= event.y <= coords[3]:
            self._dragging = True; self._drag_y = event.y
            self._drag_scroll = float(self.text_widget.index('@0,0').split('.')[0])
            self.canvas.config(cursor='hand2')

    def _on_drag(self, event):
        if not self._dragging or not self.thumb_id: return
        try:
            ch = self.canvas.winfo_height()
            thumb_h = self.canvas.coords(self.thumb_id)[3] - self.canvas.coords(self.thumb_id)[1]
            delta = event.y - self._drag_y
            total = float(self.text_widget.index('end-1c').split('.')[0])
            if ch <= thumb_h: return
            ratio = delta / (ch - thumb_h)
            new_first = max(0, min(total-1, self._drag_scroll + ratio * total))
            self.text_widget.yview_moveto(new_first / total)
            self._update()
        except: pass

    def _on_release(self, event):
        self._dragging = False
        self.canvas.config(cursor='')

    def _on_mousewheel(self, event):
        if not self.text_widget: return
        delta = -1 * (event.delta // 120) if hasattr(event, 'delta') else -1 * event.num
        self.text_widget.yview_scroll(delta, 'units')
        self._update()

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("数字转325计算公式")
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"1000x800+{(sw-1000)//2}+{(sh-800)//2}")
        root.minsize(900, 700)
        c = COLORS
        root.configure(bg=c['bg_dark'])

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', background=c['accent'], foreground='white',
                        borderwidth=0, font=('微软雅黑', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', c['accent_light'])])
        style.configure('TButton', background=c['button_bg'], foreground=c['text_primary'],
                        borderwidth=1, font=('微软雅黑', 10))
        style.map('TButton', background=[('active', c['accent_light'])])
        style.configure('TEntry', fieldbackground=c['entry_bg'], foreground=c['text_primary'],
                        borderwidth=1, font=('Consolas', 11))
        style.configure('TLabelframe', background=c['bg_dark'], foreground=c['text_primary'],
                        bordercolor=c['accent'])
        style.configure('TLabelframe.Label', background=c['bg_dark'], foreground=c['accent'],
                        font=('微软雅黑', 11, 'bold'))

        # ----- 布局 -----
        top = tk.Frame(root, bg=c['bg_dark'])
        top.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=(15,0))

        hdr = tk.Frame(top, bg=c['bg_dark'])
        hdr.pack(fill=tk.X, pady=(0,10))
        tk.Label(hdr, text="✨ 数字转325计算公式 ✨", font=('微软雅黑', 20, 'bold'),
                 fg=c['accent'], bg=c['bg_dark']).pack(anchor='w')
        tk.Label(hdr, text="将任意整数转换为包含3、2、5的数学表达式",
                 font=('微软雅黑', 10), fg=c['text_secondary'], bg=c['bg_dark']).pack(anchor='w', pady=(5,0))
        tk.Frame(hdr, height=2, bg=c['accent']).pack(fill=tk.X, pady=(5,0))

        inp_frame = tk.Frame(top, bg=c['bg_dark'])
        inp_frame.pack(fill=tk.X, pady=(0,10))
        tk.Label(inp_frame, text="📝 输入数字", font=('微软雅黑', 12, 'bold'),
                 fg=c['text_primary'], bg=c['bg_dark']).pack(anchor='w')
        self.input_var = tk.StringVar()
        self.entry = ttk.Entry(inp_frame, textvariable=self.input_var, font=('Consolas', 12))
        self.entry.pack(fill=tk.X, ipady=8, pady=5)
        btn_row = tk.Frame(inp_frame, bg=c['bg_dark'])
        btn_row.pack(fill=tk.X, pady=(5,0))
        for text, cmd, accent in [("🔢 计算", self.calculate, True),
                                  ("🗑️ 清除", self.clear_all, False),
                                  ("📚 示例", self.show_examples, False),
                                  ("❓ 关于", self.show_about, False)]:
            ttk.Button(btn_row, text=text, command=cmd,
                       style='Accent.TButton' if accent else 'TButton').pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        res_lf = ttk.LabelFrame(top, text="📊 计算结果", padding=12)
        res_lf.pack(fill=tk.BOTH, expand=False)
        res_lf.configure(height=300)
        res_lf.pack_propagate(False)
        self.result_text = tk.Text(res_lf, font=('Consolas', 11),
                                   bg=c['bg_medium'], fg=c['text_primary'],
                                   wrap=tk.WORD, relief='flat', borderwidth=0, padx=8, pady=8)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.result_scroll = ModernScrollbar(res_lf, c)
        self.result_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(2,0))
        self.result_scroll.attach(self.result_text)
        ttk.Button(res_lf, text="📋 复制结果", command=self.copy_result).pack(anchor='e', pady=(5,0))
        self.result_text.tag_configure('title', font=('Consolas', 12, 'bold'), foreground=c['accent'])
        self.result_text.tag_configure('highlight', foreground=c['success'])
        self.result_text.tag_configure('info', foreground=c['info'])

        hist_frame = tk.Frame(root, bg=c['bg_dark'], height=180)
        hist_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=15, pady=(10,15))
        hist_frame.pack_propagate(False)
        hist_lf = ttk.LabelFrame(hist_frame, text="📜 历史记录 (最近10条)", padding=12)
        hist_lf.pack(fill=tk.BOTH, expand=True)
        self.history_text = tk.Text(hist_lf, font=('Consolas', 10),
                                    bg=c['bg_medium'], fg=c['text_secondary'],
                                    wrap=tk.WORD, relief='flat', borderwidth=0, padx=8, pady=8)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.hist_scroll = ModernScrollbar(hist_lf, c)
        self.hist_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(2,0))
        self.hist_scroll.attach(self.history_text)
        ttk.Button(hist_lf, text="🗑️ 清空历史", command=self.clear_history).pack(anchor='e', pady=(5,0))
        self.history_text.insert('1.0', "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录")

        footer = tk.Frame(root, bg=c['bg_medium'], height=35)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        footer.pack_propagate(False)
        self.status_var = tk.StringVar(value="✨ 就绪 | 输入任意整数开始转换")
        tk.Label(footer, textvariable=self.status_var, font=('微软雅黑', 9),
                 fg=c['text_secondary'], bg=c['bg_medium']).pack(side=tk.LEFT, padx=10)
        self.time_var = tk.StringVar()
        tk.Label(footer, textvariable=self.time_var, font=('Consolas', 9),
                 fg=c['text_secondary'], bg=c['bg_medium']).pack(side=tk.RIGHT, padx=10)

        self.history = []
        root.bind('<Control-c>', lambda e: self.copy_result())
        root.bind('<Control-h>', lambda e: self.clear_history())
        root.bind('<Return>', lambda e: self.calculate())
        root.bind('<Escape>', lambda e: self.clear_all())
        self.entry.focus()
        self._tick()

    def _tick(self):
        self.time_var.set(f"🕐 {time.strftime('%H:%M:%S')}")
        self.root.after(1000, self._tick)

    def calculate(self):
        inp = self.input_var.get().strip()
        if not inp: self.status_var.set("⚠️ 请输入数字"); return
        try: num = int(inp)
        except ValueError: messagebox.showerror("错误", "请输入有效整数"); self.status_var.set("❌ 格式错误"); return
        if len(inp) > 100 and not messagebox.askyesno("确认", f"输入长度 {len(inp)}，可能较慢，继续？"): return
        if inp == "325": messagebox.showinfo("325", "苦也，这也言周!")
        result = number_to_325(num)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('end', "🎯 转换结果\n", 'title')
        self.result_text.insert('end', "─" * 60 + "\n")
        self.result_text.insert('end', f"{num} = {result}\n\n", 'highlight')
        self.result_text.insert('end', f"📊 位数: {len(str(abs(num)))} | 表达式长度: {len(result)}\n", 'info')
        self.history.append(f"{num} = {result}")
        if len(self.history) > 10: self.history.pop(0)
        self._update_history()
        self.status_var.set(f"✅ 计算完成 | {len(str(abs(num)))}位数")
        self.input_var.set("")
        self.entry.focus()

    def _update_history(self):
        self.history_text.delete('1.0', tk.END)
        if not self.history:
            self.history_text.insert('1.0', "暂无历史记录\n\n💡 提示：计算结果会自动添加到历史记录")
        else:
            for i, item in enumerate(reversed(self.history), 1):
                self.history_text.insert('end', f"{i:2d}. {item[:100]}\n")
        self.hist_scroll._update()

    def copy_result(self):
        content = self.result_text.get('1.0', 'end-1c').strip()
        if content:
            self.root.clipboard_clear(); self.root.clipboard_append(content)
            self.status_var.set("📋 已复制")

    def clear_all(self):
        self.input_var.set(""); self.result_text.delete('1.0', tk.END)
        self.entry.focus(); self.status_var.set("✨ 已清除")

    def clear_history(self):
        if messagebox.askyesno("确认", "清空所有历史记录？"):
            self.history.clear(); self._update_history()
            self.status_var.set("🗑️ 历史记录已清除")

    def show_examples(self):
        messagebox.showinfo("示例",
            "• 0  → 3+2-5\n• 1  → (3*2-5)\n• 10 → (3*2-5) × (3+2+5)\n"
            "• -5 → -((3-2)*5)\n\n快捷键:\nEnter 计算  Esc 清除\nCtrl+C 复制  Ctrl+H 清空历史")

    def show_about(self):
        if messagebox.askyesno("关于", "数字转325计算公式 v6.4.1 Lite\n开发者：Ichifuyu\n是否查看项目仓库地址？"):
            webbrowser.open("https://github.com/Cudny10D/325_Calculator")

if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


#                                           ..        .....           .--.                           
#                                      ......            ........      ...:-:                        
#                                    .....      .          ...........    . .--.                     
#                                    ....     ......      ..............      .::                    
#                                  .....    .....              ..........       .::                  
#                                   ...   ......              ......::......                         
#                                   ...  ......          ..........:::::...:..                       
#                                    ...  .......        ............:..::....                       
#                                    ....                ......::::::.....:...                       
#                                ....::::..              .....:::...:......::..     ..               
#                             .::--------::..        .... ..:..:::..........:....    ..              
#                            ::--======---::.................::::::..........:....     .             
#                          .:--==========--::::::.....:..::...::..::..  ...........                  
#                          .:-=====++====-----::::::::::::::....:..:..   ...:.......                 
#                         .:-==--==+++++=====-:::::::::::::::....:..:..  ............    .           
#              .         .::-==++++=++++======-----::::::::.........:... ....:........               
#             ....      ..     .:=+++++++======-----::::::.....  ....:..  ............               
#            .....     ..  ..   ..:=++++++======-----::::::....  ....:::. ...:..:....                
#            .....     .::-==-:....:-=++++++=====------:::::...   ...::.. ...:..:....                
#           ......    .::-=====-:..::-=++++=====-----:::::::....  ...::.. ...:::.....                
#          ... ...   .:::-==++==-::::-==+++===---:::....  ......  ...:::....::... ..                 
#          ..       .::......:=+=--:::--======----:::....   ...   ...:::..:.....                     
#          ..       ::::.::===++----::::-----------:::::::.....   ...:::......      .........        
#                .:.  :::....  -+---::::-------------:-:::::.........::...         ...:::..-.        
#               ::.  .-----..::-+=-=--:-====---:::::-------:.............         .:.:-:--::         
#               -:. .-------==++=-====-=+**+==--:::.:::::......... .....          ..:--:--:          
#               -=:..-====--====++-:===+*#**++=--::-.  :--:.        ...          ...----::   .       
#               .=:..-=======++++++.====----:-==----:. .::..         .           ..::--::.  :.       
#                ==::--===+++++++==::=**#*+:+*++=------:::.                       .::::..  :.        
#                .*#=:--====+++==-:.=+###+-::=++==--:::::.                        ......  .:.        
#                 .:=+----=====--::=*####*-:.=++==---::.   ..                     .....  ...         
#                  ....:-==--==-:=+**##%##=..-=====--:. .....      .                     .           
#                   ....::::----=+***#####+--====--:.. ..... ..   ...                                
#                    ...:::--::.:=++***##**-:===--:......:.. .   .....                               
#                    ..::----:...:-======++=:--*=:. ...:::.. .  .:......                             
#           ..::::.. ...:----::....:::...:----::....::--::..    .:......                             
#    .::-------------:...:----:::::----:::-=--:.. ..::::::..    .......                              
#  :-----------------:....:----=====+========::..::::::::::.    ....:.              ..:::..          
# :--------------::::::.....:=+**++***++++===--:---:::::::::.   .....             .-=====++===:.     
# -----------:::::..    ......:=+*****++++===-------:::::::::... ...      ..      .-====+++++++++=-. 
# -------:::::.         .....    ..-=++++====---:     .::::.             ..             :=+++++++++=:
# -----:::.             ......       .:---------  :::.  ::. .:::.       .:.        -+++  -+++++++++==
# ---::.    .::......  .....::.         ::------ .=+++=  .. -+++:       .=++=:     -+++  -+++++++++==
# :...:-===-:.::::..    ...::::..    ::--------- .=+++++    -+++:            :-:-  -+++  :==+++++++==
# =+++=-:::----:......  ...:---:::::-======----- .=++++++:  -+++:   -+++++++:  +#  -+++  +#*++=======
# -..-=++++=:.:---::... ....--==---:==---====--- .=++--+++- -+++:  ++++= -+++=  :  -+++  =**+++**###*
# ***++-:::-===-:..      ....:-----------------: .=++- =+++==+++: :++++   -+++- +  :+++  =*##%%%%##**
# :::-++++++=-.          .:.....::::::---------: .=++-  .+++++++: =+++-   -+++- .  :+++  +##*+=--=+*#
# ###**+=-...             .:..:::---=======----: .=++-   .++++++: .++++   -+++- .       .+*#%%%%%##*+
# +-::.......               .:::---=====---:::.. .=++-  : .=++++:  -++++=++++=  :  -+++. .::::-=+*##%
# ...........                  .:::::::..     .. .=++-  ::  =+++:    =+++++=   ::  -+++. .:::::::::::
# ............                              ....       ....                  ::::.       ....::::::::
# ...............                             ...:=-=+==:.....      ......:::::::::::......::::::::..
# :...............                              .::---:..             ...::::::::.........::::::::...