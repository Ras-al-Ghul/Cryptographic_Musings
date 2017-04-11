import time, random

p = 37
gen = 5

def isPrime(n):
	if n == 1:
		return False
	for i in range(2, n):
		if n % i == 0:
			return False
	return True

def modExp(gen, pows, pri):
	ans = 1
	for i in range(1, pows+1):
		ans = (ans*gen)%pri
	return ans

def isGen(p, gen):
	setZ = set()
	for i in range(1, p):
		setZ.add(modExp(gen, i, p))
	if len(setZ) == p-1:
		return True
	return False

def checkPrimeAndGen(p, gen):
	if not isPrime(p):
		return False
	if not isGen(p, gen):
		return False
	return True

if __name__ == '__main__':
	random.seed(time.time())
	if checkPrimeAndGen(p, gen):
		a = random.randint(1, p-1)
		b = random.randint(1, p-1)
		A = modExp(gen, a, p)
		B = modExp(gen, b, p)
		print "Answer to part a)"
		print "B's session key", modExp(A, b, p), "and A's session key", modExp(B, a, p)

		print "\nAnswer to part b)"
		print "MITM:"
		c = random.randint(1, p-1)
		C = modExp(gen, c, p)
		print "A originally sends A =", A, "towards B"
		print "C intercepts", A
		print "\nC now sends C =", C, "towards B"
		print "B receives", C
		print "B's session key (C^b)mod(p) which it assumes to be with A but is actually with C", modExp(C, b, p)
		print "\nB sends B =", B, "towards A"
		print "C intercepts", B
		print "C's session key with B (B^c)mod(p) which is equal to B's assumed session key", modExp(B, c, p)
		print "\nC now sends C =", C, "towards A"
		print "C's session key with A (A^c)mod(p) which will be equal to A's assumed session key", modExp(A, c, p)
		print "A receives", C
		print "A's session key (C^a)mod(p) which it asssumes to be with B but is actually with C", modExp(C, a, p)
		print "\nUltimately, C has a session key with A and with B. Whatever it gets from A using its session key with A,\
		it intercepts, decrypts, and finally encrypts it again appropriately using its session key with B. Ditto other way around"