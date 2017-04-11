from math import ceil, sqrt
p = 37
g = 5
h = 13

# p= 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
# g= 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
# h= 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333

sqrtp = int(ceil(p**0.5))
# sqrtp = 2**20

def powmod(b,e,n):
	"""powmod(b,e,n) computes the eth power of b mod n.  
	(Actually, this is not needed, as pow(b,e,n) does the same thing for positive integers.
	This will be useful in future for non-integers or inverses."""
	accum = 1; i = 0; bpow2 = b
	while ((e>>i)>0):
		if((e>>i) & 1):
			accum = (accum*bpow2) % n
		bpow2 = (bpow2*bpow2) % n
		i+=1
	return accum
	
def xgcd(a,b):
	"""xgcd(a,b) returns a list of form [g,x,y], where g is gcd(a,b) and
	x,y satisfy the equation g = ax + by."""
	a1=1; b1=0; a2=0; b2=1; aneg=1; bneg=1; swap = False
	if(a < 0):
		a = -a; aneg=-1
	if(b < 0):
		b = -b; bneg=-1
	if(b > a):
		swap = True
		[a,b] = [b,a]
	while (1):
		quot = -(a / b)
		a = a % b
		a1 = a1 + quot*a2; b1 = b1 + quot*b2
		if(a == 0):
			if(swap):
				return [b, b2*bneg, a2*aneg]
			else:
				return [b, a2*aneg, b2*bneg]
		quot = -(b / a)
		b = b % a;
		a2 = a2 + quot*a1; b2 = b2 + quot*b1
		if(b == 0):
			if(swap):
				return [a, b1*bneg, a1*aneg]
			else:
				return [a, a1*aneg, b1*bneg]

def main():
	print "Following are the input sizes"
	print "Length of Prime p in (Zp)",len(str(p))
	print "Length of Generator g",len(str(g))
	print "Length of h, an element of (Zp)",len(str(h))

	# find (g^j)modp for all possible js where j is atmost sqrtp
	gjs = []
	for i in xrange(sqrtp):
		gjs.append(powmod(g, i, p))

	# find inverses for all of the above gjs i.e. calc inv such that (g^j).inv = 1modp(p)
	gminusjs = []
	for i in gjs:
		# xgcd(a,b) - Find [g,x,y] such that g=gcd(a,b) and g = ax + by. We know inv = x
		gminusjs.append(xgcd(i, p)[1]) 

	# more efficient - comment out above two parts - here - find ginv and then do (ginv^j) = (g^-j)mod(p)
	# ginv = xgcd(g, p)[1]
	# gminusjs = []
	# for i in xrange(sqrtp):
	# 	gminusjs.append(powmod(ginv, i, p))
	
	# multiply all elements by h and take mod(p)
	gminusjsh = []
	for i in gminusjs: 
		gminusjsh.append(h * i % p)

	# construct the list for the other side
	gpowersqrtp = powmod(g, sqrtp, p) ### (g^sqrt(p))mod(p) 
	otherside = []
	for i in xrange(sqrtp):
		otherside.append(powmod(gpowersqrtp, i, p))

	# Start Searching
	print "Meet in the middle search"
	for i in xrange(sqrtp):
	    if otherside[i] in gminusjsh: # if LHS = RHS
	        j = gminusjsh.index(otherside[i])
	        print "Value of i =",i
	        print "Value of j =",j
	        print "Value of x = ",i*sqrtp + j
	        break

if __name__ == '__main__':
	main()