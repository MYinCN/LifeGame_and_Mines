import tkinter
import tkinter.messagebox
import time
from random import randint
# ======================================================
# 设定参数
RUNNING = [False, -1]   # 运行状态设置。True为运行中，False为暂停中。第二个变量为游戏进行时间。-1为未开始。
x_size, y_size = 9, 9  # x，y轴棋盘点个数
safes = [0, 0]   # 安全点数量，[未找到的，已找到的]
num_mines = [y_size]   # 设置多少个雷，由难度决定
mines = []  # 储存所有雷的位置的列表
# 设定常数
MINE = 1
SAFE = 0
UNKNOWN = 0
KNOWN = 1
COLOR = {0:'#FAEBD7', 1:'#FFE4B5', 2:'#F0E68C',
         3:'#FFFF00' , 4:'#F4A460', 5:'#FFA500',
         6:'#FF4500', 7:'#FF0000', 8:'#A52A2A'}  # 颜色列表
# ======================================================
def findNeighbour(x, y):
    visited = []
    border = []
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    ps = [(x, y)]
    while ps:
        nextRound = []
        for p in ps:
            visited.append(p)
            for d in dirs:
                x1 = p[0] + d[0]
                y1 = p[1] + d[1]
                if (x1, y1) not in visited and (x1, y1) not in nextRound and (x1, y1) not in border:
                    if 0 <= x1 < x_size and 0 <= y1 < y_size:
                        if buttons[y1][x1].state == UNKNOWN and buttons[y1][x1].surround == 0:
                            nextRound.append((x1, y1))
                        elif buttons[y1][x1].state == UNKNOWN and buttons[y1][x1].surround > 0:
                            border.append((x1, y1))
        ps = nextRound
    return visited + border


class customButton(object):
# 自定义按钮类，每一个按钮放在一个格子中，作为一个生命单元，便于储存类一些状态变量，包括：
# xpos, ypox: 按钮的位置
# state: 当前按钮的生存状态
# bt: 当前按钮的Button实例，由tkinter.Button生成
    def __init__(self, master, x, y):
        self.xpos = x
        self.ypos = y
        self.state = UNKNOWN
        self.inside = SAFE
        self.surround = 0
        self.bt = tkinter.Button(master, bg=COLOR[randint(0,8)], height=1, width=3,
                                 command=self.valueDefine, text=' ', fg='black')

# 自定义函数valueDefine，用于判断按键时调用什么方法。
# 本质是调用changeColor函数，但是加了层判断让游戏运行时不能通过点击按钮调用changeColor
    def valueDefine(self):
        if RUNNING[0] == False or self.state == KNOWN:
            return
        else:
            if tagButton['bg'] == 'red':
                self.mineTag()
            else:
                self.changeColor()

    def mineTag(self):
        if self.state == UNKNOWN:
            if self.bt['text'] == ' ':
                self.bt['text'] = 'X'
                self.bt['fg'] = 'red'
            elif self.bt['text'] == 'X':
                self.bt['text'] = '?'
                self.bt['fg'] = 'yellow'
            elif self.bt['text'] == '?':
                self.bt['text'] = ' '
                self.bt['fg'] = 'black'

        # 自定义函数changeColor。进行挖雷操作，同时改变颜色。
    def changeColor(self):
        if self.inside == MINE:
            self.state = KNOWN
            self.bt['bg'] = 'red'
            self.bt['text'] = '@'
            self.bt['fg'] = 'yellow'
            for pos in mines:
                buttons[pos[1]][pos[0]].bt['bg'] = 'RED'
                buttons[pos[1]][pos[0]].bt['text'] = '@'
                buttons[pos[1]][pos[0]].bt['fg'] = 'yellow'
            stopGame()
            if safes[1] > 3:
                tkinter.messagebox.showinfo('游戏结束','任务失败')
            else:
                tkinter.messagebox.showinfo('游戏结束', '你真乃踩雷大师也')

        else:
            if self.surround == 0:
                tmp = findNeighbour(self.xpos, self.ypos)
                for p in tmp:
                    buttons[p[1]][p[0]].bt['bg'] = COLOR[buttons[p[1]][p[0]].surround]
                    buttons[p[1]][p[0]].bt['text'] = str(buttons[p[1]][p[0]].surround)
                    buttons[p[1]][p[0]].bt['fg'] = 'black'
                    buttons[p[1]][p[0]].state = KNOWN

                safes[0] -= len(tmp)
                safes[1] += len(tmp)
            else:
                self.bt['bg'] = COLOR[self.surround]
                self.bt['text'] = str(self.surround)
                self.bt['fg'] = 'black'
                self.state = KNOWN
                safes[0] -= 1
                safes[1] += 1

            if hintButton['text'] == 'HINT' and safes[0] < 5:
                hintButton['text'] = 'No'
                hintButton['bg'] = 'gray'

            if safes[0] <= 0:
                for pos in mines:
                    buttons[pos[1]][pos[0]].bt['bg'] = '#0000FF'
                    buttons[pos[1]][pos[0]].bt['text'] = '@'
                    buttons[pos[1]][pos[0]].bt['fg'] = 'red'
                tmp = time['text']
                stopGame()
                tkinter.messagebox.showinfo('游戏结束', f'你厉害，雷都被排空了，共用时{tmp}秒。')

