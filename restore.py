import tarfile
import gzip
from cryptography.fernet import Fernet
import io
import sys
import os

def main():
    parts_path = sys.argv[1]
    key_path = sys.argv[2]
    # Une las partes del archivo cifrado y genera el archivo original
    cipher_path = join_parts(parts_path)

    print('Restore process started...')
    decrypt_tar_contents(cipher_path, key_path)
    print('Restored successfully.')


def join_parts(parts_dir):
    output_path = './test/output/archivo_cifrado_reconstruido.tar.gz'
    with open(output_path, 'wb') as outfile:
        for i in range(0, len(os.listdir(parts_dir))):
            part_path = os.path.join(parts_dir, f'part{i:04}.bin')
            with open(part_path, 'rb') as part_file:
                outfile.write(part_file.read())
    return output_path


def decrypt_part(encrypted_data, key):
    fernet = Fernet(key)
    original_chunk = fernet.decrypt(encrypted_data)

    return original_chunk


def decrypt_tar_contents(cipher_path, key_path):
    decrypt_tar_file_path =' ./test/output/archivo_descifrado.tar.gz'
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    with gzip.open(cipher_path, 'rb') as backup:
        fernet = Fernet(key)
        with tarfile.open(decrypt_tar_file_path, 'w:gz') as tar:
            for line in backup:
                filename = line.decode('utf-8').strip()
                encrypted_data = backup.readline().strip()
                original_data = fernet.decrypt(encrypted_data)
                info = tarfile.TarInfo(name=filename)
                info.size = len(original_data)
                tar.addfile(info, fileobj=io.BytesIO(original_data))
    
    return decrypt_tar_file_path


def decompress_tar(decrypt_tar_file, output_path):
    with tarfile.open(decrypt_tar_file, 'r') as tar:
        tar.extractall(path=output_path)


if __name__ == '__main__':
    main()
