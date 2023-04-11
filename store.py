import sys
import os
import tarfile
import gzip
import json
from cryptography.fernet import Fernet

full_data = []
data = {}

def main():
    global data, full_data
    # Toma los argumentos de línea de comandos y los asigna a variables
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    backup_name = sys.argv[3]
    if len(sys.argv) > 4:
        json_path = sys.argv[4]
        with open(json_path, "r") as json_file:
            full_data = json.load(json_file)
        if is_repeated_name(full_data, backup_name):
            raise ValueError('That name is already used.')
    else:
        json_path = output_path + 'data.json'

    data['backup_id'] = backup_name
    # Verifica que la ruta de salida sea una carpeta
    if not os.path.isdir(input_path):
        raise ValueError('Input path is not a valid directory.')

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Inicio del proceso de backup
    print('Backup process started...')
    # Genera el archivo tar.gz y devuelve su ruta
    tar_path = generateTarfile(input_path, output_path)

    print('Zipped successfully. Starting Partitioning')

    # Divide el archivo cifrado en partes de 512 MB y las guarda en una carpeta
    split_file(tar_path, output_path)
    print('Partitioned Successfully.')


    full_data.append(data)
    with open(json_path, 'w') as f:
        json.dump(full_data, f, indent=4)


def is_repeated_name(full_data, backup_name):
    exist = False
    for backup in full_data:
        if backup['backup_id'] == backup_name:
            exist = True
    return exist


def generateTarfile(input_path, output_path):
    global data
    data['files'] = []
    tar_path = output_path + 'temp_.tar.gz'

    tar = tarfile.open(tar_path, "w:gz")
    index_last_slash = input_path.rfind("/")
    if len(input_path) == index_last_slash + 1:
        dir_name = input_path[input_path[0:-1].rfind("/") + 1:index_last_slash]
    else:
        dir_name = input_path[index_last_slash + 1:]
    data["dir_name"] = dir_name
    for input_file in os.scandir(input_path):
        tar.add(input_file.path, arcname=os.path.basename(input_file.path))
        data['files'].append({'name':input_file.name, 'size':f'{os.path.getsize(input_file.path)} bytes'})
    tar.close()

    print('Tarfile generated in', tar_path)

    return tar_path


def encrypt_part(chunk, index, output_path):
    global data
    key_dest_folder = output_path + 'keys/'
    if not os.path.exists(key_dest_folder):
        os.makedirs(key_dest_folder)
    data['keys_path'] = key_dest_folder
    key = Fernet.generate_key()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(chunk)

    chunk_key_path = os.path.join(key_dest_folder, f'key{index:04}.key')
    with open(chunk_key_path, 'wb') as key_file:
        key_file.write(key)

    return encrypted_data, chunk_key_path


def split_file(source_path, output_path):
    global data
    dest_folder = output_path + 'parts/'
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    data['parts_path'] = dest_folder
    chunk_size=512 * 1024 * 1024
    with open(source_path, 'rb') as source_file:
        index = 0
        while True:
            chunk = source_file.read(chunk_size)
            if not chunk:
                break
            chunk_file_path = os.path.join(dest_folder, f'part{index:04}.bin')
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(encrypt_part(chunk, index, output_path)[0])

            index += 1
    data['total_parts'] = index
    os.remove(source_path)


if __name__ == '__main__':
    main()
