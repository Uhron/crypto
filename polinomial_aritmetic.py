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
		""" fill with 0 polinomyal with len less than eight
		returns p filled with len equal than irreductible polynomial
		"""

		if fill == None:
				fill = len(self.p_irreductible) - 1

		while(len(p) < fill):
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

			return Pi[0], Qi[0], a_p

		else:
			return 0, 0, a_p


def main():
	""" Main function, call aritmetic class
	no returns
	"""
	print("modular aritmetic:\n")

	ar = Aritmetic()

	print("irreductible polynomial:" + str(ar.p_irreductible) + "\n")
	print("substitution polynomial:" + str(ar.substitution) + "\n")
	"""	
	tmp = [0, 0, 1, 1, 1, 1, 0, 0]
	print("reduct: " + str(tmp) + ";\n\n\t\t result: " + str(ar.reduct(tmp)) + ";\n")
	tmp = [0, 1, 1, 0, 1, 1, 1, 0]
	print("reduct: " + str(tmp) + ";\n\n\t\t result: " + str(ar.reduct(tmp)) + ";\n")
	tmp = [0, 1, 0, 0, 0, 1, 1, 1]
	print("reduct: " + str(tmp) + ";\n\n\t\t result: " + str(ar.reduct(tmp)) + ";\n")
	a = [1, 0, 0, 0, 0, 0, 0, 0]
	b = [0]
	print("fill: " + str(ar.reduct(b)))
	print("mult: \t A: " + str(a) + ";\t B: " + str(b) + ";\n\n\t\t result: " + str(ar.reduct(ar.mult(a,b))) + ";\n")
	a = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]
	print("div: \t A: " + str(a) + ";\n\n\t\t result: " + str(ar.div(a)) + ";\n")
	"""
	b = [0, 0, 1, 1, 1, 1, 1, 0]
	a = ar.p_irreductible

	pi, qi, gdc = ar.gcd(a, b)

	print("gcd: \t A: " + str(a) + ";\t B: " + str(b) + ";\n\n\t\t result: " + str((pi, qi, gdc)) + ";\n")
	print("inverse of: " + str(b) + " is -->> " + str(qi) + ";\n")
	
	a = ar.p_irreductible
	b = [0, 1, 1, 0, 1, 1, 1, 0]

	pi, qi, gdc = ar.gcd(a, b)

	print("gcd: \t A: " + str(a) + ";\t B: " + str(b) + ";\n\n\t\t result: " + str((pi, qi, gdc)) + ";\n")
	print("inverse of: " + str(b) + " is -->> " + str(qi) + ";\n")

	a = ar.p_irreductible
	b = [0, 1, 0, 0, 0, 1, 1, 1]

	pi, qi, gdc = ar.gcd(a, b)

	print("gcd: \t A: " + str(a) + ";\t B: " + str(b) + ";\n\n\t\t result: " + str((pi, qi, gdc)) + ";\n")
	print("inverse of: " + str(b) + " is -->> " + str(qi) + ";\n")

	a = ar.p_irreductible
	b = [0, 0, 0, 0, 0, 0, 1, 0, 0]

	pi, qi, gdc = ar.gcd(a, b)

	print("gcd: \t A: " + str(a) + ";\t B: " + str(b) + ";\n\n\t\t result: " + str((pi, qi, gdc)) + ";\n")
	print("inverse of: " + str(b) + " is -->> " + str(qi) + ";\n")

	a = [1, 0, 0, 0, 1, 1, 0, 1, 1]
	b = [0, 0, 0, 0, 0, 0, 1, 0, 1]

	pi, qi, gdc = ar.gcd(a, b)

	print("gcd: \t A: " + str(a) + ";\t B: " + str(b) + ";\n\n\t\t result: " + str((pi, qi, gdc)) + ";\n")
	print("inverse of: " + str(b) + " is -->> " + str(qi) + ";\n")



if __name__ == "__main__":
	main()