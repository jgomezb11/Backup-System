import sys
import os
import tarfile
import gzip
from cryptography.fernet import Fernet

def main():
    # Toma los argumentos de línea de comandos y los asigna a variables
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Verifica que la ruta de salida sea una carpeta
    if not os.path.isdir(output_path):
        raise ValueError('El path de salida no es una carpeta')

    # Inicio del proceso de backup
    print('Backup process started...')
    # Genera el archivo tar.gz y devuelve su ruta
    tar_path = generateTarfile(input_path, output_path)

    # Cifra el archivo tar.gz generado y devuelve su ruta
    encrypt_tar_path = encrypt_tar_contents(tar_path)
    print('Encrypted successfully. Starting Partitioning')

    # Divide el archivo cifrado en partes de 512 MB y las guarda en una carpeta
    split_file(encrypt_tar_path)
    print('Partitioned Successfully.')


def encrypt_tar_contents(tar_path):
    dest_path = './test/output/archivo_cifrado.tar.gz'
    key = Fernet.generate_key()
    with tarfile.open(tar_path, 'r:gz') as tar:
        with gzip.open(dest_path, 'wb') as backup:
            fernet = Fernet(key)
            for member in tar:
                original_file = tar.extractfile(member)
                original_data = original_file.read()
                encrypted_data = fernet.encrypt(original_data)
                backup.write(os.path.basename(member.name).encode('utf-8'))
                backup.write(b'\n')
                backup.write(encrypted_data)
                backup.write(b'\n')

    with open('./test/output/clave.key', 'wb') as key_file:
        key_file.write(key)

    return dest_path


def generateTarfile(input_path, output_path):
    tar_path = output_path + 'temp_.tar.gz'

    tar = tarfile.open(tar_path, "w:gz")
    for input_file in os.scandir(input_path):
        tar.add(input_file.path)
    tar.close()

    print('Tarfile generated in', tar_path)

    return tar_path


def split_file(source_path):
    chunk_size=512 * 1024 * 1024
    dest_folder = './test/output/parts/'
    with open(source_path, 'rb') as source_file:
        index = 0
        while True:
            chunk = source_file.read(chunk_size)
            if not chunk:
                break
            chunk_file_path = os.path.join(dest_folder, f'part{index:04}.bin')
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            index += 1


if __name__ == '__main__':
    main()
