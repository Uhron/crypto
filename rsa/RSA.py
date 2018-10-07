
##############		ARITMETIC		##############

class Aritmetic:
	""" modular aritmetic
	functions: reduct, mult, div, gcd.
	"""

	def __init__(self):
		""" init function

		no returns
		"""


	def reduct(self, p, N):
		""" reduces the number p on N
		returns p reducted
		"""

		return p % N


	def mult(self, p1, p2, N):
		""" multiply the numbers in module N -->> (p1 * p2) mod(N) = c
		returns c, result of multiplication
		"""

		p1 = self.reduct(p1, N)

		p2 = self.reduct(p2, N)

		m = p1 * p2

		return self.reduct(m, N)


	def idiv(self, p1, p2, N):
		""" divide the numbers -->> a = bq + r
		-->> (a // b) mod(N)
		returns q (enter)
		"""

		m = p1 // p2

		return self.reduct(m, N)


	def fdiv(self, p1, p2, N):
		""" divide the numbers -->> a = bq + r
		-->> (a / b) mod(N)
		returns q (float)
		"""

		m = p1 / p2

		return self.reduct(m, N)


	def gcd(self, a, b, N = None):
		""" greater common divisor between a and b
		Extended euclidean algorithm and Bezout identity -->> ax + by = gcd(a,b)
		if b has inverse: return Qi, gcd(a, b)
		else: return 0, 0, gcd(a, b)
		"""

		if a == 0 or b == 0:

			return 0, a

		if N == None:
			N = max([a,b])

		if a < b:
			a, b = b, a

		a_p = a
		b_p = b

		qi = []

		count = 0
		
		while True:
			q = self.idiv(a_p, b_p, N)

			r = self.reduct(a_p, b_p)

			qi.append(q)

			a_p, b_p = b_p, r

			if r == 0:
				break

			count = count + 1

		if a_p == 1:

			Qi = [1,0]
			Pi = [0,1]

			for x in qi:
				t = x * Qi[1]
				Qi = [Qi[1], t + Qi[0]]
				t = x * Pi[1]
				Pi = [Pi[1], t + Pi[0]]

			return (((-1)**(count))*Pi[0]), (((-1)**(count+1))*Qi[0]), a_p

		else:
			return 0, 0, a_p

ar = Aritmetic()

##############		ARITMETIC		##############

#################		RSA		 #################

class RSA:
	"""implementations of RSA
	"""

	def __init__(self, p = 23, q = 11):
		""" init function, parameters 2 prime numbers and coprimers between each other

		by default q = 11 and p = 23

		no returns
		"""

		self.q = q

		self.p = p


	def key_generation(self):
		"""Generate N = p*q and compute fi(N) = (p - 1)*(q - 1)
		e = 3 such that 1 < e < fi(N) and gcd(e, fi(N)) = 1
		determine d -->> e^-1 mod fi(N)

		return e, d, N, fi(N)
		"""

		e = 3

		N = self.p * self.q

		fi_N = (self.p - 1)*(self.q - 1)

		d = ar.reduct(ar.gcd((self.p - 1)*(self.q - 1), 3)[0], fi_N)

		return e, d , N, fi_N


	def SFM(self):
		"""RSA involves a public key and a private key

		Straight Forward Method implemention

		e, N are released as the public key
		d is kept as the private key exponent

		return 0
		"""

		e, d, N, fi_N = self.key_generation()

		m = 3

		print("text:			" + str(m))

		c = pow(m, e, N)
		print("ciphered text:		" + str(c))

		m = pow(c, d, N)
		print("desciphered text:	" + str(m))

		s = pow(m, d, N)
		print("signed text:		" + str(s))

		v = pow(s, e, N)
		print("verifyed signed text:	" + str(v == m))

		return 0


	def op_crt(self, m, d, N):
		"""Chinese Remaider Theorem implemention

		It only can be done in private cases cause works with
		private key, p and q (private parameters).

		To encipher you (in real life theoretically) don't know the privates parameters

		return desciphered or signed m
		"""

		#deconstruct d
		dp = ar.reduct(d, (self.p - 1))
		dq = ar.reduct(d, (self.q - 1))

		#deconstruct m
		mp = ar.reduct(m, self.p)
		mq = ar.reduct(m, self.q)

		#invert q
		q_inv = ar.gcd(self.q, self.p)[0]

		#efficient decription
		sp = pow(mp, dp, self.p)
		sq = pow(mq, dq, self.q)

		h = ar.mult(q_inv, (sp - sq), self.p)
		x = sq + h * self.q

		return x


	def CRT(self):
		"""RSA involves a public key and a private key

		Chinese Remaider Theorem implemention

		e, N are released as the public key
		d is kept as the private key exponent

		return 0
		"""

		e, d, N, fi_N = self.key_generation()

		m = 3

		print("text:			" + str(m))

		c = pow(m, e, N)
		print("ciphered text:		" + str(c))

		#########	CRT optimitation	#########

		m = self.op_crt(c, d, N)

		#########	CRT optimitation	#########

		print("desciphered text:	" + str(m))

		#########	CRT optimitation	#########

		s = self.op_crt(m, d, N)

		#########	CRT optimitation	#########

		print("signed text:		" + str(s))

		v = pow(s, e, N)
		print("verifyed signed text:	" + str(v == m))

		return 0

