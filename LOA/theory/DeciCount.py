import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
allowedChars = {'0','1','2','3','4','5','6','7','8','9'}
class IndexTracker:
	def __init__(self,ax,X,boardsizes,cmap='viridis'):
		self.ax = ax
		self.boardsizes = boardsizes
		ax.set_title("(q) quit, (w) decrease frame, (e) increase frame")
		self.cmap = cmap
		self.X = X
		rows, cols, self.slices = X.shape
		self.ind = self.slices//2
		self.im = ax.imshow(self.X[:,:,self.ind],cmap=self.cmap)
		self.update()
	def onPress(self,event):
		if event.key == 'w':
			self.ind = (self.ind-1)%self.slices
		elif event.key == 'e':
			self.ind = (self.ind+1)%self.slices
		self.update()
	def update(self):
		self.im.set_data(self.X[:,:,self.ind])
		self.ax.set_xlabel('Board Size  %s' % self.boardsizes[self.ind])
		self.im.axes.figure.canvas.draw()
def isPrime(n):
	if n==2 or n==3: return True
	if n%2==0 or n < 2: return False
	for i in range(3,int(n**0.5)+1,2):
		if n%i == 0: return False
	return True
def factorial(n):
	if (n == 1 or n == 0):return 1
	else: return n*factorial(n-1)
def choose(n,k):
	return (factorial(n)/factorial(n-k)*factorial(k))
def DeciCount(red, black,boardsize,limit):
	if (red+black >= boardsize):
		return 2
	total = 0
	for i in range(2,red+1):
		for j in range(2,black+1):
			total = total + (choose(boardsize,i)*choose(boardsize-i,j))
			if (total >= limit):
				return 1
	return 0
#https://matplotlib.org/gallery/event_handling/image_slices_viewer.html#sphx-glr-gallery-event-handling-image-slices-viewer-py
def build(boardsizes,limit):
	arr = [[[DeciCount(i,j,k,limit) for k in boardsizes] for j in range(2,33)] for i in range(2,33)]
	return arr
def clean(usr_input):
	intList = [int(i) for i in list(usr_input) if i in allowedChars]
	n = 0
	for i in intList:
		n = (n*10) + i
	return n
def main():
	limit = clean(input("Enter upper bound: "))
	boardsizes = [i for i in range(65) if not isPrime(i)]
	data = np.array(build(boardsizes,limit))
	
	fig, ax = plt.subplots(1,1)	
	ax.set_xlim(0,32)
	ax.set_ylim(0,32)
	#ax.transData.translate(2,2)
	colors = [(0,1,0),(1,0,0),(0,0,0)]
	cmapname = 'my_map'
	cm = LinearSegmentedColormap.from_list(cmapname,colors,N=3)
	tracker = IndexTracker(ax, data,boardsizes,cm)
	fig.canvas.mpl_connect('key_press_event',tracker.onPress)
	
	green_patch = mpatches.Patch(color=(0,1,0),label = 'Within bounds')
	red_patch = mpatches.Patch(color=(1,0,0), label = 'Exceeded bounds')
	black_patch = mpatches.Patch(color=(0,0,0),label = 'Junk')
	##Not hard coded legend would be cool
	plt.legend(handles=[green_patch,red_patch,black_patch])
	plt.show()
main()
