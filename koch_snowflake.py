from math import sqrt
from copy import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.widgets import Button

class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

class LinkedList(object):
    def __init__(self, head=None):
        self.head = Node(next_node = head) 
        self.size = 0

    @staticmethod
    def from_list(ll):
        res = LinkedList()
        for i in ll[::-1]:
            res.insert(i)
        res.size = len(ll)
        return res

    def insert(self, data):
        new_node = Node(data, self.head.get_next())
        self.head.set_next(new_node)
        self.size += 1

    class Cursor(object):
        def __init__(self, node, li):
            self.curr = node
            self.parent = li

        def next(self):
            if self.curr.get_next() is not None:
                self.curr = self.curr.get_next()
                return self.curr.get_data()
            else:
                return None

        def get(self):
            if self.curr.get_next():
                return self.curr.get_next().get_data()
            else:
                return None

        def insert(self, data):
            new_node = Node(data, self.curr.get_next())
            self.curr.set_next(new_node)
            self.parent.size += 1

    def cursor(self):
        return self.Cursor(self.head, self)

    def as_list(self):
        res = []
        cur = self.cursor()
        while True:
            x = cur.next()
            if x is not None:
                res.append(x)
            else:
                break
        return res

    def __len__(self):
        return self.size

    def __iter__(self):
        cur = self.head
        while cur.get_next() is not None:
            cur = cur.get_next()
            yield cur.get_data()
    
SIN60 = sqrt(3) / 2
xdata = LinkedList.from_list([0, -SIN60, SIN60, 0])
ydata = LinkedList.from_list([1, -0.25, -0.25, 1])
adata = LinkedList.from_list([2, 1, 0])
SIGNS = [[1,1],[-1,-1],[-1,1],[-1,-1],[1,1],[1,-1]]
idx = -1
jump = 1

def paint(i):
    global xdata, ydata, adata, idx, jump
    if i % jump != jump - 1:
        return 
    idx += 1
    if idx >= 8:
        return 
    print(idx)

    xcur = xdata.cursor()
    ycur = ydata.cursor()
    acur = adata.cursor()
    x1, x2 = None, xcur.next(); xxcur = copy(xcur)
    y1, y2 = None, ycur.next(); yycur = copy(ycur)
    while True:
        x1, x2 = x2, xcur.next();
        y1, y2 = y2, ycur.next();
        a = acur.next()
        if x2 is None:
            break
        xvec = x2 - x1
        yvec = y2 - y1

        xxcur.insert(x1 + 2*xvec/3)
        yycur.insert(y1 + 2*yvec/3)
        acur.insert(a)
        acur.insert((a - 2 + 3) % 3 + (3 if a < 3 else 0))
        xxcur.insert(x1 + xvec/2 + abs(yvec*SIN60/3) * SIGNS[a][0])
        yycur.insert(y1 + yvec/2 + abs(xvec*SIN60/3) * SIGNS[a][1])
        acur.insert((a - 1 + 3) % 3 + (3 if a < 3 else 0))
        xxcur.insert(x1 + xvec/3)
        yycur.insert(y1 + yvec/3)

        xxcur, yycur = copy(xcur), copy(ycur)
        acur.next(); acur.next(); acur.next()

    ax.clear()
    ax.axis('equal')
    ax.axis('off')
    ax.axes.set_xlim(-1, 1)
    ax.axes.set_ylim(-1, 1)
    #ax.plot(xdata.as_list(), ydata.as_list())
    print(len(xdata))
    ax.plot(np.fromiter(xdata, np.float), np.fromiter(ydata, np.float),)

def slow_down(e):
    global jump 
    jump = 3
def quick(e):
    global jump 
    jump = 1

def main():
    plt.subplots_adjust(bottom=0.2)
    
    btn_slow = Button(plt.axes([0.7, 0.05, 0.1, 0.075]), "Slow")
    btn_quick = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), "Quick")
    btn_slow.on_clicked(slow_down)
    btn_quick.on_clicked(quick)
    
    ani = animation.FuncAnimation(fig, paint, interval=1000)
    plt.show()

fig, ax = plt.subplots()
if __name__ == '__main__':
    main()
