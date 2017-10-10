from random import randint
from itertools import product
import crypto_utils

# we are creating a superclass Cipher

class Cipher():
    # Legal ASCII characters given by assignment
    legal_chars = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

    def encode(self,message,key):
        return


    def decode(self,encoded_message,key):
        return




    def verify_1key(self,message,key):
        return

    def verify_2keys(self,message,key_e,key_d):
        return

    def generate_keys(self,key=None):
        return

    def possible_keys(self,length):
        return



# Cipher subclasses


class Caesar(Cipher):

    # Overriding the superclass methods
    def encode(self,message,key):
        encoded_message = ""
        for letter in message:
            #if is_legal_char(letter):
            old_index = Cipher.legal_chars.index(letter)
            new_index = (old_index + key) % 95
            encoded_message += Cipher.legal_chars[new_index]
        return encoded_message


    def decode(self,encoded_message,key):
        # using the encode method with altered key to decode
        message = Caesar.encode(self, encoded_message, 95 - key)
        return message

class Multiplicative(Cipher):


    def encode(self,message,key):
        encoded_message = ""
        for letter in message:
            old_index = Cipher.legal_chars.index(letter)
            new_index = (old_index*key) % 95
            encoded_message += Cipher.legal_chars[new_index]
        return encoded_message


    def decode(self,encoded_message,key):
        # we need to generate the inverse key to solve
        new_key = crypto_utils.modular_inverse(key, 95)
        message = self.encode(encoded_message,new_key)
        return message


    # need to generate a valid key. That is a key, x that satisfies x*a = 1 mod(b)
    def generate_valid_key(self):
        key = randint(0, 94)
        return key



class Affine(Cipher):
    # Affine is a combination of Ceasar Cipher and Multiplicative Cipher
    # where we first apply multiplicative cipher and then Caesar for encoding
    # and for decoding the reverse order

    # reuse code
    mult = Multiplicative()
    caes = Caesar()
    # note: Key input in encode and decode contains 2 keys in a list
    def encode(self,message,key):
        encoded_mult = self.mult.encode(message,key[1])
        return self.caes.encode(encoded_mult,key[0])


    def decode(self,encoded_message,key):
        decode_caesar = self.caes.decode(encoded_message,key[0])
        return self.mult.decode(decode_caesar,key[1])

    def generate_keys(self):
        # Multiplicative key
        key1 = self.mult.generate_keys()
        # Caesar key
        key2 = randint(0,94)
        return (key1,key2)



class Unbreakable(Cipher):


    # We want to add the value of a key word in a repeating pattern to encode our word
    def encode(self,message,key):
        key_index = 0
        encoded_message = ""
        for letter in message:
            letter_index = Cipher.legal_chars.index(letter)
            key_letter_index = Cipher.legal_chars.index(key[key_index % len(key)])
            new_index = (letter_index + key_letter_index) % 95
            encoded_message += Cipher.legal_chars[new_index]
            key_index+=1
        return encoded_message

    def decode(self,encoded_message,key):
        # creating a decode key
        decode_key = ""
        for letter in key:
            cipher = Cipher.legal_chars.index(letter)
            decode_key += Cipher.legal_chars[(95 - cipher) % 95]
        return self.encode(encoded_message,decode_key)

    def generate_keys(self,key):
        return key




