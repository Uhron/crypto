
##############		KEY		##############

K = [	[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1]]

##############		KEY		##############

##############		AFINE MATRIX		##############

A = [	[1,0,0,0,1,1,1,1],
		[1,1,0,0,0,1,1,1],
		[1,1,1,0,0,0,1,1],
		[1,1,1,1,0,0,0,1],
		[1,1,1,1,1,0,0,0],
		[0,1,1,1,1,1,0,0],
		[0,0,1,1,1,1,1,0],
		[0,0,0,1,1,1,1,1]]

b = [1,1,0,0,0,1,1,0]#nº 99 hex(63)

C = [	[0,0,1,0,0,1,0,1],
		[1,0,0,1,0,0,1,0],
		[0,1,0,0,1,0,0,1],
		[1,0,1,0,0,1,0,0],
		[0,1,0,1,0,0,1,0],
		[0,0,1,0,1,0,0,1],
		[1,0,0,1,0,1,0,0],
		[0,1,0,0,1,0,1,0]]

d = [1,0,1,0,0,0,0,0]#nº 160 hex(A0)

##############		AFINE MATRIX		##############

##############		MIX COLUMNS		##############

MC = [	[[1,0], [1,1], [0,1], [0,1]],
		[[0,1], [1,0], [1,1], [0,1]],
		[[0,1], [0,1], [1,0], [1,1]],
		[[1,1], [0,1], [0,1], [1,0]]]

MC_inv = [	[[1,1,1,0], [1,0,1,1], [1,1,0,1], [1,0,0,1]],
			[[1,0,0,1], [1,1,1,0], [1,0,1,1], [1,1,0,1]],
			[[1,1,0,1], [1,0,0,1], [1,1,1,0], [1,0,1,1]],
			[[1,0,1,1], [1,1,0,1], [1,0,0,1], [1,1,1,0]]]

##############		MIX COLUMNS		##############

##############		ARITMETIC		##############

class Aritmetic:
	""" modular aritmetic Z2/Z

	construct with a polinomyal by parameter or take x⁸ + x⁴ + x³ + x + 1 by default
	functions: xorit, reduct, mult, div, gcd.
	"""

	def __init__(self, p_irreductible = [1,0,0,0,1,1,0,1,1]):
		""" init function, init irreductible polynomial to x⁸ + x⁴ + x³ + x + 1

		no returns
		"""

		self.p_irreductible = p_irreductible
		self.substitution = [0] + p_irreductible[1:]


	def fill(self, p, fill = None):
		""" fill with 0 polinomyal with len less than nine

		returns p filled with len equal than irreductible polynomial
		"""

		if fill == None:
				fill = len(self.p_irreductible) - 1

		while( len(p) < fill):
				p.insert(0, 0)

		return p


	def fit(self, p):
		""" fit polynomial array to first 1

		returns p fit to first significant bit
		"""

		for x in range(len(p)):
			if p[0] == 0:
				del p[0]

			else: 
				break

		return p


	def xorit(self, a, b):
		""" xor two arrays of bits

		a and b must have the same length

		returns result of xor a and b
		"""

		xored = []

		for x in range(len(a)):
			xored.append(int(a[x]) ^ int(b[x]))

		return xored


	def reduct(self, p):
		""" reduces the polynomial p

		returns p reducted
		"""

		if len(p) <= len(self.p_irreductible):

			p = self.fill(p)

			if p[0] == 1:
				p[0] = 0
				p = self.xorit(p, self.substitution)

		else:
			while(len(p) > (len(self.p_irreductible) - 1)):
				
				if p[0] == 1:
					pad = len(p) - len(self.p_irreductible)
					tmp = self.substitution + [0]*pad
					tmp = self.fill(tmp, len(p))
					p = self.xorit(p, tmp)
					p[0] = 0

				else:
					del p[0]

		return self.fill(p)


	def mult(self, p1, p2):
		""" multiply the polynomials -->> p1 * p2 = c

		returns c, result of multiplication
		"""

		c = [0] * (len(p1) + len(p2) - 1)

		for i in range(len(p1)):
			if p1[i] == 1:

				for x in range(len(p2)):	
					if p2[x] == 1:
						
						c[i + x] = 1 ^ c[i + x]

		return c


	def div(self, a, b = None):
		""" divide the polynomials -->> a = bq + r

		returns a, b, q, r; reult of division
		"""

		if b == None:
			b = self.p_irreductible

		q = [0] * (len(a) + len(b))

		r = a
		a = self.fit(a)
		b = self.fit(b)

		grade = len(a) - len(b)

		while True:

			tmp = [1] + [0] * grade

			t = self.mult(b, tmp)

			res = self.xorit(t, r)

			r = self.fit(res)

			grade = len(r) - len(b)

			q = self.xorit(q, self.fill(tmp, len(q)))

			if grade < 0:
				break

		return a, b, self.fit(q), r


	def gcd(self, a, b):
		""" greater common divisor between a and b

		Extended euclidean algorithm and Bezout identity -->> ax + by = gcd(a,b)

		if b has inverse: return Pi, Qi, gcd(a, b)

		else: return 0, 0, gcd(a, b)
		"""

		if len(self.fit(a)) == 0 or len(self.fit(b)) == 0:

			return [0,0,0,0,0,0,0,0]

		a_p = a
		b_p = b

		qi = []
		
		while True:
			a_p, b_p, q, r = self.div(a_p, b_p)

			qi.append(q)

			a_p, b_p = b_p, r

			if len(r) == 0:
				break

		if len(a_p) == 1 and a_p[0] == 1:

			Pi = [[1],[0]]
			Qi = [[0],[1]]

			for x in qi:
				t = self.mult(x, Qi[1])
				Qi = [Qi[1], self.xorit(t,self.fill(Qi[0],len(t)))]
				t = self.mult(x, Pi[1])
				Pi = [Pi[1], self.xorit(t,self.fill(Pi[0],len(t)))]

			return Qi[0]

		else:
			return 0, 0, a_p


