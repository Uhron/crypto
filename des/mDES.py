import codecs

"""
 author: Álex Vázquez

 summary: Data Encryption Standard Implementation
"""

####        KEY VALUES      ####

KEY  =  "1010101010101010101010101010101010101010101010101010101010101010"

PC_1 =[ KEY[56],KEY[48],KEY[40],KEY[32],KEY[24],KEY[16],KEY[8],
		KEY[0],KEY[57],KEY[49],KEY[41],KEY[33],KEY[25],KEY[17],
		KEY[9],KEY[1],KEY[58],KEY[50],KEY[42],KEY[34],KEY[26],
		KEY[18],KEY[10],KEY[2],KEY[59],KEY[51],KEY[43],KEY[35],
		KEY[62],KEY[54],KEY[46],KEY[38],KEY[30],KEY[22],KEY[14],
		KEY[6],KEY[61],KEY[53],KEY[45],KEY[37],KEY[29],KEY[21],
		KEY[13],KEY[5],KEY[60],KEY[52],KEY[44],KEY[36],KEY[28],
		KEY[20],KEY[12],KEY[4],KEY[27],KEY[19],KEY[11],KEY[3]] #key permuted

C0 = PC_1[:len(PC_1)//2] #first half

D0 = PC_1[len(PC_1)//2:] #second half

SUB_KEYS = []

####        KEY VALUES      ####

####        S-BOXES         ####

S = [
		#S1
		[
			['1110','0100', '1101','0001','0010', '1111', '1011','1000','0011', '1010','0110', '1100','0101','1001','0000','0111'],
			['0000', '1111','0111','0100', '1110','0010', '1101','0001', '1010','0110', '1100', '1011','1001','0101','0011','1000'],
			['0100','0001', '1110','1000', '1101','0110','0010', '1011', '1111', '1100','1001','0111','0011', '1010','0101','0000'],
			['1111', '1100','1000','0010','0100','1001','0001','0111','0101', '1011','0011', '1110', '1010','0000','0110', '1101']
		],

		#S2
		[
			['1111','0001','1000', '1110','0110', '1011','0011','0100','1001','0111','0010', '1101', '1100','0000','0101','1010'],
			['0011', '1101','0100','0111', '1111','0010','1000', '1110', '1100','0000','0001','1010','0110','1001', '1011','0101'],
			['0000', '1110','0111', '1011','1010','0100', '1101','0001','0101','1000', '1100','0110','1001','0011','0010', '1111'],
			['1101','1000','1010','0001','0011', '1111','0100','0010', '1011','0110','0111', '1100','0000','0101', '1110','1001'],
		],

		#S3
		[
			['1010','0000','1001', '1110','0110','0011', '1111','0101','0001', '1101', '1100','0111', '1011','0100','0010','1000'],
			['1101','0111','0000','1001','0011','0100','0110','1010','0010','1000','0101', '1110', '1100', '1011', '1111','0001'],
			['1101','0110','0100','1001','1000', '1111','0011','0000', '1011','0001','0010', '1100','0101','1010', '1110','0111'],
			['0001','1010', '1101','0000','0110','1001','1000','0111','0100', '1111', '1110','0011', '1011','0101','0010', '1100'],
		],

		#S4
		[
			['0111', '1101', '1110','0011','0000','0110','1001','1010','0001','0010','1000','0101', '1011', '1100','0100', '1111'],
			['1101','1000', '1011','0101','0110', '1111','0000','0011','0100','0111','0010', '1100','0001','1010', '1110','1001'],
			['1010','0110','1001','0000', '1100', '1011','0111', '1101', '1111','0001','0011', '1110','0101','0010','1000','0100'],
			['0011', '1111','0000','0110','1010','0001', '1101','1000','1001','0100','0101', '1011', '1100','0111','0010', '1110'],
		],

		#S5
		[
			['0010', '1100','0100','0001','0111','1010', '1011','0110','1000','0101','0011', '1111', '1101','0000', '1110','1001'],
			['1110', '1011','0010', '1100','0100','0111', '1101','0001','0101','0000', '1111','1010','0011','1001','1000','0110'],
			['0100','0010','0001', '1011','1010', '1101','0111','1000', '1111','1001', '1100','0101','0110','0011','0000', '1110'],
			['1011','1000', '1100','0111','0001', '1110','0010', '1101','0110', '1111','0000','1001','1010','0100','0101','0011'],
		],

		#S6
		[
			['1100','0001','1010', '1111','1001','0010','0110','1000','0000', '1101','0011','0100', '1110','0111','0101', '1011'],
			['1010', '1111','0100','0010','0111', '1100','1001','0101','0110','0001', '1101', '1110','0000', '1011','0011','1000'],
			['1001', '1110', '1111','0101','0010','1000', '1100','0011','0111','0000','0100','1010','0001', '1101', '1011','0110'],
			['0100','0011','0010', '1100','1001','0101', '1111','1010', '1011', '1110','0001','0111','0110','0000','1000', '1101'],
		],

		#S7
		[
			['0100', '1011','0010', '1110', '1111','0000','1000', '1101','0011', '1100','1001','0111','0101','1010','0110','0001'],
			['1101','0000', '1011','0111','0100','1001','0001','1010', '1110','0011','0101', '1100','0010', '1111','1000','0110'],
			['0001','0100', '1011', '1101', '1100','0011','0111', '1110','1010', '1111','0110','1000','0000','0101','1001','0010'],
			['0110', '1011', '1101','1000','0001','0100','1010','0111','1001','0101','0000', '1111', '1110','0010','0011', '1100'],
		],

		#S8
		[
			['1101','0010','1000','0100','0110', '1111', '1011','0001','1010','1001','0011', '1110','0101','0000', '1100','0111'],
			['0001', '1111', '1101','1000','1010','0011','0111','0100', '1100','0101','0110', '1011','0000', '1110','1001','0010'],
			['0111', '1011','0100','0001','1001', '1100', '1110','0010','0000','0110','1010', '1101', '1111','0011','0101','1000'],
			['0010','0001', '1110','0111','0100','1010','1000', '1101', '1111', '1100','1001','0000','0011','0101','0110', '1011'],
		]
	]

####        S-BOXES         ####

#### 		MASKARA			####

X = '1011101110111011101110111011101110111011101110111011101110111011'
#X = '0000000000000000000000000000000011110000000000000000000000000000'

#### 		MASKARA			####

def fill(data):
	""" add parity bit to data

	Returns data with parity bit
	"""
	count = 0

	for i in range(len(data)):

		if count >= 8:
			count = 0
			data.insert(i,0)
		else: 
			count += 1

	return data


def concatenate_list_data(list):
	""" concatenate list data, concatenate all data in a list into one string

	Returns string of concatenated data
	"""
	result = ''

	for element in list:

		result += str(element)

	return result


def tobits(s):
	""" transform input string to output bit's array

	Returns arrays of bits
	"""

	result = []

	for c in s:

		bits = bin(ord(c))[2:]
		bits = '00000000'[len(bits):] + bits
		result.extend([int(b) for b in bits])

	return result


def frombits(bits):
	""" transform input bit's array to output string

	Returns string
	"""

	chars = []

	for b in range(len(bits) // 8):

		byte = bits[b*8:(b+1)*8]
		chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

	return ''.join(chars)

def int_to_bit(n):
	""" transform input integer to output bit array

	Returns array
	"""
	return [int(digit) for digit in bin(n)[2:]]


def key_cal(kL, kR, round):
	""" makes key calculations

	Returns round key computated
	"""
	p = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] #cyclic shifts

	kL = kL[p[round]:] + kL[:p[round]]# shift
	kR = kR[p[round]:] + kR[:p[round]]# shift

	k = kL + kR

	PC_2 =[ k[13],k[16],k[10],k[23],k[0],k[4],
			k[2],k[27],k[14],k[5],k[20],k[9],
			k[22],k[18],k[11],k[3],k[25],k[7],
			k[15],k[6],k[26],k[19],k[12],k[1],
			k[40],k[51],k[30],k[36],k[46],k[54],
			k[29],k[39],k[50],k[44],k[32],k[47],
			k[43],k[48],k[38],k[55],k[33],k[52],
			k[45],k[41],k[49],k[35],k[28],k[31]]# key permuted

	#print("key round " + str(round) + " : " + ''.join(PC_2) + "; length: " + str(len(PC_2)) + "\n")

	SUB_KEYS.append(PC_2);

	return PC_2, kL, kR


def sm_box_gen(inv, X2):
	""" generate sm-boxes

	Returns list with sm-box computed on input
	"""

	sm_box = []

	for i in range(64):
		sm_box.append([])

	inv_4 = []

	for i in range(0,len(inv),4):
		inv_4.append((inv[i],inv[i+1],inv[i+2],inv[i+3]))

	for i in range(64):

		b = bin(i)[2:].zfill(6)*8

		xored = []

		for j in range(len(b)):
			xored.append(int(b[j])^int(X2[j]))

		Bi = []

		for n in range(8):
			Bi = [xored[n*6],xored[(n*6)+1],xored[(n*6)+2],xored[(n*6)+3],xored[(n*6)+4],xored[(n*6)+5]]
			res = S[n][int((str(Bi[0]) + str(Bi[-1])), 2)][int((str(Bi[1]) + str(Bi[2]) + str(Bi[3]) + str(Bi[4])), 2)]
			tmp = []
			for x in range(len(inv_4[n])):
				tmp.append(int(inv_4[n][x])^int(res[x]))

			sm_box[i].append(concatenate_list_data(tmp))

	return sm_box


def compute_input(input, X1, key, sm_box):
	""" feistel function: expansion permutation , split input, xor half input 
	with key and make S-Box Substitutions

	Returns list computed
	"""
	Li = input[:len(input)//2] #first half
	Ri = input[len(input)//2:] #second half

	X1L = X1[:len(X1)//2] #first half
	X1R = X1[len(X1)//2:] #second half

	Re =[   Ri[31],Ri[0],Ri[1],Ri[2],Ri[3],Ri[4]
			,Ri[3],Ri[4],Ri[5],Ri[6],Ri[7],Ri[8]
			,Ri[7],Ri[8],Ri[9],Ri[10],Ri[11],Ri[12]
			,Ri[11],Ri[12],Ri[13],Ri[14],Ri[15],Ri[16]
			,Ri[15],Ri[16],Ri[17],Ri[18],Ri[19],Ri[20]
			,Ri[19],Ri[20],Ri[21],Ri[22],Ri[23],Ri[24]
			,Ri[23],Ri[24],Ri[25],Ri[26],Ri[27],Ri[28]
			,Ri[27],Ri[28],Ri[29],Ri[30],Ri[31],Ri[0]]

	X2 =[   X1R[31],X1R[0],X1R[1],X1R[2],X1R[3],X1R[4]
			,X1R[3],X1R[4],X1R[5],X1R[6],X1R[7],X1R[8]
			,X1R[7],X1R[8],X1R[9],X1R[10],X1R[11],X1R[12]
			,X1R[11],X1R[12],X1R[13],X1R[14],X1R[15],X1R[16]
			,X1R[15],X1R[16],X1R[17],X1R[18],X1R[19],X1R[20]
			,X1R[19],X1R[20],X1R[21],X1R[22],X1R[23],X1R[24]
			,X1R[23],X1R[24],X1R[25],X1R[26],X1R[27],X1R[28]
			,X1R[27],X1R[28],X1R[29],X1R[30],X1R[31],X1R[0]]

	xored = []
	for i in range(len(Re)):
		xored.append(int(Re[i])^int(key[i]))

	s_box_res = []

	for i in range(0,48,6):	
		pos = [xored[i],xored[i+1],xored[i+2],xored[i+3],xored[i+4],xored[i+5]]
		pos = int(concatenate_list_data(pos),2)
		res = sm_box[pos][i//6]
		for b in res:
			s_box_res.append(b)

	print(concatenate_list_data(s_box_res))

	p_box_res =[    s_box_res[15],s_box_res[6],s_box_res[19],s_box_res[20],s_box_res[28],s_box_res[11],s_box_res[27],s_box_res[16]
					,s_box_res[0],s_box_res[14],s_box_res[22],s_box_res[25],s_box_res[4],s_box_res[17],s_box_res[30],s_box_res[9]
					,s_box_res[1],s_box_res[7],s_box_res[23],s_box_res[13],s_box_res[31],s_box_res[26],s_box_res[2],s_box_res[8]
					,s_box_res[18],s_box_res[12],s_box_res[29],s_box_res[5],s_box_res[21],s_box_res[10],s_box_res[3],s_box_res[24]]

	X1x = []
	for i in range(len(X1L)):
		X1x.append(int(X1L[i])^int(X1R[i]))

	res = []
	for i in range(len(Ri)):
		res.append(int(Ri[i])^int(X1x[i]))

	xored = []
	for i in range(len(Li)):
		xored.append(int(Li[i])^int(p_box_res[i]))

	return res,xored



def DES(input, ciphre):
	""" DES function, DES implementation

	Returns output of DES
	"""

	k_left, k_rigth = C0, D0

	M = input

	MX = []
	for i in range(len(M)):
		MX.append(int(X[i])^int(M[i]))

	print("M     : " + M + "; length: " + str(len(M)) + "\n")
	print("MX    : " + concatenate_list_data(MX) + "; length: " + str(len(MX)) + "\n")

	IPMX =[	MX[57],MX[49],MX[41],MX[33],MX[25],MX[17],MX[9],MX[1],
			MX[59],MX[51],MX[43],MX[35],MX[27],MX[19],MX[11],MX[3],
			MX[61],MX[53],MX[45],MX[37],MX[29],MX[21],MX[13],MX[5],
			MX[63],MX[55],MX[47],MX[39],MX[31],MX[23],MX[15],MX[7],
			MX[56],MX[48],MX[40],MX[32],MX[24],MX[16],MX[8],MX[0],
			MX[58],MX[50],MX[42],MX[34],MX[26],MX[18],MX[10],MX[2],
			MX[60],MX[52],MX[44],MX[36],MX[28],MX[20],MX[12],MX[4],
			MX[62],MX[54],MX[46],MX[38],MX[30],MX[22],MX[14],MX[6],]
	

	X1 = [  X[57],X[49],X[41],X[33],X[25],X[17],X[9],X[1],
			X[59],X[51],X[43],X[35],X[27],X[19],X[11],X[3],
			X[61],X[53],X[45],X[37],X[29],X[21],X[13],X[5],
			X[63],X[55],X[47],X[39],X[31],X[23],X[15],X[7],
			X[56],X[48],X[40],X[32],X[24],X[16],X[8],X[0],
			X[58],X[50],X[42],X[34],X[26],X[18],X[10],X[2],
			X[60],X[52],X[44],X[36],X[28],X[20],X[12],X[4],
			X[62],X[54],X[46],X[38],X[30],X[22],X[14],X[6],]

	print("IPMX  : " + concatenate_list_data(IPMX) + "; length: " + str(len(IPMX)) + "\n")
	print("X1    : " + concatenate_list_data(X1) + "; length: " + str(len(X1)) + "\n")

	X1L = X1[:len(X1)//2] #first half
	X1R = X1[len(X1)//2:] #second half

	X1x = []
	for i in range(len(X1L)):
		X1x.append(int(X1L[i])^int(X1R[i]))

	inv_box_res =[   X1x[8],X1x[16],X1x[22],X1x[30],X1x[12],X1x[27],X1x[1],X1x[17]
					,X1x[23],X1x[15],X1x[29],X1x[5],X1x[25],X1x[19],X1x[9],X1x[0]
					,X1x[7],X1x[13],X1x[24],X1x[2],X1x[3],X1x[28],X1x[10],X1x[18]
					,X1x[31],X1x[11],X1x[21],X1x[6],X1x[4],X1x[26],X1x[14],X1x[20]]

	X2 =[   X1R[31],X1R[0],X1R[1],X1R[2],X1R[3],X1R[4]
			,X1R[3],X1R[4],X1R[5],X1R[6],X1R[7],X1R[8]
			,X1R[7],X1R[8],X1R[9],X1R[10],X1R[11],X1R[12]
			,X1R[11],X1R[12],X1R[13],X1R[14],X1R[15],X1R[16]
			,X1R[15],X1R[16],X1R[17],X1R[18],X1R[19],X1R[20]
			,X1R[19],X1R[20],X1R[21],X1R[22],X1R[23],X1R[24]
			,X1R[23],X1R[24],X1R[25],X1R[26],X1R[27],X1R[28]
			,X1R[27],X1R[28],X1R[29],X1R[30],X1R[31],X1R[0]]

	sm_boxes = sm_box_gen(inv_box_res, X2)

	i = IPMX

	if(ciphre):

		for round in range(15):

			round_key, k_left, k_rigth = key_cal(k_left, k_rigth, round)

			Li, Ri = compute_input(i, X1, round_key, sm_boxes)

			i = Li + Ri

		round_key, k_left, k_rigth = key_cal(k_left, k_rigth, 15)

		Li, Ri = compute_input(i, X1, round_key, sm_boxes)		

		Rix = []
		for i in range(len(Ri)):
			Rix.append(int(Ri[i])^int(X1x[i]))

		Lix = []
		for i in range(len(Li)):
			Lix.append(int(Li[i])^int(X1x[i]))

		i = Rix + Lix

	else:

		for round in range(1,16):

			Li, Ri = compute_input(i, X1, SUB_KEYS[-round], sm_boxes)

			i = Li + Ri


		Li, Ri = compute_input(i, X1, SUB_KEYS[0], sm_boxes)		

		Rix = []
		for i in range(len(Ri)):
			Rix.append(int(Ri[i])^int(X1x[i]))

		Lix = []
		for i in range(len(Li)):
			Lix.append(int(Li[i])^int(X1x[i]))

		i = Rix + Lix

	FP =[	i[39],i[7],i[47],i[15],i[55],i[23],i[63],i[31]
			,i[38],i[6],i[46],i[14],i[54],i[22],i[62],i[30]
			,i[37],i[5],i[45],i[13],i[53],i[21],i[61],i[29]
			,i[36],i[4],i[44],i[12],i[52],i[20],i[60],i[28]
			,i[35],i[3],i[43],i[11],i[51],i[19],i[59],i[27]
			,i[34],i[2],i[42],i[10],i[50],i[18],i[58],i[26]
			,i[33],i[1],i[41],i[9],i[49],i[17],i[57],i[25]
			,i[32],i[0],i[40],i[8],i[48],i[16],i[56],i[24]]


	MX_p = []

	for i in range(len(FP)):
		MX_p.append(int(X[i])^int(FP[i]))

	h = hex(int(concatenate_list_data(MX_p),2))		

	return concatenate_list_data(MX_p), h


def main():
	""" Main function, call DES implementation

	no returns
	"""
	input = b'12345678'
	hexlify = codecs.getencoder('hex')
	x = hexlify(input)[0]

	print("\ninput : " + str(input) + "; hex : " + str(x) + "\n")
	print("key   : " + str(KEY) + "\n")
	print("PC1   : " + ''.join(PC_1) + "; length: " + str(len(PC_1)) + "\n")

	i = bin(int(x, 16))[2:]
	i = '00' + concatenate_list_data(i)

	output1, h = DES(i, True)
	print("\n\noutput 1 : " + str(output1) + "; hex : " + h + "\n")

	output2, h = DES(output1, False)
	print("\n\noutput 2 : " + str(output2) + "; hex : " + h + "\n")


if __name__ == "__main__":
	main()
