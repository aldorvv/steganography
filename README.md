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
# con el entorno virtual activado e "imagen.jpg" objetivo en images/
$ python main.py encode imagen.jpg --message="mensaje secreto" 
# con el entorno virtual activado e "output.jpg" objetivo en outputs/
$ python main.py decode output.jpg
```