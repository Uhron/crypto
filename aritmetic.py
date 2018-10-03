
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


def main():
	""" Main function, call aritmetic class
	no returns
	"""
	print("modular aritmetic:\n")

	ar = Aritmetic()

	print(ar.gcd((11 - 1)*(23 - 1),3))



if __name__ == "__main__":
	main()