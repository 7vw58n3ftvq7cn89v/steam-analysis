import tkinter as tk
from tkinter import *
import TreeCla

select_model = -1 #1是决策树，2是线性回归，3是神经网络

def get_text():
    global select_model
    tags = text1.get("1.0",END)
    # print(listbox1.get(listbox1.curselection()))
    dev = entry1.get()
    peak = entry2.get()
    good_rate = entry3.get()
    print(tags)
    print(dev)
    if select_model == 1:
        ans = TreeCla.ans(tags,dev)
    elif select_model == 2:
        """"""
        pass
    else:
        """"""
        pass
    label22['text'] = ans

def train():
    TreeCla.training()

def callback():
    print ("click me!")

def get_selected_value():
    global select_model
    select_model = v.get()
    # 通过get()方法获取IntVar变量的值
    print(v.get())

win = Tk()
win.title("steam游戏数据统计与预测")

win.geometry('1200x800')
# 创建一个文本控件
# width 一行可见的字符数；height 显示的行数
label1 = tk.Label(win, text="请输入游戏tag，以空格隔开: ",font=('宋体',15, 'bold italic')).place(x=100,y=0, width=400, height=20)
text1 = Text(win, width=500, height=5, undo=True, autoseparators=False)
# 适用 pack(fill=X) 可以设置文本域的填充模式。比如 X表示沿水平方向填充，Y表示沿垂直方向填充，BOTH表示沿水平、垂直方向填充
text1.place(x=180,y=50, width=200, height=30)

label2 = tk.Label(win, text="请选择游戏好评率: ",font=('宋体',15, 'bold italic')).place(x=180,y=100, width=200, height=20)
listbox1 =Listbox(win)
listbox1.place(x=180,y=150, width=200, height=200)

# i表示索引值，item 表示值，根据索引值的位置依次插入
for i,item in enumerate(['好评如潮','特别好评','好评','多半好评','褒贬不一','多半差评','特别差评','差评如潮','未知']):
    listbox1.insert(i,item)

label3 = tk.Label(win, text="请输入游戏发行商：",font=('宋体',15, 'bold italic')).place(x=90,y=370, width=400, height=20)
entry1 = tk.Entry(win)
# 放置输入框，并设置位置
entry1.place(x=180,y=400, width=200, height=20)
entry1.delete(0, "end")


label4 = tk.Label(win, text="请选择使用的模型类型：",font=('宋体',15, 'bold italic')).place(x=600,y=0, width=400, height=20)
site = [('决策树',1),
        ('线性回归',2),
        ('神经网络',3)]
# IntVar() 用于处理整数类型的变量
v = tk.IntVar()
# for name, num in site:
#     radio_button = tk.Radiobutton(win ,text = name, variable = v,value =num,indicatoron = False)
#     radio_button.place(x=680,y=30+30*i, width=200, height=20)
for i, name in enumerate(site):
    num = name[1]
    name = name[0]
    radio_button = tk.Radiobutton(win ,text = name, variable = v,value =num)
    radio_button.place(x=680,y=50+30*i, width=200, height=20)
v.trace_add("write", lambda name, index, mode, sv=v: get_selected_value())


label5 = tk.Label(win, text="请输入价格：",font=('宋体',15, 'bold italic')).place(x=600,y=200, width=400, height=20)
entry2 = tk.Entry(win)
# 放置输入框，并设置位置
entry2.place(x=680,y=230, width=200, height=20)
entry2.delete(0, "end")

label6 = tk.Label(win, text="请输入好评率：",font=('宋体',15, 'bold italic')).place(x=600,y=270, width=400, height=20)
entry3 = tk.Entry(win)
# 放置输入框，并设置位置
entry3.place(x=680,y=300, width=200, height=20)
entry3.delete(0, "end")


label22 = tk.Label(win, text="预测结果显示在这里",font=('宋体',15, 'bold italic'),
                 # 设置标签内容区大小
                 width=50,height=1,
                 # 设置填充区距离、边框宽度和其样式（凹陷式）
                 padx=30, pady=1, borderwidth=1, relief="sunken")

tk.Button(win, text="预训练", width=10, command=train).place(x=200,y=450, width=100, height=30)
tk.Button(win, text="预测结果", width=10, command=get_text).place(x=400,y=450, width=150, height=30)
label22.place(x=380,y=500, width=200, height=20)
# 使用按钮控件调用函数
# b = tk.Button(win, text="点击执行回调函数", command=callback).pack()
win.mainloop()