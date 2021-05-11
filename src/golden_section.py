'''
import math

def golden_section(func, x, dim, range, eps = 0.0001):
	k = (math.sqrt(5)-1)/2

	a = x[dim] - range
	b = x[dim] + range
	print('Poczatek zlotego podzialu');
	print('lewy: {}, prawy: {}'.format(a, b))
	xL = b - k * (b - a)
	xR = a + k * (b - a)

	while(abs(b - a) > eps):
		#x[dim] = xL
		xLRes = func(x)
		#x[dim] = xR
		xRRes = func(x)
		print('zloty podzial xL: {} xR: {}'.format(xL, xR))

		if(xLRes < xRRes):
			b = xR
			xR = xL
			xL = b - k * (b - a)
		else:
			a = xL
			xL = xR
			xR = a + k * (b - a)

	return (a + b) / 2
'''

'''
import math

k = (math.sqrt(5)-1)/2

def golden_section(func, x, dim, range, eps = 0.0001):
	a = x[dim] - range
	b = x[dim] + range
	xL = a + (1 - k) * (b - a)
	xR = b - (1 - k) * (b - a)
	print("poczatek zlotego podzialu")
	print(x)

	while(abs(b - a) > eps):
		x[dim] = xL
		xLRes = func(x)
		x[dim] = xR
		xRRes = func(x)

		print('a: {:.2f} b: {:.2f} xL: {:.2f}, xR: {:.2f}, xLRes: {:.2f} xRRes: {:.2f}'.format(a, b, xL, xR ,xLRes, xRRes))

		if(xLRes < xRRes):
			b = xR
			xR = xL
			xL = a + (1 - k) * (b - a)
		else:
			a = xL
			xL = xR
			xR = b - (1 - k) * (b - a)


	return (a + b) / 2

'''


import math

gr = (math.sqrt(5) + 1) / 2

def golden_section(f, x, dim, range, tol=1e-9):
	"""Golden-section search
	to find the minimum of f on [a,b]
	f: a strictly unimodal function on [a,b]

	Example:
	>>> f = lambda x: (x-2)**2
	>>> x = gss(f, 1, 5)
	>>> print("%.15f" % x)
	2.000009644875678

	"""
	a = x[dim] - range
	b = x[dim] + range

	c = b - (b - a) / gr
	d = a + (b - a) / gr
	while abs(b - a) > tol:
		x[dim] = c
		cRes = f(x)
		x[dim] = d
		dRes = f(x)

		if cRes < dRes:
			b = d
		else:
			a = c

		# We recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
		c = b - (b - a) / gr
		d = a + (b - a) / gr

	return (b + a) / 2