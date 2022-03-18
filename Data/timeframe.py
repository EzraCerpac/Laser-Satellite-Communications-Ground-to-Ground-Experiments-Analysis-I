import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

file = 'CSV/data18urad.csv'
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

plt.plot(np.arange(len(heightlst)),heightlst)
plt.show()

beginings = {
    'off 1' : heightlst.index(max(heightlst[0:100])) * dt,
    '2 modes' : heightlst.index(min(heightlst[50:150])) * dt,
    'off 2' : heightlst.index(max(heightlst[100:200])) * dt,
    '28 modes' : heightlst.index(min(heightlst[200:300])) * dt,
    'off 3' : heightlst.index(max(heightlst[250:400])) * dt,
    '4 modes' : heightlst.index(min(heightlst[350:450])) * dt,
    'off 4' : heightlst.index(max(heightlst[400:520])) * dt,
    '8 modes': heightlst.index(min(heightlst[500:600])) * dt,
    'off 5' : heightlst.index(max(heightlst[550:700])) * dt,
    '16 modes' : heightlst.index(min(heightlst[650:700])) * dt

}

print(beginings)