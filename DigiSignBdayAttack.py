from hashlib import sha1
from random import randint, choice
from PyDictionary import PyDictionary

def hash_short(message, length=16):
    return sha1(message).hexdigest()[:length/4]


def insert_random_chars(msg):
	random_chars = ['\n', '\t', ' ', ',']
	for i in xrange(randint(0, len(msg))):
		msg.insert(randint(0, len(msg)), choice(random_chars))

def replace_with_synonyms(msg, dictionary):
	for i in xrange(randint(0, len(msg))):
		idx = randint(0,len(msg)-1)
		word = msg[idx]
		synonyms = dictionary.synonym(word)
		if synonyms != None:
			msg[idx] = choice(synonyms)

def main():
	m1 = "This is a totally random message."

	h1 = hash_short(m1)

	hash_list = []

	dictionary = PyDictionary()

	for i in xrange(500):

		msg = m1
		msgsplit = msg.split()
		replace_with_synonyms(msgsplit, dictionary)

		insert_random_chars(msgsplit)
		msg = " ".join(msgsplit)
		if msg == m1:
			continue

		print("iter:", i, "random message:", msg)
		h2 = hash_short(msg)
		print "hash:", h2
		hash_list.append([h2, msg])
		
		if h2 == h1:
			print "Collision found"
			print "Original Message:", m1
			print "Collision causing message:", msg
			break

		flag = 0
		for i in xrange(len(hash_list) - 1):
			if hash_list[i][0] == h2 and hash_list[i][1] != msg:
				print "Collision found"
				print hash_list[i], "\n", msg, "\n", h2
				break
		else:
			continue

		break

if __name__ == '__main__':
	main()