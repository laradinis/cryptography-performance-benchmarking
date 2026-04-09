import matplotlib.pyplot as plt
import ParteB as pb
import statistics
import ParteC as pc
import ParteD as pd

pb.run_aes()
pc.run_rsa()
pd.run_sha()



def plot_encryption_variability_AES():
    


    indices = [2, 3, 5]  # 512, 4096, 262144 bytes
    labels_sizes = ['512B', '4096B', '262144B']

    plt.figure(figsize=(8,5))

    positions = []
    data = []
    labels = []

    pos = 1

    for i, label in zip(indices, labels_sizes):
        # FIXO
        data.append(pb.encrypt_times_all[i])
        labels.append(f'{label}\nFixed')
        positions.append(pos)
        pos += 1

        # RANDOM
        data.append(pb.encrypt_times_rand_all[i])
        labels.append(f'{label}\nRandom')
        positions.append(pos)
        pos += 2  # espaço entre grupos

    plt.boxplot(data, positions=positions)

    plt.xticks(positions, labels)
    plt.ylabel('Time (µs)')
    plt.title('AES Encryption Variability (Fixed vs Random)')
    plt.yscale('log')
    plt.grid(True)

    plt.savefig("aes1_boxplot.png", dpi=300, bbox_inches='tight')
    plt.show()

def plot_decryption_variability_AES():
    


    indices = [2, 3, 5]  # 512, 4096, 262144 bytes
    labels_sizes = ['512B', '4096B', '262144B']

    plt.figure(figsize=(8,5))

    positions = []
    data = []
    labels = []

    pos = 1

    for i, label in zip(indices, labels_sizes):
        # FIXO
        data.append(pb.decrypt_times_all[i])
        labels.append(f'{label}\nFixed')
        positions.append(pos)
        pos += 1

        # RANDOM
        data.append(pb.decrypt_times_rand_all[i])
        labels.append(f'{label}\nRandom')
        positions.append(pos)
        pos += 2  # espaço entre grupos

    plt.boxplot(data, positions=positions)

    plt.xticks(positions, labels)
    plt.ylabel('Time (µs)')
    plt.title('AES Decryption Variability (Fixed vs Random)')
    plt.yscale('log')
    plt.grid(True)

    plt.savefig("aes2_boxplot.png", dpi=300, bbox_inches='tight')
    plt.show()

def CV_AES_encryption():


    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    # calcular CV
    cv_fixed = [statistics.stdev(pb.encrypt_times_all[i]) / statistics.mean(pb.encrypt_times_all[i])
                for i in range(len(file_sizes))]

    cv_random = [statistics.stdev(pb.encrypt_times_rand_all[i]) / statistics.mean(pb.encrypt_times_rand_all[i])
                for i in range(len(file_sizes))]

    plt.figure(figsize=(7,5))

    plt.plot(file_sizes, cv_fixed, marker='o', label='Fixed')
    plt.plot(file_sizes, cv_random, marker='o', label='Random')

    plt.xscale('log')
    plt.xticks(file_sizes, file_sizes)
    plt.xlabel('File Size (bytes)')
    plt.ylabel('Coefficient of Variation')
    plt.title('AES Encryption Stability')
    plt.legend()
    plt.grid(True)

    plt.savefig("aes_cv_encrypt.png", dpi=300, bbox_inches='tight')
    plt.show()

def CV_AES_decryption():



    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    # calcular CV
    cv_fixed = [statistics.stdev(pb.decrypt_times_all[i]) / statistics.mean(pb.decrypt_times_all[i])
                for i in range(len(file_sizes))]

    cv_random = [statistics.stdev(pb.decrypt_times_rand_all[i]) / statistics.mean(pb.decrypt_times_rand_all[i])
                for i in range(len(file_sizes))]

    plt.figure(figsize=(7,5))

    plt.plot(file_sizes, cv_fixed, marker='o', label='Fixed')
    plt.plot(file_sizes, cv_random, marker='o', label='Random')

    plt.xscale('log')
    plt.xticks(file_sizes, file_sizes)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Coefficient of Variation')
    plt.title('AES Decryption Stability')
    plt.legend()
    plt.grid(True)

    plt.savefig("aes_cv_decrypt.png", dpi=300, bbox_inches='tight')
    plt.show()

