import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('CSV/data22urad.csv', skiprows= 1, names = ['time','irradiance'])

timelist = data['time']

#i = 0
#while i < len(timelist):
#    diff = timelist[i+1] - timelist[i]
#    if abs(diff) > 0.002:
#        print(i)
#        wrongdata.append(i)
#    i += 1

#print(timelist[513443] - timelist[513442])
cor = [[171277, 173730, 12309600],[513443, 515922, -691200], [1019369, 1021822, 12268800]]
tl2 = timelist

i = 0
while i < len(tl2):
    if cor[0][0] <= i <= cor[0][1]:
        tl2[i] = tl2[i] + cor[0][2]
    elif cor[1][0] <= i <= cor[1][1]:
        tl2[i] = tl2[i] + cor[1][2]
    elif cor[2][0] <= i <= cor[2][1]:
        tl2[i] = tl2[i] + cor[2][2]

    i += 1

data ['time'] = tl2

data.to_csv('CSV/data22urad.csv')

# plt.plot(tl2, data['irradiance'])
# plt.show()