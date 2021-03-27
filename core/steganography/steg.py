from pathlib import Path

from PIL import Image

class Steg:

    def __init__(self, filename):
        filepath = Path.cwd().joinpath(f'images/{filename}')
        if not filepath.exists():
            raise FileNotFoundError('La imagen no se encontró dentro de la carpeta "images"')

        self.image = Image.open(filepath, 'rb')

