from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import timeit
import statistics
from os import urandom

#_____________________ENCRIPTAR_____________________#
def aes_encrypt_file(data, key):
    nonce = urandom(16) # Número aleatório de 16 bytes

    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce)) # Modo de cifrar (o algorítmo: (AES) e o modo: (CTR))
    encryptor = cipher.encryptor()                             

    ciphertext = encryptor.update(data) + encryptor.finalize() # Encriptar o texto + termina o processo

    return nonce, ciphertext                   


#_____________________DESENCRIPTAR_____________________#
def aes_decrypt_file(ciphertext, key, nonce):
    
    #Argumentos:
        #ciphertext: texto cifrado
        #key: mesma chave usada para a encriptação
        #nonce: mesmo valor aleatório usado na encriptação (16 bytes)
    
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    
    decrypted_text = decryptor.update(ciphertext) + decryptor.finalize() # Desencripta os dados
    
    return decrypted_text


#________________________TESTE_________________________#
key = urandom(32) # Chave de 32 bytes/256 bits
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152] # Tamanhos dos ficheiros


aes_enc_means = []
aes_dec_means = []
aes_enc_means_rand = []
aes_dec_means_rand = []

encrypt_times_all = []
decrypt_times_all = []
encrypt_times_rand_all = []
decrypt_times_rand_all = []




def run_aes():
    global aes_enc_means, aes_dec_means
    global aes_enc_means_rand, aes_dec_means_rand
    global encrypt_times_all, decrypt_times_all
    global encrypt_times_rand_all, decrypt_times_rand_all

    aes_enc_means = []
    aes_dec_means = []
    aes_enc_means_rand = []
    aes_dec_means_rand = []

    encrypt_times_all = []
    decrypt_times_all = []
    encrypt_times_rand_all = []
    decrypt_times_rand_all = []

    for size in file_sizes:
        print(f"\n-____ Teste tamanho: {size} bytes ___")
        
        # Gerar dados aleatórios
        with open(f"file_{size}.txt", "rb") as f:
            data = f.read()

        # ======================================================
        #  TESTE COM MESMO FICHEIRO (FIXO)
        # ======================================================

        encrypt_times = []
        decrypt_times = []

        # Preparar decrypt (fixo)
        nonce, ciphertext = aes_encrypt_file(data, key)

        for _ in range(30):
            # ENCRYPT
            t_enc = timeit.timeit(lambda: aes_encrypt_file(data, key), number=1)
            encrypt_times.append(t_enc)

            # DECRYPT
            t_dec = timeit.timeit(lambda: aes_decrypt_file(ciphertext, key, nonce), number=1)
            decrypt_times.append(t_dec)

        # guardar para boxplot
        encrypt_times_all.append([t * 1e6 for t in encrypt_times])
        decrypt_times_all.append([t * 1e6 for t in decrypt_times])
        

        print("\n--- MESMO FICHEIRO ---")

        media_enc = statistics.mean(encrypt_times)
        desvio_enc = statistics.stdev(encrypt_times)
        aes_enc_means.append(media_enc)


        print("\nAES Encriptação")
        print(f"Média = {media_enc*1e6:.2f} µs")
        print(f"Desvio = {desvio_enc*1e6:.2f} µs")

        media_dec = statistics.mean(decrypt_times)
        desvio_dec = statistics.stdev(decrypt_times)
        aes_dec_means.append(media_dec)

        print("\nAES Decriptação")
        print(f"Média = {media_dec*1e6:.2f} µs")
        print(f"Desvio = {desvio_dec*1e6:.2f} µs")

        # ______________________________________________________
        # TESTE COM FICHEIROS ALEATÓRIOS DIFERENTES
        # ______________________________________________________

        encrypt_times_rand = []
        decrypt_times_rand = []

        for _ in range(10): # 10 ficheiros diferentes
            data_random = urandom(size)

            # ENCRYPT
            t_enc = timeit.timeit(lambda: aes_encrypt_file(data_random, key), number=1)
            encrypt_times_rand.append(t_enc)

            # Preparar decrypt (cada vez novo)
            nonce, ciphertext = aes_encrypt_file(data_random, key)

            # DECRYPT
            t_dec = timeit.timeit(lambda: aes_decrypt_file(ciphertext, key, nonce), number=1)
            decrypt_times_rand.append(t_dec)
        
        # guardar para boxplot
        encrypt_times_rand_all.append([t * 1e6 for t in encrypt_times_rand])
        decrypt_times_rand_all.append([t * 1e6 for t in decrypt_times_rand])

        print("\n--- FICHEIROS DIFERENTES ---")

        media_enc_rand = statistics.mean(encrypt_times_rand)
        desvio_enc_rand = statistics.stdev(encrypt_times_rand)
        aes_enc_means_rand.append(media_enc_rand)

        print("\nAES Encriptação")
        print(f"Média = {media_enc_rand*1e6:.2f} µs")
        print(f"Desvio = {desvio_enc_rand*1e6:.2f} µs")

        media_dec_rand = statistics.mean(decrypt_times_rand)
        desvio_dec_rand = statistics.stdev(decrypt_times_rand)
        aes_dec_means_rand.append(media_dec_rand)

        print("\nAES Decriptação")
        print(f"Média = {media_dec_rand*1e6:.2f} µs")
        print(f"Desvio = {desvio_dec_rand*1e6:.2f} µs")

    return (
        aes_enc_means,
        aes_dec_means,
        aes_enc_means_rand,
        aes_dec_means_rand,
        encrypt_times_all,
        decrypt_times_all,
        encrypt_times_rand_all,
        decrypt_times_rand_all
    )

if __name__ == "__main__":
    run_aes()