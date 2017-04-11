from math import ceil
from random import randint, choice, getrandbits
from hashlib import sha256

KEY_BIT_LENGTH = 10

def generate_primes(a, b):
	primes = [True] * b
	b_root = b ** 0.5
	primes[0] = primes[1] = False
	for i in xrange(2, int(ceil(b_root))):
		if primes[i]:
			idx = i*i
			for j in xrange(idx, b, i):
				primes[j] = False
	output = []
	for i in xrange(a, b):
		if primes[i]:
			output.append(i)
	return output

def check_co_prime(a, b):
	for i in xrange(2, min(a,b) + 1):
		if a%i==0 and b%i==0:
			return False
	return True

def generate_keys(length):
	n_min = 2**(length - 1)
	n_max = (2**length) - 1

	# Now need to find two primes p,q s.t. p*q=n, and n has no. of bits = length

	# p and q vary by atmost 2 bits
	f_min = 2**(length//2 - 1)
	f_max = 2**(length//2 + 1)

	primes = generate_primes(f_min, f_max)
	p = q = 0
	flag = False
	while len(primes) > 0:
		idx = randint(0, len(primes))
		p = primes[idx]
		primes.pop(idx)
		possible_q = []
		for i in xrange(len(primes)):
			q = primes[i]
			n = p * q
			if n >= n_min and n <= n_max:
				possible_q.append(q)
		if possible_q:
			q = choice(possible_q)
			flag = True
			break

	if flag == False:
		raise AssertionError("Cannot find p and q for given length")

	n = p * q
	print('p:',p,' q:',q, 'n:', n)
	phi_n = (p-1) * (q-1)

	flag = False
	# Need to find an e which is coprime to phi_n
	print('Findig e')
	for e in xrange(3, phi_n, 2):
		if check_co_prime(e, phi_n):
			flag = True
			break

	if flag == False:
		raise AssertionError("Cannot find e")

	print('e:', e)
	# Find d corresponding to e
	flag = False
	print('Finding d')
	for d in xrange(3, phi_n, 2):
		if (e*d % phi_n) == 1:
			flag = True
			break

	if flag == False:
		raise AssertionError("Cannot find d")

	return n,e,d

def encrypt(m, n, e):
	return pow(m, e, n)

def decrypt(c, n, d):
	return pow(c, d, n)

def get_hash(msg):
	m = sha256()
	m.update(msg)
	return m.hexdigest()

def commit(key, msg):
	h1 = get_hash(msg)
	h2 = get_hash(key)

	m3 = h1 + h2

	return get_hash(m3)

def get_digital_sign(msg, n, d):
	int_msg = int(msg, 16)
	sign = encrypt(int_msg, n, d)
	hex_sign = "%x" % sign
	return hex_sign

def check_digital_sign(hexmsg, sign, n, e):
	print('Sign:', sign)
	int_sign = int(sign, 16) 
	int_dec_sign = decrypt(int_sign, n, e)
	hex_dec_sign = "%x" % int_dec_sign
	return hexmsg == hex_dec_sign

def signed_commit(key, msg, n, d):
	com = commit(key, msg)
	print('Commmit message:', com)
	# Very IMP - Verification fails when there is leading 0 in com
	sign = get_digital_sign(com, n, d)
	print('Sign:', sign)
	com = com + sign
	return com

def signed_verify(com, key, msg, n, e):
	len_com = 64
	h1 = com[0:len_com]
	h2 = com[len_com:]
	print('h1:', h1)
	print('h2:', h2)

	com_new = commit(key, msg)
	print('Calculated commitment:', com_new)
	return h1 == com_new and check_digital_sign(h1, h2, n, e)

def get_key(bit_len):
	return getrandbits(bit_len)

def main():
	# n,e,d = generate_keys(25)
	# print(n,e,d)

	n = 119294134840169509055527211331255649644606569661527638012067481954943056851150333806315957037715620297305000118628770846689969112892212245457118060574995989517080042105263427376322274266393116193517839570773505632231596681121927337473973220312512599061231322250945506260066557538238517575390621262940383913963
	e = 65537
	d = 72892162132453240003793081431254596487759129683932347592859641345891553040333172364830897044041106776409947506759374529741974962628265550289611864072595839380092878908763844906765562034782236695192158256372726552845451322975382692014652804746885831130782746696769480546157553394854115242420454633969276355353

	msg = 'Attack at Dawn'
	key = str(get_key(KEY_BIT_LENGTH))
	com = signed_commit(key, msg, n, d)
	print('Signed commit:', com)
	print('Verification', signed_verify(com, key, msg, n, e))

if __name__ == '__main__':
	main()