rsa = RSA()

#################		RSA		 #################

###########		EXPONENTATION METHODS	##########

def fill(p, fill):
	""" fill with 0 polinomyal with len less than eight
	returns p filled with len equal than irreductible polynomial
	"""

	while(len(p) < fill):
			p = '0' + p

	return p


def concatenate_list_data(list):
	""" concatenate list data, concatenate all data in a list into one string
	Returns string of concatenated data
	"""
	result = ''

	for element in list:

		result += str(element)

	return result


#split string in substrings of n characters no matters what
split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]


def split_string_0(x, n):
	""" split string in substring of n characters if it starts with 1,
	if starts with 0 give a substring with only a zero

	return aray with substrins
	"""

	res = []
	i, pos = 0, 0

	while pos < len(x):

		if x[pos] != '0':
			i = pos
			pos += (n - 1)

		else:
			i = pos

		res.append(x[i:pos + 1])
		pos += 1

	return res


def L2R(n, e, m):
	""" exponentation with square and multiply method
	implementation left to rigth

	returns result of exonentation
	"""

	e = bin(e)[2:]

	A = 1
	for b in e:

		A = ar.mult(A, A, m)

		if b == '1':
			A = ar.mult(A, n, m)

	print("L2R -->> " + str(A))

	return A


def R2L(n, e, m):
	""" exponentation with square and multiply method
	implementation rigth to left

	returns result of exonentation
	"""

	e = reversed(bin(e)[2:])

	A = 1
	for b in e:

		if b == '1':
			A = ar.mult(A, n, m)

		n = ar.mult(n, n, m)

	print("R2L -->> " + str(A))

	return A


def Ladder_M(n, e, m):
	"""exponentaion like square and multiply method 
	but with atomic operations.

	Montgomery's Ladder Technique

	returns result of exponentation
	"""

	e = bin(e)[3:]

	A = n
	B = ar.mult(n, n, m)

	for b in e:

		if b == '1':
			A = ar.mult(A, B, m)
			B = ar.mult(B, B, m)

		else:
			B = ar.mult(A, B, m)
			A = ar.mult(A, A, m)

	print("Ladder M. -->> " + str(A))

	return A


def K_ary(n, e, m, b = 2, k = 3):
	"""exponentation with K-ary method
	by default with binary base -->> b = 2

	value k any integer greater o requal than 1 -->> k = 2,3,4... (whatever)

	by default k = 3

	returns result of exponentaion
	"""

	#precomputation
	e = bin(e)[2:]

	while len(e)%k != 0:
		e = fill(e, len(e) + 1)

	e = concatenate_list_data(list(reversed(e)))

	e = split_string(e, k)

	e = list(reversed(e))

	for i in range(len(e)):
		e[i] = concatenate_list_data(list(reversed(e[i])))

	j = b**k

	g = {}

	g[fill(bin(0)[2:], k)] = 0

	for i in range(1, j):
		g[fill(bin(i)[2:], k)] = ar.reduct(n**i, m)

	#begin the algorithm
	A = g[e[0]]

	for i in range(1, len(e)):

		A = ar.mult(ar.reduct(A**j, m), g[fill(e[i], k)], m)

	print("K_ary -->> " + str(A))

	return A


