from pathlib import Path
from typing import List

from PIL import Image
from numpy import array


class Steg:

    def __init__(self, filename: str):
        """Inicializador de la clase."""
        filepath = Path.cwd().joinpath(f'images/{filename}')
        # En caso de que no exista el archivo o no esté dentro de images/
        if not filepath.exists():
            raise FileNotFoundError('La imagen no se encontró dentro de la carpeta "images"')

        self.image = Image.open(filepath, 'r')
        self.width, self.height = self.image.size

        # En caso de que la imagen cuente con valor de transparencia
        _ = self.image.mode
        self.pixel_size, self.offset = (3, 0) if _ == 'RGB' else (4, 1)
        self.pixel_array = array(list(self.image.getdata()))
        self.total_pixels = self.pixel_array.size // self.pixel_size

    @staticmethod
    def __message_to_bin(message: str) -> List[str]:
        """Convierte una cadena en un arreglo de cadenas en código binario."""
        return [format(ord(letter), "08b") for letter in message]

    def encode(self, message: str, output_name: str, end_sequence: str = '::end'):
        # Agregamos una secuencia de caracteres en caso de que
        message_to_encode = f'{message}{end_sequence}'

        bin_message = self.__message_to_bin(message_to_encode)
        min_pixels = len(bin_message)

        # En caso de que el mensage sea de un tamaño mayor al que la imagen
        # pueda guardar
        if min_pixels > self.total_pixels:
            raise RuntimeError('Necesito una imagen más grande.')

        # Recorriendo todos los pixeles de la imagen
        # y modificando valores rgb o rgba para ocultar
        # el mensaje.
        i = 0
        for index in range(self.total_pixels):
            for pixel in range(self.offset, self.pixel_size):
                if i < min_pixels:
                    self.pixel_array[index][pixel] = int(bin(self.pixel_array[index][pixel])[2:9] + bin_message[i], 2)
                    i += 1

        # Creando nueva imagen a partir del arreglo de pixeles creado
        self.pixel_array = self.pixel_array.reshape(self.height, self.width, self.pixel_size)
        encoded_image = Image.fromarray(self.pixel_array.astype('uint8'), self.image.mode)

        # Guardando imagen en output/
        output_path = Path.cwd().joinpath(f'output/{output_name}')
        encoded_image.save(output_path)
