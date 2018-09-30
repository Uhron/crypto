
from random import randint

#############	 UTILE FUCTION 		#############

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

#############	 UTILE FUCTION 		#############


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

			if p[0] == 1 and len(p) != 8:
				p = self.xorit(p, self.substitution)
				del p[0]

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


##############		KEY		##############

K = [	ar.fill(int_to_bitarray(int("54",16))), ar.fill(int_to_bitarray(int("68",16))), ar.fill(int_to_bitarray(int("61",16))), ar.fill(int_to_bitarray(int("74",16))),
		ar.fill(int_to_bitarray(int("73",16))), ar.fill(int_to_bitarray(int("20",16))), ar.fill(int_to_bitarray(int("6D",16))), ar.fill(int_to_bitarray(int("79",16))),
		ar.fill(int_to_bitarray(int("20",16))), ar.fill(int_to_bitarray(int("4B",16))), ar.fill(int_to_bitarray(int("75",16))), ar.fill(int_to_bitarray(int("6E",16))),
		ar.fill(int_to_bitarray(int("67",16))), ar.fill(int_to_bitarray(int("20",16))), ar.fill(int_to_bitarray(int("46",16))), ar.fill(int_to_bitarray(int("75",16)))]

##############		KEY		##############


##############		MASK	##############

"""X = [ 	[1,1,1,1,1,1,1,1], [0,0,0,0,0,0,1,0], [0,0,0,0,1,0,0,0], [0,1,0,0,0,0,0,0],
		[0,0,1,0,0,0,0,0], [0,0,0,0,1,0,0,0], [0,0,1,0,0,0,0,0], [1,1,1,1,1,1,1,1],
		[1,1,1,1,1,1,1,1], [0,0,0,0,1,0,1,0], [1,0,0,0,0,0,0,0], [0,0,1,0,0,0,0,0],
		[0,0,0,0,0,0,1,0], [0,0,0,1,0,0,0,0], [1,1,1,1,1,1,1,1], [0,0,1,0,1,0,0,0]]"""

