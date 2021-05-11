import math
from golden_section import golden_section
from py_expression_eval import Parser
import numpy as np



class GaussSeidel():

	def calculate(self, function, start, eps, range, maxIter):
		self.parser = Parser()
		self.function = self.parser.parse(function)

		self.start = [float(point) for point in start.split(';')]
		self.eps = float(eps)
		self.range = float(range)
		self.maxIter = int(maxIter)
		self.currentX = self.start
		self.currentRes = 1000;
		self.variables = self.function.variables()
		self.innerX = []
		self.innerX.append(self.currentX.copy())
		self.X = []
		self.X.append(self.currentX.copy())
		self.Results = []
		self.Steps = []
		self.ResStep = []
		self.ResultTableData = []
		self.EndingText = ""
		self.levelSetMargin = 0.1

		self.run()
	
	def run(self):			
		formattedCurrentX = ["{:0.5f}".format(v) for v in self.currentX];
		result = self.calculateFunction(self.currentX)
		self.ResultTableData.append(["{0}".format(formattedCurrentX), round(result, 5), "-", "-", 0])

		for iter in range(1, self.maxIter + 1):
			xold = self.currentX.copy();
			resOld = self.calculateFunction(self.currentX)
			self.Results.append(resOld)
			for k in range(0, len(self.variables)):
				#eforeRes = self.calculateFunction(self.currentX)
				argLocalMin = golden_section(self.calculateFunction, self.currentX.copy(), k, self.range, self.eps)
				#adjustedX = self.currentX.copy()
				#adjustedX[k] = argLocalMin
				#afterRes = self.calculateFunction(adjustedX)
				#if beforeRes > afterRes:
				self.currentX[k] = argLocalMin
				self.innerX.append(self.currentX.copy())
			self.X.append(self.currentX.copy())
			res = self.calculateFunction(self.currentX)
			self.currentRes = res			
			step = [(self.currentX[index]- xold[index])**2 for index in range(0, len(self.variables))]
			step_distance = math.sqrt(sum(step))
			self.Steps.append(step_distance)
			res_disance = abs(res - resOld)
			self.ResStep.append(res_disance)
			formattedCurrentX = ["{:0.5f}".format(v) for v in self.currentX];
			self.ResultTableData.append(["{0}".format(formattedCurrentX), "{:0.5f}".format(res), "{:0.8f}".format(step_distance), "{:0.8f}".format(res_disance), iter])
			if(step_distance < self.eps):
				self.EndingText = 'Koniec algorytmu z 1 warunku'
				return
			if(res_disance < self.eps):
				self.EndingText = 'Koniec algorytmu z 2 warunku'
				return

			k += 1
		self.EndingText = 'Koniec algorytmu z 3 warunku'


	def get_current_X(self):
		return self.currentX

	def get_formatted_current_X(self):
		formattedCurrentX = ["{:0.5f}".format(v) for v in self.currentX];
		return formattedCurrentX


	def get_current_res(self):
		return self.currentRes

	def get_result_table_data(self):
		return self.ResultTableData

	def get_ending_text(self):
		return self.EndingText


	def calculateFunction(self, x):
		evalDictionary = {self.variables[i]: x[i] for i in range(len(self.variables))}
		#print(evalDictionary)
		value = self.function.evaluate(evalDictionary)
		return value

	def generatePlot(self, ax, fig):
		if(len(self.variables) != 2 and len(self.variables) != 3):
			print("Ilosc zmiennych rozna od 2 lub 3")
			return ax
		if(len(self.variables) == 2):
			return self.generate2DPlot(ax, fig)
		return self.generate3DPlot(ax, fig)

	def generate2DPlot(self, ax, fig):
		ax.set_title('Warstwica funkcji')
		X = np.array(self.innerX)
		maxXSetRange = max(X[:, 0]) + self.levelSetMargin;
		minXSetRange = min(X[:, 0]) - self.levelSetMargin;
		maxYSetRange = max(X[:, 1]) + self.levelSetMargin;
		minYSetRange = min(X[:, 1]) - self.levelSetMargin;
		print('{} {} {} {}'.format(maxXSetRange, minXSetRange, maxYSetRange, minYSetRange))



		ax.set_xlim(minXSetRange, maxXSetRange)
		ax.set_ylim(minYSetRange, maxYSetRange)
		ax = self.levelSetPlot(ax, fig, maxXSetRange, minXSetRange, maxYSetRange, minYSetRange)
		ax = self.gaussSeidelPlot2D(ax)
		return ax

	def generate3DPlot(self, ax, fig):
		ax.set_title('Warstwica funkcji')
		X = np.array(self.innerX)
		maxXSetRange = max(X[:, 0]) + self.levelSetMargin;
		minXSetRange = min(X[:, 0]) - self.levelSetMargin;
		maxYSetRange = max(X[:, 1]) + self.levelSetMargin;
		minYSetRange = min(X[:, 1]) - self.levelSetMargin;
		maxZSetRange = max(X[:, 2]) + self.levelSetMargin;
		minZSetRange = min(X[:, 2]) - self.levelSetMargin;



		ax.set_xlim(minXSetRange, maxXSetRange)
		ax.set_ylim(minYSetRange, maxYSetRange)
		ax.set_zlim(minZSetRange, maxZSetRange)
		ax = self.levelSet3DPlot(ax, fig, maxXSetRange, minXSetRange, maxYSetRange, minYSetRange, maxZSetRange, minZSetRange)
		ax = self.gaussSeidelPlot3D(ax)
		return ax

	def levelSetPlot(self, ax, fig, maxXSetRange, minXSetRange, maxYSetRange, minYSetRange):
		print("Create level set 2D")
	
		numberOfVars = 30;
		xDiff = maxXSetRange - minXSetRange
		yDiff = maxYSetRange - minYSetRange

		x_ = np.linspace(minXSetRange - xDiff * 0.1, maxXSetRange + xDiff * 0.1, num=numberOfVars)
		y_ = np.linspace(minYSetRange - yDiff * 0.1, maxYSetRange + yDiff * 0.1, num=numberOfVars)
		x, y = np.meshgrid(x_, y_)
		levels=np.zeros((len(x),len(y)))

		
		for i in range(len(x)):
			for j in range(len(y)):
				X = [x[i][j], y[i][j]]
				value = self.calculateFunction(X)
				levels[i, j] = value
		
		cs = ax.contourf(x, y, levels, 50)
		fig.colorbar(cs, ax=ax, shrink=0.9)

		#plt.colorbar()	

		return ax 

	def levelSet3DPlot(self, ax, fig, maxXSetRange, minXSetRange, maxYSetRange, minYSetRange, maxZSetRange, minZSetRange):
		print("Create level set 3D")
		
		numberOfVars = 30;
		xDiff = maxXSetRange - minXSetRange
		yDiff = maxYSetRange - minYSetRange
		zDiff = maxZSetRange - minZSetRange

		x_ = np.linspace(minXSetRange, maxXSetRange, num=numberOfVars)
		y_ = np.linspace(minYSetRange, maxYSetRange, num=numberOfVars)
		z_ = np.linspace(minZSetRange, maxZSetRange, num=numberOfVars)
		x, y, z = np.meshgrid(x_, y_, z_)
		levels=np.zeros((len(x),len(y), len(z)))
		print(levels.shape)
		#U = np.exp(-(x/2) ** 2 - (y/3) ** 2 - z ** 2)
		for i in range(len(x)):
			for j in range(len(y)):
				for k in range(len(z)):
					X = [x[i][j][k], y[i][j][k], z[i][j][k]]
					value = self.calculateFunction(X)
					levels[i,j,k] = value
		
		ax.set_xlabel('x')
		ax.set_ylabel('y')
		ax.set_zlabel('z')
		cs = ax.scatter3D(x, y, z, c=levels.flatten(), alpha=0.7, marker='.')
	
		fig.colorbar(cs, ax=ax, shrink=0.9)

		#plt.show()
		#ax.plot_surface(x,y,z, facecolors=levels)
		#ax.contour(x, y, z, levels=levels)
		#plt.colorbar()	

		return ax 

	def gaussSeidelPlot2D(self, ax):
		x = []
		y = []
		for i in range(len(self.innerX)):
			x.append(self.innerX[i][0])
			y.append(self.innerX[i][1])
		ax.plot(x, y, 'r')
		markerSize = 40;
		ax.scatter(self.innerX[len(self.innerX) - 1][0], self.innerX[len(self.innerX) - 1][1], 40)
		return ax

	def gaussSeidelPlot3D(self, ax):
		x = []
		y = []
		z = []
		for i in range(len(self.innerX)):
			x.append(self.innerX[i][0])
			y.append(self.innerX[i][1])
			z.append(self.innerX[i][2])
		#ax.scatter(self.innerX[0][0], self.innerX[0][1], 5)
		ax.plot(x, y, z, 'r')
		return ax

	def canPlotLevelSets(self):
		if(len(self.variables) != 2 and len(self.variables) != 3):
			return False
		return True

	def is2D(self):
		return len(self.variables) == 2
	def is3D(self):
		return len(self.variables) == 3