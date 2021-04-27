import math
from golden_section import golden_section
from py_expression_eval import Parser

x = [100, -100, 2.5]
X = x

y = lambda x: (x[0]-x[1]+x[2])**2+(-x[0]+x[1]+x[2])**2+(x[0]+x[1]-x[2])**2

maxIteration = 30
eps = 0.0001

for iter in range(1, maxIteration):
	print(iter)
	print(y(x))

	xold = x.copy();
	resOld = y(x)
	for k in range(0, len(x)):
		argLocalMin = golden_section(y, x, k, -10, 10)
		x[k] = argLocalMin
	res = y(x)
	step = [abs(x[index]- xold[index]) for index in range(0, len(x))]
	max_step = max(step)
	if(max_step < eps):
		print('Koniec algorytmu z 1 warunku')
		break
	if(abs(res - resOld) < eps):
		print('Koniec algorytmu z 2 warunku')
		break

print(x)
print(y(x))

class GaussSeidel():
	def calculate(function, start, eps, range):
		self.parser = Parser()
		self.function = function
		self.start = [float(point) for point in start.split(';')]
		self.eps = float(eps)
		self.range = float(range)
		
