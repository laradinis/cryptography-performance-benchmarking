import hashlib 
import time
import statistics

# Tamanhos dos ficheiros da alinea A
file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

sha_means = []
sha_stds = []

def run_sha():
    global sha_means, sha_stds

    sha_means = []
    sha_stds = []

    for size in file_sizes:

        print(f"\n_____________________________")
        print(f"Tamanho: {size} bytes")
        print(f"_____________________________")


        with open(f"file_{size}.txt", "rb") as f: # Lê o ficheiro correspondente ao tamanho atual geradio na alinea A
            data = f.read()
        
        times = []

        for _ in range(30): # Repetir o processo 30 vezes

            # Mede a duração do hash
            start = time.perf_counter() # Começar a medir o tempo (não coomeça a 0)
            hash_result = hashlib.sha256(data).digest() # Cálculo do hash do ficheiro
            end = time.perf_counter() # Pára o tempo
            
            times.append((end - start)) # Diferença entre start e end para saber exatamente quanto tempo demora
            
        media = statistics.mean(times) # Calcular a média dos tempos
        desvio = statistics.stdev(times) # Calcular o desvio padrão dos tempos

        sha_means.append(media)
        sha_stds.append(desvio)

        media_us = media * 1e6 # Converter a média para microsegundos
        desvio_us = desvio * 1e6 # Converter o desvio para microsegundos


        print("\n--- SHA-256 ---")
        print(f"Média = {media_us:.2f} µs")
        print(f"Desvio Padrão = {desvio_us:.2f} µs")

    return sha_means, sha_stds


if __name__ == "__main__":
    run_sha()