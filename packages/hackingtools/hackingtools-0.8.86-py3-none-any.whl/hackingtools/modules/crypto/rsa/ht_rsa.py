from hackingtools.core import Logger
import random

class StartModule():

	def __init__(self):
		Logger.printMessage(message='ht_rsa loaded', debug_module=True)
		pass

	'''
	Euclid's algorithm for determining the greatest common divisor
	Use iteration to make it faster for larger integers
	'''
	def __gcd__(self, a, b):
		while b != 0:
			a, b = b, a % b
		return a

	'''
	Euclid's extended algorithm for finding the multiplicative inverse of two numbers
	'''
	def __multiplicative_inverse__(self, e, phi):
		d = 0
		x1 = 0
		x2 = 1
		y1 = 1
		temp_phi = phi
		
		while e > 0:
			temp1 = temp_phi/e
			temp2 = temp_phi - temp1 * e
			temp_phi = e
			e = temp2
			
			x = x2- temp1* x1
			y = d - temp1 * y1
			
			x2 = x1
			x1 = x
			d = y1
			y1 = y
		
		if temp_phi == 1:
			return d + phi

	'''
	Tests to see if a number is prime.
	'''
	def __is_prime__(self, num):
		if int(num) == 2:
			return True
		if int(num) < 2 or int(num) % 2 == 0:
			return False
		for n in range(3, int(num**0.5)+2, 2):
			if num % n == 0:
				return False
		return True

	def generate_keypair(self, prime_a, prime_b):
		if not (self.__is_prime__(prime_a) and self.__is_prime__(prime_b)):
			raise ValueError('Both numbers must be prime.')
		elif prime_a == prime_b:
			raise ValueError('p and q cannot be equal')
		#n = pq
		n = prime_a * prime_b

		#Phi is the totient of n
		phi = (prime_a-1) * (prime_b-1)

		#Choose an integer e such that e and phi(n) are coprime
		e = random.randrange(1, phi)

		#Use Euclid's Algorithm to verify that e and phi(n) are comprime
		g = self.__gcd__(e, phi)
		while g != 1:
			e = random.randrange(1, phi)
			g = self.__gcd__(e, phi)

		#Use Extended Euclid's Algorithm to generate the private key
		print(e)
		print(phi)
		d = self.__multiplicative_inverse__(e, phi)
		
		#Return public and private keypair
		#Public key is (e, n) and private key is (d, n)
		return ((e, n), (d, n))

	def encrypt(self, private_key, plaintext):
		#Unpack the key into it's components
		key, n = private_key
		#Convert each letter in the plaintext to numbers based on the character using a^b mod m
		cipher = [(ord(char) ** key) % n for char in plaintext]
		#Return the array of bytes
		return cipher

	def decrypt(self, public_key, ciphertext):
		#Unpack the key into its components
		key, n = public_key
		#Generate the plaintext based on the ciphertext and key using a^b mod m
		plain = [chr((char ** key) % n) for char in ciphertext]
		#Return the array of bytes as a string
		return ''.join(plain)
		
	def getRandomKeypair(self):
		prime_a = ''
		prime_b = ''
		while prime_a == '':
			num = random.randint(random.randint(0,15),random.randint(15,30))*random.randint(1,10)
			if self.__is_prime__(num):
				prime_a = num
		print('A: {a}'.format(a=prime_a))
		while prime_b == '':
			num = random.randint(random.randint(30,45),random.randint(45,60))*random.randint(1,10)
			if self.__is_prime__(num):
				prime_b = num
		print('B: {b}'.format(b=prime_b))
		return self.generate_keypair(prime_a, prime_b)

#message= 'Hola que tal'

#prime_a, prime_b = getRandomKeypair()
#public, private = generate_keypair(prime_a, prime_b)

#encrypted_msg = encrypt(private, message)
#encrypted_msg_joined = ''.join(map(lambda x: str(x), encrypted_msg))

#decrypted_msg = decrypt(public, encrypted_msg)