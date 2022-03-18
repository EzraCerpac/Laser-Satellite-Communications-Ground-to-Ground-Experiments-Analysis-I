import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('CSV/data22urad.csv', skiprows= 1, names = ['time','irradiance'])

tl2 = data['time']
#print(timelist[1902320] - timelist[1902320+1])

# wrongdata=[]
# i = 0
# while i < len(timelist):
#    diff = timelist[i+1] - timelist[i]
#    if abs(diff) > 0.002:
#        print(i)
#        wrongdata.append(i)
#    i += 1

cor = [[83389, 85846, 12234180],[192581, 195036, 12235200], [286857, 291794, 12232800],[510251,512706,12096000],[1180131,1182612,2400],[1468035,1470516,2400],[1621909,1624366,12268800],[1654171,1656626,12182400],[1748465,1750920,12232800],[1902321,1904776,12234850]]

# for j in range(len(tl2)):
#     if cor[0][0] <= j <= cor[0][1]:
#         tl2[j] = tl2[j] + cor[0][2]
#     elif cor[1][0] <= j <= cor[1][1]:
#         tl2[j] = tl2[j] + cor[1][2]
#     elif cor[2][0] <= j <= cor[2][1]:
#         tl2[j] = tl2[j] + cor[2][2]
#     elif cor[3][0] <= j <= cor[3][1]:
#         tl2[j] = tl2[j] + cor[3][2]
#     elif cor[4][0] <= j <= cor[4][1]:
#         tl2[j] = tl2[j] + cor[4][2]
#     elif cor[5][0] <= j <= cor[5][1]:
#         tl2[j] = tl2[j] + cor[5][2]
#     elif cor[6][0] <= j <= cor[6][1]:
#         tl2[j] = tl2[j] + cor[6][2]
#     elif cor[7][0] <= j <= cor[7][1]:
#         tl2[j] = tl2[j] + cor[7][2]
#     elif cor[8][0] <= j <= cor[8][1]:
#         tl2[j] = tl2[j] + cor[8][2]
#     elif cor[9][0] <= j <= cor[9][1]:
#         tl2[j] = tl2[j] + cor[9][2]
#
tl2 = tl2 - tl2[0]
#
# print(tl2[0],tl2[len(tl2)-1])
#
#
data['time'] = tl2
#data.to_csv('CSV/data22urad.csv')
plt.plot(data['time'], data['irradiance'])
plt.show()