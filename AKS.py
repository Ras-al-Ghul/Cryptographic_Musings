from copy import deepcopy
from fractions import gcd
from math import ceil, log, sqrt

def isqrt(n):
	if n < 0:
		raise ValueError('Square root not defined for negative numbers')
	nn = long(n)
	if nn == 0:
		return nn
	q, r = divmod(nn.bit_length(), 2)
	n = 2 ** (q + r)
	while True:
		o = (n + nn // n) // 2
		if o >= n:
			return n
		n = o

def order(r, n):
	o = 3
	while True:
		if pow(n, o, r) == 1:
			return o
		o += 1

def totient(r):
	tot = 0
	for i in xrange(1, r + 1):
		if gcd(r, i) == 1:
			tot += 1
	return tot

def polymul(polya, polyb, n):
	deg = len(polya) + len(polyb)
	poly = [0 for i in xrange(deg)]
	for i in xrange(len(polya)):
		for j in xrange(len(polyb)):
			poly[i + j] += polya[i] * polyb[j]
			poly[i + j] %= n
	return poly_mod(poly, n)

def degree(poly):
	while poly and poly[-1] == 0:
		# from the last
		poly.pop() 
	return len(poly) - 1

def normalize(poly):
	while poly and poly[-1] == 0:
		poly.pop()
	if poly == []:
		poly.append(0)

def polydiv(num, den):
	num = num[:]
	normalize(num)
	den = den[:]
	normalize(den)

	if len(num) >= len(den):
		#Shift den towards right so it's the same degree as num
		shiftlen = len(num) - len(den)
		den = [0] * shiftlen + den
	else:
		return num

	quot = []
	divisor = float(den[-1])
	for i in xrange(shiftlen + 1):
		#Get the next coefficient of the quotient.
		mult = num[-1] / divisor
		quot = [mult] + quot

		#Subtract mult * den from num, but don't bother if mult == 0
		#Note that when i==0, mult!=0; so quot is automatically normalized.
		if mult != 0:
			d = [mult * u for u in den]
			num = [u - v for u, v in zip(num, d)]

		num.pop()
		den.pop(0)

	normalize(num)
	return num

def poly_mod(poly, n):
	for i in range(len(poly)):
		poly[i] %= n
	return poly

def polydiv_with_mod(a, r, n):
	xplusa = [a, 1]
	poly = deepcopy(xplusa)
	xrminusone = [0 for i in xrange(r + 1)] # rth degree
	xrminusone[0] = -1
	xrminusone[r] = 1
	for i in xrange(2, n + 1):
		poly = polymul(poly, xplusa, n)
		if degree(poly) >= r:
			poly = polydiv(poly, xrminusone)
	return poly_mod(poly, n)

def main(n):
	# step 1 - checking n == a**b
	for a in xrange(2, isqrt(n) + 1):
		num = a
		for b in xrange(2, n):
			num *= a
			if num == n:
				return False
			if num > n:
				break

	# step 2 - finding smallest r
	logn = log(n, 2)
	logsquaredn = logn * logn

	r = 3
	while True:
		if gcd(r, n) == 1 and order(r, n) >= logsquaredn:
			break
		r += 1

	# step 3 check if 1 < (a, n) < n
	for a in xrange(2, r + 1):
		if 1 < gcd(a, n) < n:
			return False

	# step 4 if n <= r, output prime
	if n <= r:
		return True

	# step 5 loop iterations to check compositeness
	xnplusa = [0 for i in xrange(n + 1)] # nth degree
	xnplusa[n] = 1 # set the last index
	xrminusone = [0 for i in xrange(r + 1)] # rth degree
	xrminusone[0] = -1
	xrminusone[r] = 1
	for a in xrange(1, long(ceil(sqrt(totient(r)) * logn))):
		polycoeff = deepcopy(xnplusa)
		polycoeff[0] = a
		newpoly = polydiv_with_mod(a, r, n)
		normalize(newpoly)
		polycoeff = poly_mod(polydiv(polycoeff, xrminusone), n)
		normalize(polycoeff)
		print polycoeff, len(polycoeff)
		if cmp(polycoeff, newpoly) != 0:
			return False

	# step 6 output prime
	return True

if __name__ == '__main__':
	n = long(raw_input("Enter an integer > 1 "))
	if main(n):
		print "Prime"
	else:
		print "Composite"