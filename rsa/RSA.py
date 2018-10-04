
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

			Pi = [1,0]
			Qi = [0,1]

			for x in qi:
				t = self.mult(x, Qi[1], N)
				Qi = [Qi[1], self.reduct(t + Qi[0], N)]
				t = self.mult(x, Pi[1], N)
				Pi = [Pi[1], self.reduct(t + Pi[0], N)]

			return self.reduct(((-1)**count)*Qi[0], N), a_p

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

		d = ar.gcd((self.p - 1)*(self.q - 1), 3)[0]

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

	value k any integer greater than 1 -->> k = 2,3,4... (whatever)

	by default k = 3

	returns result of exponentaion
	"""

	j = b**k

	g = []

	for i in range(j):
		g.append(fill(bin(i)[2:], k))

	print(g)

	return 0


def slidig_W(n, e, b = 2):
	"""exponentation with sliding windows method
	by default with binary base -->> b = 2

	returns result of exponentaion
	"""

	return 0


def MP(a, b):
	"""montgomery's product

	returns result of the product
	"""

	return 0


def ME(n, e, b = 2):
	"""exponentation with montgomery's exponentation
	by default with binary base -->> b = 2

	returns result of exponentaion
	"""

	return 0

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


if __name__ == "__main__":
	main()