class RSA(Cipher):


    def encode(self,message,key):
        blocks = crypto_utils.blocks_from_text(message,2)
        new_blocks = []
        for block in blocks:
            new_blocks.append(encode_integer(block,key))
        return new_blocks

    def decode(self,cipher_text_blocks,key):
        new_blocks = []
        for block in cipher_text_blocks:
            new_blocks.append(decode_integer(block,key))
        return crypto_utils.text_from_blocks(new_blocks,2)


    def generate_keys(self):
        p,q = 0,0
        check_keys = -1
        # 5 step method
        while p==q:
            # (1) generate two random primes p & q in range 2^8 to 2^9
            p = crypto_utils.generate_random_prime(8)
            q = crypto_utils.generate_random_prime(8)
        # (2) define n and phi as following
        phi = (p - 1) * (q - 1)
        n = p * q
        # (3) generate a random number between 3 and phi-1
        encode_key = randint(3, phi - 1)

        # (4) we want the inverse mod of e with respect for phi
        try:
            decode_key = crypto_utils.modular_inverse(encode_key, phi)
            return (n, encode_key), (n, decode_key)
        except:
            self.generate_keys()

        # (5) keys successfully generated. (n,encode_key) is used to encrypt the message and is
        #  is for det sender. The reciever can freely publish this key.
        #  (n,d) is for the kept secret and only the reciever knows this key.


# For encrypting messages consisting of integers

# uses previously generated keys
def encode_integer(integer,key):
    n,encode_key = key
    encoded_integer = pow(integer,encode_key,n)
    return encoded_integer

def decode_integer(encoded_integer,key):
    n,decode_key = key
    decoded_integer = pow(encoded_integer,decode_key,n) % n
    return decoded_integer

# creating fictional people acting in the transfer of messages
# Person super class
class Person():

    def __init__(self,key,encrypt_method):
        self.key = key
        self.cipher = encrypt_method

    def set_key(self,key):
        self.key = key

    def get_key(self):
        return self.key



# source subclass used for encoding messages
class Source(Person):
    # initializer
    def __init__(self,key,cipher):
        Person.__init__(self,key,cipher)

    # encrypting the message
    def encrypt_message(self,message):
        encoded_message = self.cipher.encode(message,self.get_key())
        return encoded_message

# receiver is used for decoding messages
class Receiver(Person):

    def __init__(self,key,cipher):
        Person.__init__(self,key,cipher)

    # decrypting the messafe
    def decrypt_message(self,encoded_message):
        decoded_message = self.cipher.decode(encoded_message,self.get_key())
        return decoded_message


# hacker subclass is a bit trickier. In the assignment we were handed out a .txt file containing
# common english words to try to brute force a decoding sequence.

class Hacker(Receiver):

    # importing the dictionary
    def __init__(self,input_dict):
        file = open(input_dict,"r")
        read_data = file.read()
        file.close()
        self.dictionary = read_data.split("\n")


    # scans self.dictionary for word match
    def word_match(self,word):

        return word in self.dictionary


    def decode_bruteforce(self,encoded_message,cipher):
        self.cipher = cipher
        c = 0
        prev_matched = 0
        possible_answer = ""

        if isinstance(cipher, Affine):
            for x in range(0, 95):
                for y in range(0,95):
                    try:
                        crypto_utils.modular_inverse(y,95)
                    except:
                        continue
                    test_key = [x,y]
                    candidat_answer = cipher.decode(encoded_message, test_key)
                    if " " in candidat_answer:
                        candidat_words = candidat_answer.split(" ")
                        words_matched = 0
                        for word in candidat_words:
                            words_matched = 0
                            if word in self.dictionary:
                                words_matched += 1
                        if words_matched > prev_matched:
                            possible_answer = candidat_answer
                            prev_matched = words_matched

            return possible_answer


        # since the brute force for Caesar, Multiplicative and Affine is just iterating through keys from 0 to 95
        # we can use the same method and only need to customize for Unbreakable and RSA.
        if not isinstance(cipher,Unbreakable):
            for x in range(0,95):
                try:
                    crypto_utils.modular_inverse(x,95)
                except:
                    continue
                candidat_answer = cipher.decode(encoded_message,x)

                if " " in candidat_answer and not candidat_answer == "          ":
                    candidat_words = candidat_answer.split(" ")
                    words_matched = 0
                    for word in candidat_words:
                        if word in self.dictionary:
                            words_matched += 1
                    if words_matched > prev_matched:
                        possible_answer = candidat_answer
                        prev_matched = words_matched

            return possible_answer


        # Unbreakable bruteforce. I am choosing the following approach: First we start with the simplest length of the
        # problem, that is only 1 letter in the encrypt word (basicly Caesar). We scan our dictionary for words of that
        # length and try to apply it to the decoding. Then we add the length of the word by 1, scan dictionary again,
        # and so on.
        else:
            satisfied = False
            while satisfied == False:
                for words in self.dictionary:
                    decoded_message = self.cipher.decode(encoded_message,words)
                    decoded_words = decoded_message.split(" ")
                    # if all words are found in list
                    if all(self.word_match(word) for word in decoded_words) and decoded_words != []:
                        possible_answer = decoded_message
                        return possible_answer





