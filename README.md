
## Ejecución


### Ambiente virtual

Teniendo instalado algúna extensión para virtualenv (python) inicie un ambiente virtual estando en el directorio raíz del proyecto.
**Nota:** Para los usuarios Linux podría ser útil usar virtualenvwrapper. Además, el uso del ambiente virtual es opcional dado que para el estado del proyecto, son pocas las librerías usadas.

[Instalación virtualenvwrapper](https://tonyj.me/blog/virtualenvwrapper-setup-linux/)


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