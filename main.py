import swatch
#import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime


mydata = pd.read_csv("3077594.csv")

maxv = mydata.TMAX
minv=mydata.TMIN

therange= max(mydata.TMAX) - min(mydata.TMAX)
bin = therange// 15

colorscore =[]
months = []
days = []
mycolordict = dict()

for i,x in enumerate(mydata.TMAX[0:365]):
    newval = x - min(mydata.TMAX)
    xscore = newval//bin
    colorscore.append(xscore)
    mydate = datetime.datetime.strptime(mydata.DATE[i], "%Y-%m-%d")
    mym = mydate.month
    myd = mydate.day
    if mym=='' or myd =='':
        print(mydata.DATE[i])
        print('mym {}'.format(mym))
        print('myd {}'.format(myd))
    mycolordict.update({(mym,myd): xscore})

def calculateZ(Xv, Yv):
    value = mycolordict.get((Xv,Yv))
    if value == None:
        return float(0)
    else:
        return float(value)
vcalcZ = np.vectorize(calculateZ)
plt.show()
plt.style.use('_mpl-gallery-nogrid')

X, Y = np.meshgrid(np.linspace(1,12, 12), np.linspace(1, 31, 31))
Z = vcalcZ(X,Y)

fig, ax =plt.subplots()
# plot
ax.imshow(Z)

plt.show()