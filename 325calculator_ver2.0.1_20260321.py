# 最后编辑于2026/03/21 17:43 Ver2.0.2
# 修改了部分变量名称，修复了一些已知问题

print("输入一个数字，它能把任何数字变成325计算公式……")
while True:
    try:
        input_num = int(input("请输入一个绝对值小于1,000,000,000的整数："))
        if input_num >= 1000000000:
            print("我叫你输入绝对值小于1,000,000,000的一个整数，你尔多隆吗？") # 判断输入不合法并返回 
            continue
    except ValueError: 
        print("我叫你输入绝对值小于1,000,000,000的一个整数，你尔多隆吗？")  # 判断输入不合法并返回
    else:
        out_num1=out_num2=out_num3=out_num4=out_num5=out_num6=out_num7=out_num8=out_num9=None # 定义输出的每一位，防止未定义
        abs_input_num = abs(input_num)
        if input_num != 0:
            num9 = abs_input_num//100000000
            num8 = (abs_input_num%100000000)//10000000 # 得千万位
            num7 = (abs_input_num%10000000)//1000000  # 得百万位
            num6 = (abs_input_num%1000000)//100000  # 得十万位
            num5 = (abs_input_num%100000)//10000  # 得万位
            num4 =(abs_input_num%10000)//1000  # 得千位
            num3 = (abs_input_num%1000)//100  # 得百位
            num2 = (abs_input_num%100)//10  # 得十位
            num1 = abs_input_num%10  # 得个位
            mapping = {
                1:'(3*2-5)',
                2:'(3-2+5+3-2-5)',
                3:'(3+2+5+3-2*5)',
                4:'(-3+2+5)',
                5:'(3-2)*5',
                6:'(3-2+5)',
                7:'(-3+2*5)',
                8:'(3*2-5-3+2*5)',
                9:"3*(-2+5)"
            }        # 方便对应
            
            for i in range(1,10):        # 检验位上value合法性
                val = globals()[f'num{i}']        # 将i-1个10相乘改为(3+2+5)
                if val == 0:        # 判断每一位的value是否=0
                    globals()[f'out_num{i}'] = ''  # 是，输出None
                elif val in mapping:
                    if i == 1:        # 判断每一位的value是否=1
                        globals()[f'out_num{i}'] = mapping[val]        # 将i-1个(3+2+5)输出为None
                    else:
                         # mapping[v] 乘以 i-1 个 (3+2+5) 相乘
                        base = '(3+2+5)'
                        factors = [base] * (i-1)
                        globals()[f'out_num{i}'] = f"{mapping[val]} * " + ' * '.join(factors)        # 输出位数*(3+2+5)
            parts = [out_num9, out_num8, out_num7, out_num6, out_num5, out_num4, out_num3, out_num2, out_num1]        # 为方便表示而将其组成parts
            parts = [p for p in parts if p]        # 移除None
            if input_num > 0:
                print(input_num, "=", " + ".join(parts))         # 输出结果
            else:
                print(input_num, "= -", " + ".join(parts))         # 输出结果
        else:        # 判断input_num的Value为0
            print("3+2-5")  # 对0输出
        




# By Shichi Neko
        