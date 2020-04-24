import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from random import uniform, random
from json import load as json_load
import matplotlib.animation as animation
import sys

def parse(fname):
    with open(fname) as f:
       config = json_load(f)

    if "config" not in config: raise ValueError('"config" parameter missing')

    prob_sum = sum([i['probability'] for i in config['config']])
    for i in config['config']:
        i['probability'] /= prob_sum

    return config['config']

x, y = 1, 1
jump = 1

def paint(zz):
    global x, y, ax, jump, config
    if zz % jump != jump - 1:
        return 
    for _ in range(150):
        r = random()
        for cc in config:
            if r <= cc['probability']:
                x1, y1 = eval(cc['exper'], {'x':x,'y':y})
                break
            r -= cc['probability']

        x, y = x1, y1
        ax.scatter(x, y, s = 3)

def slow_down(e):
    global jump
    jump = 3

def quick(e):
    global jump
    jump = 1

config = parse(sys.argv[-1])
fig, ax = plt.subplots()

def main():
    plt.subplots_adjust(bottom=0.2)
    ax.axis('equal')
    ax.axis('off')
    ax.axes.set_xlim(-0.5, 1.5)
    ax.axes.set_ylim(-0.5, 1.5)
    
    btn_slow = Button(plt.axes([0.7, 0.05, 0.1, 0.075]), "Slow")
    btn_quick = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), "Quick")
    btn_slow.on_clicked(slow_down)
    btn_quick.on_clicked(quick)
    
    ani = animation.FuncAnimation(fig, paint, interval=100)
    plt.show()

if __name__ == "__main__":
    main()
