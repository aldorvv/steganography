## Steganography

Script escrito en Python 3.9 para implementar esteganografía.

### Instalación

```
$ git clone https://github.com/aldorvv/steganography.git
$ cd steganography/
$ virtualenv .venv && source .venv/bin/activate
$ pip install -r requirements.txt
```

### Uso

```
$ # Dentro del directorio
$ chmod +x ./steganos.py
$ ./steganos.py encode /path/hasta/imagen.png --message="mensaje secreto" --output output.png
$ ./steganos.py decode /path/hasta/output.png
```