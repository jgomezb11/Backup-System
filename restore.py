import tarfile
import gzip
from cryptography.fernet import Fernet
import io
import sys
import os
import json

data = {}

def main():
    global data
    restore_path = sys.argv[1]
    json_path = sys.argv[2]

    # Cargo las rutas que se almacenan en el json
    with open(json_path, "r") as json_file:
        data = json.load(json_file)

    # Une las partes del archivo cifrado y genera el archivo original
    cipher_path = join_parts(data['parts_path'], restore_path)
    print('Restore process started...')
    decrypt_file = decrypt_tar_contents(cipher_path, data['tar_key'], restore_path)
    print('Restored successfully.')
    decompress_tar(decrypt_file, restore_path)


def join_parts(parts_dir, restore_path):
    global data
    output_path = restore_path + 'archivo_cifrado_reconstruido.tar.gz'
    with open(output_path, 'wb') as outfile:
        for i in range(0, len(os.listdir(parts_dir))):
            part_path = os.path.join(parts_dir, f'part{i:04}.bin')
            key_path = os.path.join(data['keys_path'], f'key{i:04}.key')
            with open(key_path, 'rb') as key_file:
                key_data = key_file.read()
            with open(part_path, 'rb') as part_file:
                outfile.write(decrypt_part(part_file.read(), key_data))
    return output_path


def decrypt_part(encrypted_data, key):
    fernet = Fernet(key)
    original_chunk = fernet.decrypt(encrypted_data)
    return original_chunk


def decrypt_tar_contents(cipher_path, key_path, restore_path):
    decrypt_tar_file_path = restore_path + 'archivo_descifrado.tar.gz'
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
    os.remove(cipher_path)
    return decrypt_tar_file_path


def decompress_tar(decrypt_tar_file, output_path):
    global data
    dest_path = output_path + data['dir_name'] + "_backup"
    os.makedirs(dest_path)
    with tarfile.open(decrypt_tar_file, 'r') as tar:
        tar.extractall(path=dest_path)
    os.remove(decrypt_tar_file)


if __name__ == '__main__':
    main()
