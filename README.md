
# Backup-System OS

## Julian Gómez Benítez - Isaac Tadina Giraldo. Sistemas Operativos 2023-1

Herramienta desarrollada en Python que permite realizar una copia de seguridad de una carpeta en fragmentos de 512 MB, además permite restaurar la copia de seguridad a su estado original.

A partir de un directorio de entrada, al cual se le va a hacer backup, se genera un directorio comprimido (.tar) con los archivos originales, dicho directorio comprimido se particiona en fragmentos de 512 MB los cuales serán encriptados ocn el fin de dar una primera capa de seguridad al proceso.
A la hora de reconstruir el directorio para generar el copiado o backup, se desencriptan las partes generadas y se unen en otro directorio comprimido (.tar) generado. Finalmente, teniendo el directorio comprimido completo se descomprime su contenido en la ubicación especificada en la ejecución. La herramienta esta pensada para soportar varios backups.

Veamos a detalle las partes de la herramienta desarrollada:

##  1) Store.py

Se encarga de gestionar los archivos a copiar, verificadas las rutas de entrada y salida se crea el .tar a la vez que se extrae la información relevante de cada archivo a copiar (nombre y tamaño en bytes) para ser escrita en un archivo json. Se generan las particiones binarias encriptadas y se añaden las rutas para encontrar las particiones, sus respectivas llaves y la cantidad total de particiones dentro del archivo json.

## 2) Restore.py

Cargada la información de control introducida en el data.json, esta es utilizada para desencriptar las partes de 512 MB. Posteriormente se unen las partes y se genera el .tar restaurado, finalmente se descomprime en la ruta establecida.

## 3) Data.json

La herramienta de copia de seguridad está hecha para tener un registro de múltiples backups, por lo que cada uno tendra un identificador específico. Tomando como ejemplo una carpeta llamada 'input' a la cual se le hará un backup inicial 'test1', que contiene programas c y archivos de audio, la estructura sería la siguiente:

```json
[
    {
        "backup_id": "test1",
        "files": [
            {
                "name": "road.mp3",
                "size": "2225664 bytes"
            },
            {
                "name": "s1.mp3",
                "size": "4661960 bytes"
            },
            {
                "name": "proc.c",
                "size": "314 bytes"
            },
            {
                "name": "s3.mp3",
                "size": "109920 bytes"
            },
            {
                "name": "command.c",
                "size": "1410 bytes"
            },
            {
                "name": "laugh.mp3",
                "size": "156396 bytes"
            },
            {
                "name": "s2.mp3",
                "size": "89760 bytes"
            },
            {
                "name": "test.c",
                "size": "773 bytes"
            }
        ],
        "dir_name": "input",
        "parts_path": "./test/output1/parts/",
        "keys_path": "./test/output1/keys/",
        "total_parts": 1
    }
]
```
* **backup_id:** identificador del backup.
* **files:** archivos contenidos.
* **name:** nombre del archivo.
* **size:** tamaño del archivo en bytes.
* **dir_name:** nombre del directorio a copiar.
* **parts_path:** ruta donde están almacenadas todas las partes (.bin).
* **keys_path:** ruta donde están almacenadas las llaves (.key) de las partes ya mencionadas.
* **total_parts:** El total de partes de 512 MB obtenidas después de hacer el split.


## Ejecución


### Ambiente virtual

Teniendo instalado algúna extensión para virtualenv (python) inicie un ambiente virtual estando en el directorio raíz del proyecto.
**Nota:** Para los usuarios Linux podría ser útil usar virtualenvwrapper. Además, el uso del ambiente virtual es opcional dado que para el estado del proyecto, son pocas las librerías usadas.

Creación del ambiente virtual (virtualenvwrapper):

```bash
  mkvirtualenv name-of-your-virtual-env
```

Para desactivar el ambiente  virtual:

```bash
    deactivate
```

Activar nuevamente un ambiente virtual ya creado:

```bash
  workon name-of-your-virtual-env
```

Instalación de las librerías requeridas teniendo activo el ambiente virtual:

```bash
  pip install -r requirements.txt
```

### Store

Inicialmente, estando en la raíz del proyecto, se ejecuta store.py:
```bash
  python3 store.py <input-to-copy-path> <output-of-copy-path> <backup-id> <json-data-path>
```
* **input-to-copy-path:** ubicación del directorio al que se le hará backup.
* **output-of-copy-path:** ubicación del directorio donde se guardará la información necesarioa para el backup (particiones, llaves, etc).
* **backup-id:** Identificador (nombre) del backup que se quiere generar.
* **json-data-path:** ubicación del archivo data.json.
**Importante:** Esta última instrucción (json-data-path) solo se debe escribir a partir de la segunda ejecución del store.py, es decir después  de tener un primer backup en caso de quererse múltiples backups. Además, cada path debe terminar con '/' dado que se trata de directorios.

### Restore

Estando en la raíz del proyecto, se ejecuta restore.py:
```bash
  python3 restore.py <copy-location-path> <json-data-path> <backup-id>
```
* **copy-location-path:** ubicación donde quedará el backup generado.
* **json-data-path:** ubicación del archivo data.json.
* **backup-id:** Identificador (nombre) del backup que se quiere recuperar.

Hechos los pasos anteriores, el backup se genera correctamente en la ruta final especificada.

Ejemplo:

![image](https://i.ibb.co/ChtxcMt/Captura-desde-2023-04-10-22-55-31.png)