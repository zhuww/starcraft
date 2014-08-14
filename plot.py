import numpy as np
from numpy import array
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import RBUT

verts = [
    (0., 0.), # left, bottom
    (0., 1.), # left, top
    (1., 1.), # right, top
    (1., 0.), # right, bottom
    (0., 0.), # ignored
    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]


path = Path(verts, codes)


def box(xo, yo, width, height, color='orange', lw=1):
        verts = [
            (xo, yo), # left, bottom
            (xo, yo+height), # left, top
            (xo+width, yo+height), # right, top
            (xo+width, yo), # right, bottom
            (0., 0.), # ignored
            ]
        codes = [Path.MOVETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.LINETO,
                 Path.CLOSEPOLY,
                 ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color, lw=lw)
        patch.set_alpha(0.5)
        return patch

def plotlog(splt, item):
    if isinstance(item[0], RBUT.unit):
        color = 'blue'
    elif isinstance(item[0], RBUT.building):
        color = 'red'
    elif isinstance(item[0], RBUT.tech):
        color = 'orange'
    patch = box(item[2],item[1],item[3],item[0].MineReq, color=color)
    splt.add_patch(patch)
    splt.text(item[2]+0.5*item[3], item[1]+0.5*item[0].MineReq, item[0].name,ha='center', va='center', rotation=90)
    

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(0,2)
    ax.set_ylim(0,2)
    patch = box(1.,1.,0.5,0.5)
    ax.add_patch(patch)
    ax.text(1.25,1.25,'test', ha='center', va='center' )
    plt.show()
