import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

file = 'CSV/data22urad.csv'
data = pd.read_csv(file, skiprows=1, names = ['time','irradiance'])
time = np.array(data['time'])
psi = data['irradiance']

time = time.astype(int)



dt = 1. #s
t = 0. #s

list = np.array([])

while t < time[len(time)-1]:
    ind = int(np.where(time == t)[0][0])
    list = np.append(list, ind)
    t += dt

slotlst = []
#print(list)
i = 0

while i < len(list) - (30/dt +1):
    timeslot = [list[i],list[i+ int(30/dt)]]
    slotlst.append(timeslot)
    i+= 1

j = 0
heightlst = []
while j < len(slotlst):
    beg = int(slotlst[j][0])
    end = int(slotlst[j][1])
    height = np.var(psi[beg:end+1])
    heightlst.append(height)
    j += 1

# print(heightlst)
# print(slots)

plt.plot(np.arange(len(heightlst)),heightlst, linewidth = 0.5)
# plt.vlines(10/dt,1e11,2e11,colors = 'red')
# plt.vlines(56/dt,1e11,2e11,colors = 'red')
# plt.vlines(98/dt,1e11,2e11,colors = 'red')
# plt.vlines(140/dt,1e11,2e11,colors = 'red')
# plt.vlines(180/dt,1e11,2e11,colors = 'red')
# plt.vlines(220/dt,1e11,2e11,colors = 'red')
# plt.vlines(260/dt,1e11,2e11,colors = 'red')
# plt.vlines(300/dt,1e11,2e11,colors = 'red')
# plt.vlines(340/dt,1e11,2e11,colors = 'red')

plt.show()

# beginings = {
#     'off 1' : heightlst.index(max(heightlst[0:50])) * dt,
#     '2 modes' : heightlst.index(min(heightlst[40:70])) * dt,
#     'off 2' : heightlst.index(max(heightlst[70:100])) * dt,
#     '28 modes' : heightlst.index(min(heightlst[80:120])) * dt,
#     'off 3' : heightlst.index(max(heightlst[120:200])) * dt,
#     '4 modes' : heightlst.index(min(heightlst[200:250])) * dt,
#     'off 4' : heightlst.index(max(heightlst[250:300])) * dt,
#     '8 modes': heightlst.index(min(heightlst[300:360])) * dt,
#     'off 5' : heightlst.index(max(heightlst[350:370])) * dt,
#     '16 modes' : heightlst.index(min(heightlst[350:400])) * dt
#
# }
#
# print(beginings)