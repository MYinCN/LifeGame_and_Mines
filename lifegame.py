import tkinter
import tkinter.messagebox
import time
# ======================================================
# 设定参数
RUNNING = [False]   # 运行状态设置。True为运行中，False为暂停中。
wait_time = [1.0]   # 刷新等待时间，控制游戏速度。采用列表储存是为了方便子函数修改。
x_size, y_size = 11, 11  # x，y轴棋盘点个数
# 设定常数
DEAD = -1
KEEP = 0
LIVE = 1
# ======================================================
# 制定规则：下方二维矩阵表示周围生命个数时的存活数
# 第j行表示祖父代周围的生命个数。(如果祖父代不影响，则将每一行都设置为一样的规则)
# 第i列表示父代周围的生命个数
# rule[j][i]就表示祖父代周围有j个生命，父代周围有i个生命时，当代的变化规则
# 其中:
# 0: 维持现状
# 1: 维持生命或生命复活
# -1: 维持死亡或生命死去
row = [DEAD, DEAD, KEEP, LIVE, LIVE, DEAD, DEAD, DEAD, DEAD]
rule = [row for j in range(9)]
# ======================================================
class customButton(object):
# 自定义按钮类，每一个按钮放在一个格子中，作为一个生命单元，便于储存类一些状态变量，包括：
# xpos, ypox: 按钮的位置
# state: 当前按钮的生存状态
# bt: 当前按钮的Button实例，由tkinter.Button生成
    def __init__(self, master, x, y):
        self.xpos = x
        self.ypos = y
        self.state = DEAD
        self.bt = tkinter.Button(master, bg='grey', height=1, width=3, command=self.valueDefine)

# 自定义函数valueDefine，用于停止游戏时改变按钮状态。
# 本质是调用changeColor函数，但是加了层判断让游戏运行时不能通过点击按钮调用changeColor
# （游戏自己运行过程中需要直接调用changeColor，不经过valueDefine判断）
    def valueDefine(self):
        if RUNNING[0] == True:
            return
        else:
            self.changeColor()

# 自定义函数changeColor。
# 其实是改变当前按钮的生存状态，同时改变颜色。
    def changeColor(self):
        if self.state == DEAD:
            self.bt['bg'] = 'red'
            self.state = LIVE
        else:
            self.bt['bg'] = 'grey'
            self.state = DEAD

top = tkinter.Tk()
top.title('生命游戏')
width = str(x_size * 30)
top.geometry('x'.join([str(x_size * 32 + 16),str(y_size * 32 + 80)]))

# 生成网格上所有数组
buttons = []
for y in range(1, y_size+1):
    row = []
    for x in range(1, x_size+1):
        tmp = customButton(top, x, y)
        tmp.bt.grid(row=y, column=x, padx=1, pady=1)
        row.append(tmp)
    buttons.append(row)

# 开始游戏
def startGame():
    # 先读取初始值，赋值给祖父代和父代
    RUNNING[0] = True
    startButton['bg'] = 'white'
    stopButton['bg'] = 'red'
    gfGen = [[buttons[j][i].state for i in range(x_size)] for j in range(y_size)]
    faGen = [[buttons[j][i].state for i in range(x_size)] for j in range(y_size)]

    dirs = [(1,0), (1,1), (0,1), (-1,1),
            (-1,0), (-1,-1), (0,-1), (1,-1)]
    while RUNNING[0]:  # 判断是否继续运行。如果RUNNING[0]被StopGame函数修改，则停止游戏
        # 对每个格子，数它周围在父代和祖父代分别有有多少存活的单元
        for j in range(y_size):
            for i in range(x_size):
                gnum = 0   # 祖父代存活个数
                fnum = 0   # 父代存活个数
                for d in dirs:
                    x1 = i + d[0]
                    y1 = j + d[1]
                    if 0 <= x1 < x_size and 0 <= y1 < y_size:
                        if gfGen[y1][x1] == LIVE:
                            gnum += 1
                        if faGen[y1][x1] == LIVE:
                            fnum += 1

                trans = rule[gnum][fnum]   # 根据规则，判定是否要改变生存状态
                if ((trans == LIVE and buttons[j][i].state == DEAD) or
                    (trans == DEAD and buttons[j][i].state == LIVE)
                ):
                    buttons[j][i].changeColor()

        # 数当前代周围有多少存活单元，显示在按钮上
        for j in range(y_size):
            for i in range(x_size):
                cnum = 0
                for d in dirs:
                    x1 = i + d[0]
                    y1 = j + d[1]
                    if 0 <= x1 < x_size and 0 <= y1 < y_size:
                        if buttons[y1][x1].state == LIVE:
                            cnum += 1
                buttons[j][i].bt['text'] = str(cnum)

        # 判断是否进入稳定态，将当前代状态存入父代，父代状态存入祖父代
        # 如果没有哪个网格祖父代、父代、和当前代有变化，则判断进入稳定态
        diff = False
        for j in range(y_size):
            for i in range(x_size):
                if diff == False:
                    if not (gfGen[j][i] == faGen[j][i] and faGen[j][i] == buttons[j][i].state):
                        diff = True
                gfGen[j][i] = faGen[j][i]
                faGen[j][i] = buttons[j][i].state
        top.update()

        if diff == False:  # 进入稳定态，则停止游戏
            tkinter.messagebox.showinfo('','进入稳定状态')
            startButton['bg'] = 'green'
            stopButton['bg'] = 'white'
            RUNNING[0] = False
            return

        # 继续进行游戏，通过间隔控制速度
        time.sleep(wait_time[0])

# 结束游戏的函数。
def stopGame():
    startButton['bg'] = 'green'
    stopButton['bg'] = 'white'
    RUNNING[0] = False
    return

# 添加控制按钮，开始、停止、清空
startButton = tkinter.Button(top, height=1, width=6, text='START', command=startGame, bg='green')
startButton.grid(row=y_size+1, column=1, columnspan=2)

stopButton = tkinter.Button(top, height=1, width=6, text='Stop', command=stopGame, bg='white')
stopButton.grid(row=y_size+2, column=1, columnspan=2)

# 自定义函数，清除整个棋盘
def clearMap():
    if RUNNING[0] == True:
        return

    for j in range(y_size):
        for i in range(x_size):
            if buttons[j][i].state == LIVE:
                buttons[j][i].changeColor()
            buttons[j][i].bt['text'] = ''

clearButton = tkinter.Button(top, height=1, width=6, text='Clear', command=clearMap, bg='white')
clearButton.grid(row=y_size+1, column=7, columnspan=2)


# ======================================================
# 游戏速度设置部分，用scale模块实现。scale的command似乎自动传入当前值
def getSpeed(x):
    wait_time[0] = float(x)

speed = tkinter.Scale(top, label='Fast <-> Slow', from_=0.1, to=2.1, orient=tkinter.HORIZONTAL,
                      length=90, showvalue=0, resolution=0.2, command=getSpeed)
speed.set(1.0)
speed.grid(row=y_size+1, column=3, columnspan=3)

### 下面几行是用listbox来设置速度, 不是很好
# listVar = tkinter.StringVar()
# listVar.set((0.5,1,2))
# def getSpeed():
#     wait_time[0] = speedChoice.get(speedChoice.curselection())
#     print(wait_time[0])
#
# speedChoice = tkinter.Listbox(top, listvariable=listVar)
# speedChoice.grid(row=y_size+1, column=3, columnspan=5)

# ======================================================
# 开始游戏循环
top.mainloop()