from hashlib import sha256
from random import getrandbits

KEY_BIT_LENGTH = 10

def get_hash(msg):
	m = sha256()
	m.update(msg)
	return m.hexdigest()

def commit(key, msg):
	h1 = get_hash(msg)

	print('h1', h1)

	h2 = get_hash(key)
	print('h2', h2)

	m3 = h1 + h2
	print('m3:',m3)
	com = get_hash(m3)

	return com

def verify(com, key, msg):
	com_new = commit(key, msg)
	return com == com_new

def get_key(bit_len):
	return getrandbits(bit_len)

def main():
	msg = 'Attack at Dawn'
	key = str(get_key(KEY_BIT_LENGTH))
	com = commit(key, msg)
	print('Final commitment:', com)
	print('Result of verify is:', verify(com, key, msg))

if __name__ == '__main__':
	main()