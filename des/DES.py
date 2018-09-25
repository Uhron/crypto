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


def concatenate_list_data(list):    #TODO
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


def compute_input(input, key):
	""" feistel function: expansion permutation , split input, xor half input 
	with key and make S-Box Substitutions

	Returns list computed
	"""
	Li = input[:len(input)//2] #first half
	Ri = input[len(input)//2:] #second half

	Re =[   Ri[31],Ri[0],Ri[1],Ri[2],Ri[3],Ri[4]
			,Ri[3],Ri[4],Ri[5],Ri[6],Ri[7],Ri[8]
			,Ri[7],Ri[8],Ri[9],Ri[10],Ri[11],Ri[12]
			,Ri[11],Ri[12],Ri[13],Ri[14],Ri[15],Ri[16]
			,Ri[15],Ri[16],Ri[17],Ri[18],Ri[19],Ri[20]
			,Ri[19],Ri[20],Ri[21],Ri[22],Ri[23],Ri[24]
			,Ri[23],Ri[24],Ri[25],Ri[26],Ri[27],Ri[28]
			,Ri[27],Ri[28],Ri[29],Ri[30],Ri[31],Ri[0]]

	xored = []
	for i in range(len(Re)):
		xored.append(int(Re[i])^int(key[i]))

	s_box_res = []

	i = 0
	while i < 48:
		Bi = xored[i:i+6]

		res = S[i//6][int((str(Bi[0]) + str(Bi[-1])), 2)][int((str(Bi[1]) + str(Bi[2]) + str(Bi[3]) + str(Bi[4])), 2)]

		for b in res:
			s_box_res.append(b)

		i += 6

	print(concatenate_list_data(s_box_res))

	p_box_res =[    s_box_res[15],s_box_res[6],s_box_res[19],s_box_res[20],s_box_res[28],s_box_res[11],s_box_res[27],s_box_res[16]
					,s_box_res[0],s_box_res[14],s_box_res[22],s_box_res[25],s_box_res[4],s_box_res[17],s_box_res[30],s_box_res[9]
					,s_box_res[1],s_box_res[7],s_box_res[23],s_box_res[13],s_box_res[31],s_box_res[26],s_box_res[2],s_box_res[8]
					,s_box_res[18],s_box_res[12],s_box_res[29],s_box_res[5],s_box_res[21],s_box_res[10],s_box_res[3],s_box_res[24]]

	xored = []

	for i in range(len(Li)):
		xored.append(int(Li[i])^int(p_box_res[i]))

	return Ri,xored



def DES(input, ciphre):
	""" DES function, DES implementation

	Returns output of DES
	"""

	k_left, k_rigth = C0, D0

	i = input

	print("i     : " + input + "; length: " + str(len(input)) + "\n")

	IP = [  i[57],i[49],i[41],i[33],i[25],i[17],i[9],i[1],
			i[59],i[51],i[43],i[35],i[27],i[19],i[11],i[3],
			i[61],i[53],i[45],i[37],i[29],i[21],i[13],i[5],
			i[63],i[55],i[47],i[39],i[31],i[23],i[15],i[7],
			i[56],i[48],i[40],i[32],i[24],i[16],i[8],i[0],
			i[58],i[50],i[42],i[34],i[26],i[18],i[10],i[2],
			i[60],i[52],i[44],i[36],i[28],i[20],i[12],i[4],
			i[62],i[54],i[46],i[38],i[30],i[22],i[14],i[6],]

	print("IP    : " + concatenate_list_data(IP) + "; length: " + str(len(IP)) + "\n")

	i = IP

	if(ciphre):

		for round in range(15):

			round_key, k_left, k_rigth = key_cal(k_left, k_rigth, round)

			Li,Ri = compute_input(i,round_key)

			i = Li + Ri

		round_key, k_left, k_rigth = key_cal(k_left, k_rigth, 15)

		Li,Ri = compute_input(i,round_key)

		i = Ri + Li

	else:

		for round in range(1,16):

			Li,Ri = compute_input(i, SUB_KEYS[-round])

			i = Li + Ri


		Li,Ri = compute_input(i, SUB_KEYS[0])

		i = Ri + Li

	FP =[	i[39],i[7],i[47],i[15],i[55],i[23],i[63],i[31]
			,i[38],i[6],i[46],i[14],i[54],i[22],i[62],i[30]
			,i[37],i[5],i[45],i[13],i[53],i[21],i[61],i[29]
			,i[36],i[4],i[44],i[12],i[52],i[20],i[60],i[28]
			,i[35],i[3],i[43],i[11],i[51],i[19],i[59],i[27]
			,i[34],i[2],i[42],i[10],i[50],i[18],i[58],i[26]
			,i[33],i[1],i[41],i[9],i[49],i[17],i[57],i[25]
			,i[32],i[0],i[40],i[8],i[48],i[16],i[56],i[24]]

	h = hex(int(concatenate_list_data(FP),2))		

	return concatenate_list_data(FP), h


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