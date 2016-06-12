from tkinter import *
from tkinter import filedialog
import csv
class App:
	"""Builds the window UI and manages data IO"""
	#Init
	def __init__(self, master):
		# Background
		self.bg = Canvas(master, bg="white", height=510, width=510)
		self.bg.pack()
		
		# Buttons
		self.btnOF = Button(master, text="Open File", command=self.openFile, width="10")
		self.btnOF.pack(side=LEFT)
		self.btnSHp = Button(master, text="S/H Points", command=self.pointsShowHide, state=DISABLED, width="10")
		self.btnSHp.pack(side=LEFT)
		self.btnSHn = Button(master, text="S/H Names", command=self.namesShowHide, state=DISABLED, width="10")
		self.btnSHn.pack(side=LEFT)
		self.btnSHl = Button(master, text="S/H Lines", command=self.linesShowHide, state=DISABLED, width="10")
		self.btnSHl.pack(side=LEFT)
		
		# Variables
		self.fileName = ''
		self.coord = []
		self.pointsShowHide, self.namesShowHide, self.linesShowHide = 1, 1, 1
		self.gridx, self.gridy = 0,0
	
	def read(self):
		# Defining variables
		items = []
		char = ""
		
		# Opening file
		with open(self.fileName, 'r', newline='') as csvfile:
			csvData = csv.reader(csvfile, delimiter=' ', quotechar='|')
			
			# Reading each row in csvData
			for rows in csvData:
				
				# Extracting data from rows
				for data in rows:
					row = []
					data += ","
					
					# Reformatting data
					for symbol in data:
						if symbol == ",":
							row.append(float(char))
							char = ""
						else:
							char += symbol	
				
				items.append(row)
			
			# Recalculating data to fit window
			items = self.resizeList(items)
			
			# Flipping data incase written incorrectly
			if len(items[1]) != 2: output = self.flipCSV(items)
			else: output = items
		
		return output
	
	# Buttons
	def openFile(self):
		# Opening file dialog and reading selected file
		self.fileName = filedialog.askopenfilename()
		
		if self.fileName != '':
			self.gridx, self.gridy = 0,0
			self.coord = self.read()
			
			# Setting buttons to "Active" state
			self.btnSHp['state'] = self.btnSHn['state'] = self.btnSHl['state'] = 'normal'
			
			# Drawing using data read from selected file
			self.draw(self.coord)
	
	def pointsShowHide(self):
		if self.pointsShowHide == 1:
			self.pointsShowHide = 0
			self.draw(self.coord)		
		else:
			self.pointsShowHide = 1
			self.draw(self.coord)
	
	def namesShowHide(self):
		if self.namesShowHide == 1:
			self.namesShowHide = 0
			self.draw(self.coord)
		else:
			self.namesShowHide = 1
			self.draw(self.coord)
	
	def linesShowHide(self):
		if self.linesShowHide == 1:
			self.linesShowHide = 0
			self.draw(self.coord)
		else:
			self.linesShowHide = 1
			self.draw(self.coord)
	
	# Data recalculators
	def flipCSV(self, items):
		newxy = []
		for x in range(0,len(items)): newxy.append([items[0][x],items[1][x]])
		return newxy
	
	def resizeList(self, items):
		xval, yval = [], []
		
		# Deviding x & y values to separate lists
		for x in range(0,len(items)): xval.append(items[x][0])
		for y in range(0,len(items)): yval.append(items[y][1])
		xsort = list(xval)
		ysort = list(yval)
		xsort.sort(key=float)
		ysort.sort(key=float)
		
		# Shifting negative values to 0+
		if xsort[0] < 0: 
			self.gridx = xsort[0]
			xval = [round(i - xsort[0],2) for i in xval]
			xsort = list(xval)
		if ysort[0] < 0: 
			self.gridy = ysort[0]
			yval = [round(j - ysort[0],2) for j in yval]
			ysort = list(yval)
		
		# Resize to fit windows
		divx = (xsort[len(xval)-1] + xsort[0])/460
		
		if divx == 0: divx +=1		
		xval = [round(m/ divx,0)+20 for m in xval]
		divy = (ysort[len(yval)-1] + ysort[0])/460
		
		if divy == 0: divy +=1		
		yval = [(480 - round(n / divy,0)) for n in yval]
		
		# Shifting grid axis
		self.gridx = round(self.gridx / divx,0)
		self.gridy = round(self.gridy / divy,0)
		
		return list(map(list,zip(xval,yval)))
	# Plotter caller
	def draw(self, xy):
		#Clearing canvas
		self.bg.delete("all")
		
		# Connecting points with lines
		for i in range(0, len(self.coord)-1):
			if self.linesShowHide == 1: pl.drawLine(self.coord[i][0],self.coord[i][1],self.coord[i+1][0],self.coord[i+1][1])
		
		# Drawing points
		for j in range(0,len(self.coord)):
			if self.pointsShowHide == 1: pl.drawPoint(self.coord[j][0],self.coord[j][1])
			if self.namesShowHide == 1: 
				if j == 0: pl.drawVName(self.coord[j][0]-20,self.coord[j][1],j+1)
				elif j == (len(self.coord)-1): pl.drawVName(self.coord[j][0]+20,self.coord[j][1],j+1)
				elif self.coord[j][1] > self.coord[j+1][1]: pl.drawVName(self.coord[j][0],self.coord[j][1]+20,j+1)
				else: pl.drawVName(self.coord[j][0],self.coord[j][1]-20,j+1)
		
		# Drawing grid
		pl.drawGrid(self.gridx,self.gridy)
class Plotter(object):
	"""Draws canvas elements"""
	def __init__(self, plot): self.plot = plot
	def drawPoint(self,x, y):
		# Draws "+" to indicate point location
		size = 10
		self.plot.bg.create_line(x, y-size, x, y+size, fill="black", width=size/5)
		self.plot.bg.create_line(x-size, y, x+size, y, fill="black", width=size/5)
	def drawLine(self,x1,y1,x2,y2): self.plot.bg.create_line(x1, y1, x2, y2, fill="red", width=3)
	# Draws point name
	def drawVName(self,x, y,txt): self.plot.bg.create_text(x,y,fill="blue",text=txt,)
	# Draws grid
	def drawGrid(self, gridx,gridy):
		self.plot.bg.create_line(20 - gridx, 0, 20 - gridx, 510, fill="black", width=1)
		self.plot.bg.create_line(510, 480 + gridy, 0, 480 + gridy, fill="black", width=1)
		self.plot.bg.create_text(10 - gridx,490+gridy,fill="blue",text="0")
# App start
root = Tk()
app = App(root)
pl = Plotter(app)
root.title("Graph plotter")
root.resizable(0,0)
root.mainloop()