def AES_time_size_comparison():



    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    # converter para µs
    enc = [x * 1e6 for x in pb.aes_enc_means]
    dec = [x * 1e6 for x in pb.aes_dec_means]

    plt.figure(figsize=(8,5))

    plt.plot(file_sizes, enc, marker='o', label='AES Encrypt', linewidth=2)
    plt.plot(file_sizes, dec, marker='o', label='AES Decrypt', linewidth=2)

    plt.xscale('log')
    plt.yscale('log')

    #mostrar valores reais no eixo X
    plt.xticks(file_sizes, file_sizes, rotation=45)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (µs)')
    plt.title('AES Performance')

    plt.grid(True)
    plt.legend()

    plt.savefig("aes_general.png", dpi=300, bbox_inches='tight')
    plt.show()

def rsa_time_size_comparison():



    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]
    

    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    # converter para µs
    enc = [x * 1e6 for x in pc.rsa_enc_means]
    dec = [x * 1e6 for x in pc.rsa_dec_means]

    plt.figure(figsize=(8,5))

    plt.plot(file_sizes, enc, marker='o', label='RSA Encrypt', linewidth=2)
    plt.plot(file_sizes, dec, marker='o', label='RSA Decrypt', linewidth=2)

    plt.xscale('log')
    plt.yscale('log')

    plt.xticks(file_sizes, file_sizes, rotation=45)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (µs)')
    plt.title('RSA Performance')

    plt.grid(True)
    plt.legend()

    plt.savefig("rsa_general.png", dpi=300, bbox_inches='tight')
    plt.show()

def sha_time_size_comparison():




    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    # converter para µs

    plt.figure(figsize=(8,5))

    means = [x * 1e6 for x in pd.sha_means]

    plt.plot(file_sizes, means, marker='o', linewidth=2, label='SHA-256')

    plt.xscale('log')
    plt.yscale('log')

    plt.xticks(file_sizes, file_sizes, rotation=45)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (µs)')
    plt.title('SHA-256 Performance')

    plt.grid(True)
    plt.legend()

    plt.savefig("sha_general.png", dpi=300, bbox_inches='tight')
    plt.show()

def compare_encryption_all():



    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    # converter para µs
    aes_enc = [x * 1e6 for x in pb.aes_enc_means]
    rsa_enc = [x * 1e6 for x in pc.rsa_enc_means]
    sha = [x * 1e6 for x in pd.sha_means]

    plt.figure(figsize=(8,5))

    plt.plot(file_sizes, aes_enc, marker='o', label='AES Encrypt', linewidth=2)
    plt.plot(file_sizes, rsa_enc, marker='o', label='RSA Encrypt', linewidth=2)
    plt.plot(file_sizes, sha, marker='o', label='SHA-256', linewidth=2)

    plt.xscale('log')
    plt.yscale('log')

    plt.xticks(file_sizes, file_sizes, rotation=45)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (µs)')
    plt.title('Encryption / Hash Performance Comparison')

    plt.grid(True)
    plt.legend()

    plt.savefig("compare_encrypt.png", dpi=300, bbox_inches='tight')
    plt.show()


def compare_decryption_all():




    file_sizes = [8, 64, 512, 4096, 32768, 262144, 2097152]

    aes_dec = [x * 1e6 for x in pb.aes_dec_means]
    rsa_dec = [x * 1e6 for x in pc.rsa_dec_means]

    plt.figure(figsize=(8,5))

    plt.plot(file_sizes, aes_dec, marker='o', label='AES Decrypt', linewidth=2)
    plt.plot(file_sizes, rsa_dec, marker='o', label='RSA Decrypt', linewidth=2)

    plt.xscale('log')
    plt.yscale('log')

    plt.xticks(file_sizes, file_sizes, rotation=45)

    plt.xlabel('File Size (bytes)')
    plt.ylabel('Time (µs)')
    plt.title('Decryption Performance Comparison')

    plt.grid(True)
    plt.legend()

    plt.savefig("compare_decrypt.png", dpi=300, bbox_inches='tight')
    plt.show()