top = tkinter.Tk()
top.title('扫雷')
width = str(x_size * 30)
top.geometry('x'.join([str(x_size * 36 + 56),str(y_size * 36 + 120)]))

# 生成网格上所有数组
buttons = []
for y in range(y_size):
    row = []
    for x in range(x_size):
        tmp = customButton(top, x, y)
        tmp.bt.grid(row=y, column=x, padx=1, pady=1)
        row.append(tmp)
    buttons.append(row)

# 开始游戏
def startGame():
    RUNNING[0] = True
    RUNNING[1] = -1
    safes[0] = x_size * y_size - num_mines[0]
    safes[1] = 0
    startButton['text'] = 'Restart'
    startButton['bg'] = 'white'
    time['text'] = '0'
    hintButton['bg'] = '#7FFFD4'
    hintButton['text'] = 'HINT'
    tagButton['bg'] = '#7FFFD4'

    # 计时器模块，用after函数控制每1000ms调用一次timing自身。
    def timing():
        if RUNNING[0] == True:
            time['text'] = str(RUNNING[1] + 1)
            RUNNING[1] += 1
            top.update()
            top.after(1000, timing)
    timing()

    # 初始化按钮状态
    for j in range(y_size):
        for i in range(x_size):
            buttons[j][i].bt['bg'] = '#778899'
            buttons[j][i].bt['text'] = ' '
            buttons[j][i].bt['fg'] = 'black'
            buttons[j][i].state = UNKNOWN
            buttons[j][i].inside = SAFE

    # 随机生成地雷，埋在按钮内
    mines.clear()
    for k in range(num_mines[0]):
        while True:
            x = randint(0, x_size-1)
            y = randint(0, y_size-1)
            if buttons[y][x].inside == SAFE:
                buttons[y][x].inside = MINE
                mines.append((x,y))
                break

    # 数当前代周围有多少雷，记录在每个按钮实例内
    dirs = [(1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)]
    for j in range(y_size):
        for i in range(x_size):
            buttons[j][i].state = UNKNOWN
            cnum = 0
            for d in dirs:
                x1 = i + d[0]
                y1 = j + d[1]
                if 0 <= x1 < x_size and 0 <= y1 < y_size:
                    if buttons[y1][x1].inside == MINE:
                        cnum += 1
            buttons[j][i].surround = cnum

# 结束游戏的函数。
def stopGame():
    startButton['bg'] = 'green'
    RUNNING[0] = False
    return

# 添加控制按钮，开始、提示、添加标记
startButton = tkinter.Button(top, height=1, width=6, text='START', command=startGame, bg='green')
startButton.grid(row=y_size+1, column=1, columnspan=2)

def hint():
    if RUNNING[0] == False or hintButton['text'] != 'HINT':
        return
    while True:
        x = randint(0, x_size-1)
        y = randint(0, y_size-1)
        if (x, y) not in mines and buttons[y][x].state == UNKNOWN:
            buttons[y][x].bt['bg'] = '#00FF7F'
            buttons[y][x].bt['text'] = 'ok'
            hintButton['text'] = 'USED'
            hintButton['bg'] = 'gray'
            break

hintButton = tkinter.Button(top, height=1, width=6, text='HINT', command=hint, bg='#7FFFD4')
hintButton.grid(row=y_size+1, column=7, columnspan=2)

def tagNote():
    if RUNNING[0] == False:
        return
    if tagButton['bg'] == '#7FFFD4':
        tagButton['bg'] = 'red'
        top.config(cursor="spraycan")
        cautionTag1['text'] = '标'
        cautionTag2['text'] = '记'
        cautionTag3['text'] = '中'
    else:
        tagButton['bg'] = '#7FFFD4'
        top.config(cursor="arrow")
        cautionTag1['text'] = ''
        cautionTag2['text'] = ''
        cautionTag3['text'] = ''
tagButton = tkinter.Button(top, height=1, width=6, text='TAG', command=tagNote, bg='#7FFFD4')
tagButton.grid(row=y_size+2, column=7, columnspan=2)


timeTag = tkinter.Label(top, text='TIME:')
timeTag.grid(row=y_size+2, column=0, columnspan=2, sticky='E')
time = tkinter.Label(top, text='0')
time.grid(row=y_size+2, column=2, columnspan=1, sticky='W')
timeTag = tkinter.Label(top, text='雷个数')
timeTag.grid(row=y_size+2, column=4, columnspan=2, sticky='W')

cautionTag1 = tkinter.Label(top, text='', fg='red')
cautionTag1.grid(row=3, column=x_size, sticky='W')
cautionTag2 = tkinter.Label(top, text='', fg='red')
cautionTag2.grid(row=4, column=x_size, sticky='W')
cautionTag3 = tkinter.Label(top, text='', fg='red')
cautionTag3.grid(row=5, column=x_size, sticky='W')
# ======================================================
# 游戏难度设置部分，用scale模块实现。scale的command似乎自动传入当前值
def getDiff(x):
    num_mines[0] = int(x)

diff = tkinter.Scale(top, from_=y_size//2, to=x_size*y_size//3,
                      orient=tkinter.HORIZONTAL, length=120, showvalue=1, resolution=1,
                      command=getDiff)
diff.set(num_mines[0])
diff.grid(row=y_size+1, column=3, columnspan=4)

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