from microbit import *
import random
import gc
gc.enable()
gc.collect()



di = 0#direction
darr = [[0,-1],[1,0],[0,1],[-1,0]]#move dir
diarr = [[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]]#rendering maze's dir
dirarr = [[4,0],[4,1],[4,2],[4,3],[4,4],[3,4],[2,4],[1,4],[0,4],[0,3],[0,2],[0,1],[0,0],[1,0],[2,0],[3,0]]#rendering Direction indicator
maze = []
mazesize = 0
level = 0
lightlevel = []


def generatemaze(lx,ly):#maze generates
    global px, py#player coordinate
    px = 1
    py = 1
    maze = []
    for x in range(lx):
        a = []
        for y in range(ly):
            if x % 2 == 0 or y % 2 == 0:
                a.append(1)  # 1 means wall
            else:
                a.append(0)  # 0 means channel
        maze.append(a)
    a, b = [], []
    a.append([1, 1])
    b.append([2, 1, 1, 0])
    b.append([1, 2, 0, 1])
    c = [0, 1, 0, -1]
    d = [1, 0, -1, 0]

    while True:
        i = b[random.randint(0, len(b) - 1)]
        if a.count([i[0] + i[2], i[1] + i[3]]) == 0:
            a.append([i[0] + i[2], i[1] + i[3]])
            b.remove(i)
            maze[i[0]][i[1]] = 0  # Open up walls to create passages
            for e in range(4):
                f = [i[0] + i[2] + c[e], i[1] + i[3] + d[e]]
                if f[0] <= lx - 2 and f[0] >= 1 and f[1] <= ly - 2 and f[1] >= 1:
                    if maze[i[0] + i[2] + c[e]][i[1] + i[3] + d[e]] == 1:
                        b.append([i[0] + i[2] + c[e], i[1] + i[3] + d[e], c[e], d[e]])

        for x in range(lx):
            for y in range(ly):
                if a.count([x, y]) > 1:
                    a.remove([x, y])

        if len(a) == ((lx - 1) / 2) * ((ly - 1) / 2):
            maze[1][1] = 2  # start
            maze[lx - 2][ly - 2] = 3  # end
            return maze


def show():
    for i in range(8):#rendering maze from 1,1 to 3,3 on the board
        if maze[py+diarr[i][1]][px+diarr[i][0]] == 1:
            display.set_pixel(2+diarr[i-2*di][0],2+diarr[i-2*di][1],6)
        elif maze[py+diarr[i][1]][px+diarr[i][0]] == 2 or maze[py+diarr[i][1]][px+diarr[i][0]] == 3:
            display.set_pixel(2+diarr[i-2*di][0],2+diarr[i-2*di][1],3)
        else:
            display.set_pixel(2+diarr[i-2*di][0],2+diarr[i-2*di][1],0)
    display.set_pixel(2,2,9)

def move():#according to dir to change player coordinate
    global px,py
    if maze[py+darr[di][1]][px+darr[di][0]] != 1:
        py += darr[di][1]
        px += darr[di][0]
    if maze[py][px] == 3:
        return 1
    return 0


def showdir():#rendering Direction indicator which point to the end
    
    if py > px:#the brighter always render on top
        for i in range(16):
            if i < 5:
                display.set_pixel(dirarr[i-di*4][0],dirarr[i-di*4][1],int((mazesize-2-px)/lightlevel[level]))
            elif i < 9:
                display.set_pixel(dirarr[i-di*4][0],dirarr[i-di*4][1],int((mazesize-2-py)/lightlevel[level]))
            else:
                display.set_pixel(dirarr[i-di*4][0],dirarr[i-di*4][1],0)
    else:
        for i in range(8,-8,-1):
            if i > 3:
                display.set_pixel(dirarr[i-di*4][0],dirarr[i-di*4][1],int((mazesize-2-py)/lightlevel[level]))
            elif i>=0:
                display.set_pixel(dirarr[i-di*4][0],dirarr[i-di*4][1],int((mazesize-2-px)/lightlevel[level]))
            else:
                display.set_pixel(dirarr[(i-di*4)%16][0],dirarr[(i-di*4)%16][1],0)


display.scroll('MAZE',50)
display.scroll('CHOOSE LEVEL',100)
levellist = [5,9,13,17,21]
lightlevel = [0.21,0.61,1.01,1.41,1.81]
display.show('1')


while 1:# choose level
    if button_a.is_pressed() and button_b.is_pressed():
        break
    else:
        if button_b.was_pressed():
            level = (level+1)%5
            display.clear()
            sleep(300)
            display.show(str(level+1))
        if button_a.was_pressed():
            level = (level-1)%5
            display.clear()
            sleep(300)
            display.show(str(level+1))  


mazesize = levellist[level]#go to levellist to take size 
display.scroll(str(mazesize)+'^2 ',100)#tell player mazesize


display.scroll('LOADING... ',100)
maze = generatemaze(mazesize,mazesize)#generating maze


for i in maze:#it's only used for debugging has no other effect
    for e in i:
        if e == 1:
            print('▮',end = '')
        else:
            print(' ',end = '')
    print()


display.clear()
playtime = running_time()


#game start
show()
showdir()
while 1:
    if button_a.is_pressed() and button_b.is_pressed():#move forward
        if move():
            break
        show()
        showdir()
    else:
        if button_a.was_pressed():#turn left
            di = (di-1)%4
            show()
            showdir()
        if button_b.was_pressed():#turn right
            di = (di+1)%4
            show()
            showdir()
#end


display.clear()
playtime = (running_time() - playtime)//1000
display.scroll('TIME:'+str(playtime//60)+' min '+str(playtime%60)+' s',150,loop=1)