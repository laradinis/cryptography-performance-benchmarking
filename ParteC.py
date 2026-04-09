from cryptography.hazmat.primitives.asymmetric import rsa
import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import timeit
import statistics

# Implementa: Enc(m;r) = (RSA(r), H(0,r)⊕m0​, …, H(n,r)⊕mn​)
class RSA:
    # Criar a chave RSA

    # Executada quando se cria o objeto
    def __init__(self):
        '''
        chave privada (n,e,d,p,q)
        internamente é escolhido um p e um q e calculado o n = p * q
        também é calculado o d
        '''
        self.private_key = rsa.generate_private_key(
            public_exponent= 0x10001, # e
            key_size=2048 # aprox n
        )
        # Chave pública (n,e)
        self.public_key = self.private_key.public_key()

        # Dividir as mensagem em blocos de 32 bytes
        self.block_size = 32


    # Criar função hash com i = índice do bloco
    def H(self, i, r):

        i_bytes = i.to_bytes(4,'big') # Transforma o índice em bytes
        return hashlib.sha256(i_bytes + r).digest() # Calcula o hash


    #____Função de Encriptação____
    def encrypt(self, mensagem):
        # Gerar r: número aleatorio de tamanho 32 bytes
        r = os.urandom(32)

        # Converter r para inteiro
        r_int = int.from_bytes(r, 'big')

        e = self.public_key.public_numbers().e
        n = self.public_key.public_numbers().n
        
        # Cifrar r manualmente: c = r^e mod n
        encrypted_r_int = pow(r_int, e, n)
        
        # Converter de volta para bytes
        key_size_bytes = (n.bit_length() + 7) // 8
        encrypted_r = encrypted_r_int.to_bytes(key_size_bytes, 'big')
        
        # Encriptar mensagem com XOR usando H(i, r)
        blocks = []
        for i in range(0, len(mensagem), 32):
            block = mensagem[i:i+32]
            key = self.H(i//32, r)
            cipher = bytes([a ^ b for a, b in zip(block, key)])
            blocks.append(cipher)
        
        return encrypted_r, blocks


    #____Função de Desencriptação____
    def decrypt(self, encrypted_r, blocks):
        # Converter encrypted_r para inteiro
        c_int = int.from_bytes(encrypted_r, 'big')
        
        d = self.private_key.private_numbers().d
        n = self.private_key.private_numbers().public_numbers.n
        
        # Decifrar r manualmente: r = c^d mod n
        r_int = pow(c_int, d, n)
        
        # Converter de volta para bytes
        r_bytes = r_int.to_bytes((r_int.bit_length() + 7) // 8, 'big')
        
        # Se r_bytes for menor que 32 bytes, preencher à esquerda com zeros
        if len(r_bytes) < 32:
            r = b'\x00' * (32 - len(r_bytes)) + r_bytes
        else:
            r = r_bytes[:32] # Pegar apenas os primeiros 32 bytes
        
        # Desencriptar mensagem com XOR
        mensagem = b''
        for i, block in enumerate(blocks):
            key = self.H(i, r)
            m = bytes([a ^ b for a, b in zip(block, key)])
            mensagem += m
        
        return mensagem

#___Tempo de execução___
rsa_enc_means = []
rsa_dec_means = []



file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]


def run_rsa():
    global rsa_enc_means, rsa_dec_means
    global encrypt_times_all, decrypt_times_all

    rsa_enc_means = []
    rsa_dec_means = []

    cipher = RSA()

    for size in file_sizes:
        print(f"\n_____________________________")
        print(f"Tamanho: {size} bytes")
        print(f"_____________________________")

        with open(f"file_{size}.txt", "rb") as f:
            data = f.read()

        encrypt_times = []
        decrypt_times = []

        # preparar decrypt (fixo)
        encrypted_r, blocks = cipher.encrypt(data)

        for _ in range(30):
            # ENCRYPT
            t_enc = timeit.timeit(lambda: cipher.encrypt(data), number=1)
            encrypt_times.append(t_enc)

            # DECRYPT
            t_dec = timeit.timeit(lambda: cipher.decrypt(encrypted_r, blocks), number=1)
            decrypt_times.append(t_dec)


        # médias
        media_enc = statistics.mean(encrypt_times)
        desvio_enc = statistics.stdev(encrypt_times)
        rsa_enc_means.append(media_enc)

        media_dec = statistics.mean(decrypt_times)
        desvio_dec = statistics.stdev(decrypt_times)
        rsa_dec_means.append(media_dec)

        print("\n--- MESMO FICHEIRO ---")
        print(f"RSA Encrypt Média = {media_enc*1e6:.2f} µs")
        print(f"RSA Decrypt Média = {media_dec*1e6:.2f} µs")

    return rsa_enc_means, rsa_dec_means


if __name__ == "__main__":
    run_rsa()