def slidig_W(n, e, m, b = 2, k = 3):
	"""exponentation with sliding windows method
	by default with binary base -->> b = 2

	value k any integer greater o requal than 1 -->> k = 2,3,4... (whatever)

	by default k = 3

	returns result of exponentaion
	"""

	#precomputation
	e = concatenate_list_data(list(reversed(bin(e)[2:])))

	e = split_string_0(e, k)

	e = list(reversed(e))

	for i in range(len(e)):
		e[i] = concatenate_list_data(list(reversed(e[i])))

	j = b**k

	g = {}

	g[fill(bin(0)[2:], k)] = 0

	for i in range(1, j):
		g[fill(bin(i)[2:], k)] = ar.reduct(n**i, m)

	#begin the algorithm
	A = g[fill(e[0], k)]

	for i in range(1, len(e)):

		if e[i] == '0':
			A = ar.mult(A, A, m)

		else:
			A = ar.mult(A**j, g[fill(e[i], k)], m)

	print("sliding window -->> " + str(A))

	return A


def MP(a, b, n, r):
	"""montgomery's product

	Calculate n' so that r*r^-1 - n*n' = 1

	returns a*b*r^1 mod m
	"""

	#r = 2

	#while r <= n:
	#	r = r << 1

	#compute a and b in Montgomerys' space
	a = ar.mult(a,r,n)
	b = ar.mult(b,r,n)

	#print("r -->> " + str(r) + "; n -->> " + str(n))

	n_p, r_inv = ar.gcd(r, n, n)[:2]

	#print("r_inv -->> " + str(r_inv) + "; n_p -->> " + str(n_p))

	n_p = -n_p

	t = a * b

	m = t * n_p % r

	u = (t + m * n) / r

	while u > n:
		u = u - n

	u_real = ar.mult(u,r_inv,n)
	#print("expected u -->> " + str(ar.mult(t,r_inv,n)))
	#print("MP u (M.s' space)-->> " + str(u))
	print("real space u -->> " + str(u_real))

	return u_real


def ME(n, e, m, b = 2):
	"""exponentation with montgomery's exponentation
	by default with binary base -->> b = 2

	returns result of exponentaion
	"""

	e = bin(e)[2:]

	r = 2

	while r <= m:
		r = r << 1

	x = MP(n, r**2, m, r)

	A = MP(1, r**2, m, r)

	for b in e:

		A = MP(A, A, r, r)

		if b == '1':
			A = MP(A, n, r, r)

	A = MP(A, 1, m, r)

	print("ME -->> " + str(A))

	return A


###########		EXPONENTATION METHODS	##########


def main():
	"""call at all functions to test it

	returns nothing
	"""
	
	print("RSA_SFM implementation : \n")
	rsa.SFM()
	print("\nRSA_SFM end --------\n\n")

	print("RSA_CRT implementation : \n")
	rsa.CRT()
	print("\nRSA_CRT end --------\n\n")

	print("L2R implementation: values -->> 45^23 mod 13\n")
	L2R(45, 23, 13)
	print("expected res -->> " + str(pow(45, 23, 13)))
	print("\nL2R end ------------\n\n")

	print("R2L implementation: values -->> 8^13 mod 67\n")
	R2L(8, 13, 67)
	print("expected res -->> " + str(pow(8, 13, 67)))
	print("\nR2L end ------------\n\n")

	print("Ladder M. implementation: values -->> 73^7 mod 31\n")
	Ladder_M(73, 7, 31)
	print("expected res -->> " + str(pow(73, 7, 31)))
	print("\nLadder M. end ------------\n\n")

	print("K-ary implementation: values -->> 34^11 mod 29; k = 3 and b = 2 (binary)\n")
	K_ary(34, 11, 29)
	print("expected res -->> " + str(pow(34, 11, 29)))
	print("\nK-ary end ------------\n\n")

	print("Sliding window implementation: values -->> 54^17 mod 19; k = 3 and b = 2 (binary)\n")
	slidig_W(54, 17, 19)
	print("expected res -->> " + str(pow(54, 17, 19)))
	print("\nK-ary end ------------\n\n")

	print("Montgomery product: values -->> 43 * 59 mod 97\n")
	#r = 2
	#while r <= m:
	#	r = r << 1
	r = 100
	MP(43, 56, 97, r)
	print("expected res -->> " + str(pow((43*56), 1, 97)))
	print("\nK-ary end ------------\n\n")

	print("Montgomery exponentation: values -->> 73^7 mod 31\n")
	ME(73, 7, 31)
	print("expected res -->> " + str(pow(73, 7, 31)))
	print("\nK-ary end ------------\n\n")


if __name__ == "__main__":
	main()
