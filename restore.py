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


def join_parts(parts_dir):
    output_path = './test/output/archivo_cifrado_reconstruido.tar.gz'
    with open(output_path, 'wb') as outfile:
        for i in range(0, len(os.listdir(parts_dir))):
            part_path = os.path.join(parts_dir, f'part{i:04}.bin')
            with open(part_path, 'rb') as part_file:
                outfile.write(part_file.read())
    return output_path

def decrypt_tar_contents(cipher_path, key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    with gzip.open(cipher_path, 'rb') as backup:
        fernet = Fernet(key)
        with tarfile.open('./test/output/archivo_descifrado.tar.gz', 'w:gz') as tar:
            for line in backup:
                filename = line.decode('utf-8').strip()
                encrypted_data = backup.readline().strip()
                original_data = fernet.decrypt(encrypted_data)
                info = tarfile.TarInfo(name=filename)
                info.size = len(original_data)
                tar.addfile(info, fileobj=io.BytesIO(original_data))

if __name__ == '__main__':
    main()
