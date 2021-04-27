import math

def golden_section(func, x, dim, range, eps = 0.0001):
	k = (math.sqrt(5)-1)/2

	a = x[dim] - range
	b = x[dim] + range
	
	xL = b - k * (b - a)
	xR = a + k * (b - a)

	while((b - a) > eps):
		x[dim] = xL
		xLRes = func(x)
		x[dim] = xR
		xRRes = func(x)

		if(xLRes < xRRes):
			b = xR
			xR = xL
			xL = b - k * (b - a)
		else:
			a = xL
			xL = xR
			xR = a + k * (b - a)

	return (a + b) / 2