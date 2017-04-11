from random import randrange
from math import sqrt, floor
from fractions import gcd

def MillerRabin(N, t = 50):

	if(N == 2):
		return True

	if (N % 2 == 0 or N < 2):
		return False

	# perfect power
	for i in xrange(3, long(sqrt(N))):
		tmp = 1
		while tmp < N:
			tmp = tmp * i
			if(tmp == N):
				return False

	# compute r, u
	r, u = 0, N-1

	while u % 2 == 0:
		r += 1
		u /= 2

	# loop 
	for i in xrange(t):
		a = randrange(1, N - 1)
		if gcd(N, a) != 1:
			return False
		# strong witness
		x = pow(a, u, N)
		if x == 1 or x == N - 1:
			continue
		for j in xrange(r - 1):
			x = pow(x, 2, N)
			if x == N - 1:
				break
		else:
			return False
	# prime
	return True

def findStrongLiarWitness(N):

	strong_liars = []
	strong_witness = []

	if (N % 2 == 0):
		print "Even number"
		return

	# compute r, u
	r, u = 0, N-1

	while u % 2 == 0:
		r += 1
		u /= 2

	for a in xrange(1, N - 1):
		if gcd(N, a) != 1:
			strong_witness.append(a)
			continue
		x = pow(a, u, N)
		for j in xrange(r - 1):
			x = pow(x, 2, N)
			if x == N - 1:
				break
		else:
			strong_witness.append(a)
			continue
		strong_liars.append(a)

	print "Strong Liars: ", strong_liars
	print "Strong Witness: ", strong_witness

	return

def findNextPrime(N):
	if N % 2 == 1:
		N += 1
	N += 1
	while True:
		if MillerRabin(N):
			print "Next prime:", N
			return
		N += 2

def main():
	print "Input a positive integer:",
	# Part a)
	N = int(raw_input())
	if MillerRabin(N):
		print "Prime"
	else:
		print "Composite"

	# Part b)
	findNextPrime(N)

	# Part c)
	if MillerRabin(N):
		print "Number is prime"
	else:
		findStrongLiarWitness(N)
	

if __name__ == '__main__':
	main()