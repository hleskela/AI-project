import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = []
Y = []
Z = []

f = open("plot.txt")
for line in f.readlines():
    la = line.split(' , ')
    X.append(int(la[1]))
    Y.append(int(la[2]))
    Z.append(int(la[0]))

X, Y = np.meshgrid(X, Y)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

ax.set_xlabel('Significant Unigram Words')
ax.set_ylabel('Significant Bigram Words')
ax.set_zlabel('Number of Correct Articles')

plt.savefig('reinforcement_plot.png')
