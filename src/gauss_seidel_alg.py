import math
from golden_section import golden_section
from py_expression_eval import Parser
from matplotlib import pyplot as plt
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
		self.X = []
		self.X.append(self.currentX.copy())
		self.Results = []
		self.Steps = []
		self.ResStep = []
		self.iterationText = ""

		self.run()
	
	def run(self):
		k = 0
		for iter in range(1, self.maxIter):
			if k >= len(self.variables):
				k = 0
			xold = self.currentX.copy();
			resOld = self.calculateFunction(self.currentX)
			self.Results.append(resOld)
			argLocalMin = golden_section(self.calculateFunction, self.currentX, k, self.range)
			self.currentX[k] = argLocalMin
			self.X.append(self.currentX.copy())
			res = self.calculateFunction(self.currentX)
			self.currentRes = res			
			self.iterationText += 'Iteracja {}, pozycja: {}, wartosc funkcji: {}\n'.format(iter, np.around(self.currentX, 3), round(res, 3))
			step = [abs(self.currentX[index]- xold[index]) for index in range(0, len(self.variables))]
			max_step = max(step)
			self.Steps.append(max_step)
			res_disance = abs(res - resOld)
			self.ResStep.append(res_disance)
			if(max_step < self.eps):
				self.iterationText += 'Koniec algorytmu z 1 warunku'
				break
			if(res_disance < self.eps):
				self.iterationText += 'Koniec algorytmu z 2 warunku'
				break

			k += 1
				

	def get_current_X(self):
		return self.currentX

	def get_current_res(self):
		return self.currentRes

	def get_iteration_text(self):
		return self.iterationText

	def calculateFunction(self, x):
		evalDictionary = {self.variables[i]: x[i] for i in range(len(self.variables))}
		value = self.function.evaluate(evalDictionary)
		return value

	def generatePlot(self, ax):
		if(len(self.variables) != 2):
			print("Ilosc zmiennych rozna od 2")
			return ax

		ax.set_title('Warstwica funkcji')
		X = np.array(self.X)
		maxXSetRange = max(X[:, 0]) + 2;
		minXSetRange = min(X[:, 0]) - 2;
		maxYSetRange = max(X[:, 1]) + 2;
		minYSetRange = min(X[:, 1]) - 2;



		ax.set_xlim(minXSetRange, maxXSetRange)
		ax.set_ylim(minYSetRange, maxYSetRange)
		ax = self.levelSetPlot(ax, maxXSetRange, minXSetRange, maxYSetRange, minYSetRange)
		ax = self.gaussSeidelPlot(ax)
		return ax


	def levelSetPlot(self, ax, maxXSetRange, minXSetRange, maxYSetRange, minYSetRange):
		print("Create level set")
	
		numberOfVars = 30;
		xDiff = maxXSetRange - minXSetRange
		yDiff = maxYSetRange - minYSetRange

		x_ = np.linspace(minXSetRange - xDiff * 0.3, maxXSetRange + xDiff * 0.3, num=numberOfVars)
		y_ = np.linspace(minYSetRange - yDiff * 0.3, maxYSetRange + yDiff * 0.3, num=numberOfVars)
		x, y = np.meshgrid(x_, y_)
		levels=np.zeros((len(x),len(y)))

		
		for i in range(len(x)):
			for j in range(len(y)):
				X = [x[i][j], y[i][j]]
				value = self.calculateFunction(X)
				levels[i, j] = value
		
		ax.contour(x, y, levels, 50)
		#plt.colorbar()	

		return ax 

	def gaussSeidelPlot(self, ax):
		x = []
		y = []
		for i in range(len(self.X)):
			x.append(self.X[i][0])
			y.append(self.X[i][1])
		print(x)
		ax.plot(x, y, 'r')
		return ax
