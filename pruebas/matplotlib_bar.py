"""

#!/usr/bin/env python
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt


N = 5
NN = 1, 1.5, 2, 2.5, 3
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)
menStd = (2, 3, 4, 1, 2)
womenStd = (3, 5, 2, 3, 3)
ind = np.arange(N)    # the x locations for the groups
print ind
#ind = NN
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, menMeans, width, color='r')
#p2 = plt.bar(ind, womenMeans, width, color='y', bottom=menMeans, yerr=womenStd)

plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind , ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 81, 10))
#plt.legend((p1[0], p2[0]), ('Men', 'Women'))

plt.show()

"""
"""
import numpy as np
import matplotlib.pyplot as plt

N = 10  #could change

plt.figure()

A   = np.array([70, 88, 78, 93, 99, 58, 89, 66, 77, 78])
B = np.array([73, 65, 78, 87, 97, 57, 77, 88, 69, 78])
C = np.array([66, 98, 88, 67, 99, 88, 62, 70, 90, 73])


ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, A,width, color='r')
p2 = plt.bar(ind, B, width, color='y', bottom=A)
p3 = plt.bar(ind, C, width, color='b', bottom=A+B)


plt.ylabel('Scores')
plt.title('Index')

plt.xticks(ind+width/2., ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))#dynamic - fed

plt.yticks(np.arange(0,300,10))
plt.legend( (p1[0], p2[0], p3[0]), ('A','B','C') )
plt.grid(True)


plt.show()


"""

import matplotlib.pyplot as plt

def main():
    # Make an example pie plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    labels = ['Apple', 'Mango', 'Orange']
    wedges, plt_labels = ax.pie([20, 40, 60], labels=labels)
    ax.axis('equal')

    make_picker(fig, wedges)
    plt.show()

def make_picker(fig, wedges):

    def onclick(event):
        wedge = event.artist
        label = wedge.get_label()
        print label

# Make wedges selectable
    for wedge in wedges:
        wedge.set_picker(True)

    fig.canvas.mpl_connect('pick_event', onclick)

if __name__ == '__main__':
    main()
    
    
    
