'''
This code helps to visualize the top three prinicpal components

by Lambert Leong
'''
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os

data = pd.read_csv("vis_data.csv")
x = data.iloc[:,:-1]
y = data['label']
class0='b'
class1='r'
dx = x['dx']
dx_0 = dx[y==class0]
dx_1 = dx[y==class1]

mean_gz = x['mean_gz']
mean_gz_0 = mean_gz[y==class0]
mean_gz_1 = mean_gz[y==class1]

max_gz = x['max_gz']
max_gz_0 = max_gz[y==class0]
max_gz_1 = max_gz[y==class1]

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(max_gz_0,dx_0,mean_gz_0, c='r', label='class 0')
ax.scatter(max_gz_1,dx_1,mean_gz_1, c='b', label = 'class 1')
ax.set_xlabel('Maximum Z axis tilt')
ax.set_ylabel('Total X displacement')
ax.set_zlabel('Mean Z axis tilt')
plt.legend()
ax.view_init(60, -135)
plt.show()