X = [ 	[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

##############		MASK	##############


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

MC = [	[[0,0,1,0],[0,0,1,1],[0,0,0,1],[0,0,0,1]],
		[[0,0,0,1],[0,0,1,0],[0,0,1,1],[0,0,0,1]],
		[[0,0,0,1],[0,0,0,1],[0,0,1,0],[0,0,1,1]],
		[[0,0,1,1],[0,0,0,1],[0,0,0,1],[0,0,1,0]]]

MC_inv = [	[[1,1,1,0],[1,0,1,1],[1,1,0,1],[1,0,0,1]],
			[[1,0,0,1],[1,1,1,0],[1,0,1,1],[1,1,0,1]],
			[[1,1,0,1],[1,0,0,1],[1,1,1,0],[1,0,1,1]],
			[[1,0,1,1],[1,1,0,1],[1,0,0,1],[1,1,1,0]]]

##############		MIX COLUMNS		##############

def genY():
	"""generate Y random not zero

	return Y generated
	"""

	Y = []

	for j in range(16):
		y = []

		while len(ar.fit(y)) == 0:
			y = []

			for i in range(8):
				y.append(randint(0,1))

		Y.append(ar.fill(y))

	return Y


def subBytes(a, inv):
	""" subBytes function with mask-->> a * v = 1 mod( ar.p_irreductible ) 
	-->> y = A * v + b

	return y
	"""

	if not inv :

		state = []
		for w in a:
			v = w

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

			state.append(Ax)

	else:

		state = []

		for w in a:
			v = w
			
			Ax = []
			for p in C:
				tmp = []

				for i in range(len(v)):
					tmp.append(v[-i-1] and p[i])

				t = 0
				for i in tmp:
					t = t ^ i

				Ax.append(t)
		
			Ax = ar.xorit(Ax, d)
			Ax.reverse()
			Ax = ar.fill(ar.gcd(ar.p_irreductible, Ax))

			state.append(Ax)

	return state


def maskSubBytes(aX, inv):
	"""Modified inversion in GF(2^8) with masking countermeasure

	return xor(B,X1)
	"""

	for i in range(len(X)):
		ar.fill(X[i])

	Y = genY()

	if not inv:
		res = []

		for w in range(len(aX)):

			Ax = ar.reduct(ar.mult(Y[w], aX[w]))

			yx = ar.reduct(ar.mult(Y[w], X[w]))

			Ay = ar.xorit(yx, Ax)

			Ay = ar.fill(ar.gcd(ar.p_irreductible, Ay))

			y_inv = ar.fill(ar.gcd(ar.p_irreductible, Y[w]))

			yx = ar.reduct(ar.mult(y_inv, X[w]))

			Ay = ar.xorit(yx, Ay)

			Ax = ar.reduct(ar.mult(Y[w], Ay))

			res.append(Ax)

	else:
		pass

	return subBytes(res, inv)


def sBox_gen(inv):
	""" generate sBox of AES with subByte function trying all combinations

	returns sBoxes
	"""

	s_box = []

	for x in range(256):
		x = int_to_bitarray(x)
		x = ar.fill(x)
		x = ar.fill(ar.gcd(ar.p_irreductible, x))
		s_box.append(x)

	return subBytes(s_box, inv)


def shiftRows(a, inv):
	""" shift each row of a Nr times

	return a shifted
	"""

	if not inv:

		for x in range(0, len(a), 4):
			a[x:x+4] = a[x:x+4][x//4:] + a[x:x+4][:x//4]

	else:
		for x in range(len(a), 0, -4):
			a[x:x+4] = a[x:x+4][4-(x//4):] + a[x:x+4][:4-(x//4)]

	return a


def mixColumns(a, inv):
	""" linear function to diffus input

	return a mixed
	"""

	B = [0]*16

	if not inv:

		for i in range(4):

				B[i] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[0][0]), ar.mult(a[i + 4], MC[0][1])), ar.mult(a[i + 8], MC[0][2])), ar.mult(a[i + 12], MC[0][3])))
				B[i + 4] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[1][0]), ar.mult(a[i + 4], MC[1][1])), ar.mult(a[i + 8], MC[1][2])), ar.mult(a[i + 12], MC[1][3])))
				B[i + 8] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[2][0]), ar.mult(a[i + 4], MC[2][1])), ar.mult(a[i + 8], MC[2][2])), ar.mult(a[i + 12], MC[2][3])))
				B[i + 12] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC[3][0]), ar.mult(a[i + 4], MC[3][1])), ar.mult(a[i + 8], MC[3][2])), ar.mult(a[i + 12], MC[3][3])))

	else:
		for i in range(4):

				B[i] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC_inv[0][0]), ar.mult(a[i + 4], MC_inv[0][1])), ar.mult(a[i + 8], MC_inv[0][2])), ar.mult(a[i + 12], MC_inv[0][3])))
				B[i + 4] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC_inv[1][0]), ar.mult(a[i + 4], MC_inv[1][1])), ar.mult(a[i + 8], MC_inv[1][2])), ar.mult(a[i + 12], MC_inv[1][3])))
				B[i + 8] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC_inv[2][0]), ar.mult(a[i + 4], MC_inv[2][1])), ar.mult(a[i + 8], MC_inv[2][2])), ar.mult(a[i + 12], MC_inv[2][3])))
				B[i + 12] = ar.reduct(ar.xorit(ar.xorit(ar.xorit(ar.mult(a[i], MC_inv[3][0]), ar.mult(a[i + 4], MC_inv[3][1])), ar.mult(a[i + 8], MC_inv[3][2])), ar.mult(a[i + 12], MC_inv[3][3])))

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

	r = ar.reduct(r)

	r = ar.xorit(t,r)	

	return r + res


