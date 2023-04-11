import tarfile
import gzip
from cryptography.fernet import Fernet
import io
import sys
import os
import json

full_data = []
data = {}

def main():
    global data, full_data
    restore_path = sys.argv[1]
    json_path = sys.argv[2]
    backup_name = sys.argv[3]

    # Cargo las rutas que se almacenan en el json
    with open(json_path, "r") as json_file:
        full_data = json.load(json_file)

    data = find_backup(full_data, backup_name)
    # Une las partes del archivo cifrado y genera el archivo original
    print('Restore process started...')
    cipher_path = join_parts(data['parts_path'], restore_path)
    print('Restored successfully.')
    decompress_tar(cipher_path, restore_path)


def find_backup(full_data, backup_name):
    return_data = None
    for backup in full_data:
        if backup['backup_id'] == backup_name:
            return_data = backup
    if not return_data:
        raise ValueError("The backup name that you specified doesn't exist...")
    return return_data


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


def decompress_tar(decrypt_tar_file, output_path):
    global data
    dest_path = output_path + data['dir_name'] + "_backup"
    os.makedirs(dest_path)
    with tarfile.open(decrypt_tar_file, 'r') as tar:
        tar.extractall(path=dest_path)
    os.remove(decrypt_tar_file)


if __name__ == '__main__':
    main()