def main():
    melding = "hello boss"
    caesar = Caesar()
    multiplicative = Multiplicative()
    affine = Affine()
    unbreakable = Unbreakable()
    rsa = RSA()

    print("Testing Caesar Cipher with key = 3")
    s_cae = Source(3,caesar)
    encoded_message_c = s_cae.encrypt_message(melding)
    print("Message: " + str(melding) + " Encoded: " + str(encoded_message_c))

    r_cae = Receiver(3,caesar)
    decoded_message_c = r_cae.decrypt_message(encoded_message_c)
    print("Encoded: " + str(encoded_message_c) + " Decoded: " + str(decoded_message_c))

    print("Testinh Multiplicative Cipher with key = 4")
    s_mul = Source(4, multiplicative)
    encoded_message_m = s_mul.encrypt_message(melding)
    print("Message: " + str(melding) + " Encoded: " + str(encoded_message_m))

    r_mul = Receiver(4, multiplicative)
    decoded_message_m = r_mul.decrypt_message(encoded_message_m)
    print("Encoded: " + str(encoded_message_m) + " Decoded: " + str(decoded_message_m))

    print("Testing Affine Cipher with keys = 3, 4")
    s_aff = Source((3,4), affine)
    encoded_message_a = s_aff.encrypt_message(melding)
    print("Message: " + str(melding) + " Encoded: " + str(encoded_message_a))

    r_aff = Receiver((3,4), affine)
    decoded_message_a = r_aff.decrypt_message(encoded_message_a)
    print("Encoded: " + str(encoded_message_a) + " Decoded: " + str(decoded_message_a))

    print("Testing Unbreakable Chipher with key = abaci")
    s_unb = Source("abase",unbreakable)
    encoded_message_u = s_unb.encrypt_message(melding)
    print("Message: " + str(melding) + " Encoded: " + str(encoded_message_u))

    r_unb = Receiver("abase", unbreakable)
    decoded_message_u = r_unb.decrypt_message(encoded_message_u)
    print("Encoded: " + str(encoded_message_u) + " Decoded: " + str(decoded_message_u))

    print("Testing RSA Chipher with generated keys")
    print("we will have to generate keys")
    (n, encode_key), (n, decode_key) = rsa.generate_keys()
    #valid = crypto_utils.modular_inverse(decode_key,encode_key)
    #print(valid)
    print("encode key: " + str(encode_key) + " decode key: " +str(decode_key))
    s_rsa = Source((n,encode_key),rsa)
    encoded_message = s_rsa.encrypt_message(melding)
    print("Message: " + str(melding) + " Encoded: " + str(encoded_message))

    r_rsa = Receiver((n,decode_key),rsa)
    decoded_message = r_rsa.decrypt_message(encoded_message)
    print("Encoded: " + str(encoded_message) + " Decoded: " + str(decoded_message))

    print("Hacker: ")
    hacker = Hacker("english-text.txt")
    print("CaesarHack: " + str(hacker.decode_bruteforce(encoded_message_c, caesar)))
    print("MultiHack: " + str(hacker.decode_bruteforce(encoded_message_m, multiplicative)))
    print("AffineHack: " + str(hacker.decode_bruteforce(encoded_message_a, affine)))
    print("UnbreakableHack: " + str(hacker.decode_bruteforce(encoded_message_u, unbreakable)))
main()






