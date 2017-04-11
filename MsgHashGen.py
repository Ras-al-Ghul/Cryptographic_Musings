from hashlib import sha1


def hash_short(message, length=16):
    return sha1(message).hexdigest()[:length/4]

def main():
	m1 = u'This is a totally irregular , message.'
	# m1 = u'previously mentioned is a \n totally   random message.   \n'
	# m1 = '\n This , \n is a \n totally random message.'
	# m1 = u'\n that is a completely incidental message.'
	m2 = u'This is \n a exactly random e-mail'
	# m2 = u'This \n is a \n \n , totally , incidental message. \t'
	# m2 = 'This is a \n totally random message.'
	# m2 = u'This   is   a \n utterly random message.'
	
	print('Message:', m1)
	print('Its hash:', hash_short(m1))
	print('Message:', m2)
	print('Its hash:', hash_short(m2))

if __name__ == '__main__':
	main()