ar = Aritmetic()

##############		AITMETIC		##############


def int_to_bitarray(n):
	return [int(digit) for digit in bin(n)[2:]]


def concatenate_list_data(list):
	""" concatenate list data, concatenate all data in a list into one string

	Returns string of concatenated data
	"""
	result = ''

	for element in list:

		result += str(element)

	return result


def subBytes(x):
	""" subBytes function -->> x * v = 1 mod( ar.p_irreductible ) 
	-->> y = A * v + b

	return y
	"""
	v = ar.fit(ar.gcd(ar.p_irreductible, x))

	Ax = []
	
	for p in A:
		tmp = []

		for i in range(len(v)):
			tmp.append(v[-i-1] and p[i])

		t = 0
		for i in tmp:
			t = t ^ i
		Ax.append(t)
	
	Ax = ar.xorit(Ax, b)
	Ax.reverse()
	return Ax


def sBox_gen():
	""" generate sBox of AES with subByte function trying all combinations

	returns sBoxes
	"""

	s_box = []

	for x in range(256):
		x = int_to_bitarray(x)
		x = ar.fill(x)
		s_box.append(subBytes(x))

	return s_box


def shiftRows(a):
	""" shift each row of a Nr times

	return a shifted
	"""

	for x in range(len(a)):
		a[x] = a[x][x:] + a[x][:x]

	return a


def mixColumns(a):
	""" linear function to diffus input

	return a mixed
	"""

	B = [[0,0,0,0]]*4

	for i in range(4):

			B[i] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[0][0]), ar.mult(a[i + 4], MC[0][1])), ar.mult(a[i + 8], MC[0][2])), ar.mult(a[i + 12], MC[0][3])))
			B[i + 4] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[1][0]), ar.mult(a[i + 4], MC[1][1])), ar.mult(a[i + 8], MC[1][2])), ar.mult(a[i + 12], MC[1][3])))
			B[i + 8] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[2][0]), ar.mult(a[i + 4], MC[2][1])), ar.mult(a[i + 8], MC[2][2])), ar.mult(a[i + 12], MC[2][3])))
			B[i + 12] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[3][0]), ar.mult(a[i + 4], MC[3][1])), ar.mult(a[i + 8], MC[3][2])), ar.mult(a[i + 12], MC[3][3])))

	print(hex(int(concatenate_list_data(B),2)))

	return B


def KSC(B, i, s_box):
	""" Key schedule core to generate round key

	returns key rounded
	"""

	t = B
	t = t[8:] + t[:8]

	res = []
	for x in range(4):
		pos = int(concatenate_list_data(t[(x * 8):(x * 8) + 8]), 2)
		res = res + s_box[pos]

	t = res[:8]
	del res[:8]

	r = int_to_bitarray(2 ** (i - 1))

	r = ar.xorit(t,ar.fill(r))

	return r + res


def key_gen(s_box):
	""" key generation 

	returns expaned key
	"""

	Nk = 4
	EK = [K[0] + K[4] + K[8] + K[12], K[1] + K[5] + K[9] + K[13], K[2] + K[6] + K[10] + K[14], K[3] + K[7] + K[11] + K[15]]
	t_pp = K[3] + K[7] + K[11] + K[15] 

	for x in range(4, 44, 4):
			t = KSC(t_pp, (x//Nk), s_box)
			t = ar.xorit(t,EK[x-Nk])
			EK.append(t)

			for i in range(3):
				print("i -->> " + str(i))
				print("x -->> " + str(x))
				print("pos -->> " + str(x+i-Nk))
				print("len EK -->> " + str(len(EK)) + "\n")
				t = ar.xorit(t,EK[x+i-Nk])
				EK.append(t)
				t_pp = t

	return EK


def addRoundKey(state, key):

	for x in range(len(state)):
		


def AES(input, s_box):
	""" AES function, AES implementation

	returns AES output
	"""

	ek = key_gen(s_box)

	state = []



	#addRoundKey

	for i in range(10):

		s = []

		for row in state:
			s.append(subBytes(row))

		s = shiftRows(s)
		s = mixColumns(s)

		#addRoundKey

		state = s

	s = []

	for row in state:
		s.append(subBytes(row))
	
	s = shiftRows(s)

	#addRoundKey

	return s

def main():
	input = "10"*64 #128

	s_box = sBox_gen()

	AES(input, s_box)


if __name__ == "__main__":
	main()