def key_gen(s_box):
	""" key generation 

	returns expanedd key
	"""

	EK = [K[0] + K[1] + K[2] + K[3], K[4] + K[5] + K[6] + K[7], K[8] + K[9] + K[10] + K[11], K[12] + K[13] + K[14] + K[15]]


	t_p = EK[-1]
	Nk = 4

	for x in range(4, 44, 4):

		t = KSC(t_p, (x//Nk), s_box)
		t = ar.xorit(t, EK[x-Nk])
		EK.append(t)
		#print("k -->> " + str(hex(int(concatenate_list_data(t),2))[2:]) + ";")

		for i in range(1,4):
			t = ar.xorit(t, EK[x+i-Nk])
			EK.append(t)
			#print("k -->> " + str(hex(int(concatenate_list_data(t),2))[2:]) + ";")
			t_p = t
		#print("\n\n")

	tmp = []
	for x in range(0, 44, 4):
		t = []

		for i in range(4):
			n = [EK[x + i][:8], EK[x + i][8:][:8], EK[x + i][16:][:8], EK[x + i][24:][:8]]
			t.append(n)

		tmp.append(t)


	return tmp


def maskAddRoundKey(state, key, Xx):


	for i in range(len(X)):
		ar.fill(X[i])

	for i in range(len(state)):
		w = ar.xorit(state[i], key[i%4][i//4])
		w = ar.xorit(w, X[i])
		state[i] = ar.xorit(w, Xx[i])

	return state


def addRoundKey(state, key):

	for x in range(len(state)):
		state[x] = ar.xorit(state[x], key[x%4][x//4])

	return state


def computeX(inv):
	"""compute X1, X2 and X3 with X

	returns X1, X2, X3
	"""

	tmp = []
	for x in X:

		tmp.append(ar.fill(ar.gcd(ar.p_irreductible, x)))
	
	tmp = subBytes(tmp, inv)

	X1 = []

	x = b

	x.reverse()

	for w in tmp:	
		X1.append(ar.xorit(w, x))

	X2 = shiftRows(X1, inv)

	X3 = mixColumns(X2, inv)

	return X1, X2, X3

		
def AES(input, s_box):
	""" AES function, AES implementation

	returns AES ciphered output
	"""

	state = [	input[0], input[4], input[8], input[12],
				input[1], input[5], input[9], input[13],
				input[2], input[6], input[10], input[14],
				input[3], input[7], input[11], input[15]]

	ek = key_gen(s_box)

	X1, X2, X3 = computeX(False)

	s = []

	for i in range(len(X)):
		ar.fill(X[i])
		s.append(ar.xorit(state[i], X[i]))

	state = addRoundKey(s, ek[0])

	for b in state:
		print("st -->> " + str(0) + " : " + str(hex(int(concatenate_list_data(b), 2))[2:]) + ";")

	print("\n\n")

	for i in range(1,10):

		s = maskSubBytes(state, False)

		for n in range(len(s)):
			b = ar.xorit(s[n], X1[n])
			print("st -->> " + str(i) + " : " + str(hex(int(concatenate_list_data(b), 2))[2:]) + ";")

		print("\n\n")

		s = shiftRows(s, False)

		s = mixColumns(s, False)

		state = maskAddRoundKey(s, ek[i], X3)

		"""for n in range(len(s)):
			b = ar.xorit(s[n], X[n])
			print("st -->> " + str(i) + " : " + str(hex(int(concatenate_list_data(b), 2))[2:]) + ";")

		print("\n\n")"""


	s = subBytes(state, False)
 
	s = shiftRows(s, False)

	state = maskAddRoundKey(s, ek[10], X2)

	s = []

	for i in range(len(state)):
		s.append(ar.xorit(state[i], X[i]))

	state = [	s[0], s[4], s[8], s[12],
				s[1], s[5], s[9], s[13],
				s[2], s[6], s[10], s[14],
				s[3], s[7], s[11], s[15]]

	for b in state:
		print("b -->> " + str(10) + " : " + str(hex(int(concatenate_list_data(b),2))[2:]) + ";")

	print("\n\n")

	return state


def dAES(input, s_box):
	""" AES function, AES implementation

	returns AES clear output
	"""

	state = [	input[0], input[4], input[8], input[12],
				input[1], input[5], input[9], input[13],
				input[2], input[6], input[10], input[14],
				input[3], input[7], input[11], input[15]]

	ek = key_gen(s_box)

	state = addRoundKey(state, ek[10])

	for i in range(1,10):
		s = []

		s = shiftRows(state, True)

		s = subBytes(s, True)

		s = addRoundKey(s, ek[-i-1])

		state = mixColumns(s, True)

	s = []

	s = shiftRows(state, True)

	s = subBytes(s, True)

	s = addRoundKey(s, ek[0])

	state = [	s[0], s[4], s[8], s[12],
				s[1], s[5], s[9], s[13],
				s[2], s[6], s[10], s[14],
				s[3], s[7], s[11], s[15]]

	for b in state:
		print("b -->> " + str(10) + " : " + str(hex(int(concatenate_list_data(b),2))[2:]) + ";")

	print("\n\n")

	return state


def main():
	input = [	ar.fill(int_to_bitarray(int("54",16))), ar.fill(int_to_bitarray(int("77",16))), ar.fill(int_to_bitarray(int("6F",16))), ar.fill(int_to_bitarray(int("20",16))),
				ar.fill(int_to_bitarray(int("4F",16))), ar.fill(int_to_bitarray(int("6E",16))), ar.fill(int_to_bitarray(int("65",16))), ar.fill(int_to_bitarray(int("20",16))),
				ar.fill(int_to_bitarray(int("4E",16))), ar.fill(int_to_bitarray(int("69",16))), ar.fill(int_to_bitarray(int("6E",16))), ar.fill(int_to_bitarray(int("65",16))),
				ar.fill(int_to_bitarray(int("20",16))), ar.fill(int_to_bitarray(int("54",16))), ar.fill(int_to_bitarray(int("77",16))), ar.fill(int_to_bitarray(int("6F",16)))]
	
	s_box = sBox_gen(False)

	ciphredText = AES(input, s_box)

	#print(ciphredText)

	#clearText = dAES(ciphredText, s_box)

	#print(ciphredText)


if __name__ == "__main__":
	main()