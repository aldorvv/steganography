from pathlib import Path
from typing import List

from PIL import Image
from numpy import array


class Steg:

    def __init__(self, filepath: str):
        """Inicializador de la clase."""
        filepath = Path(filepath)

        # en caso de que la imagen no se encuentre
        if not filepath.exists():
            raise FileNotFoundError(f'La imagen no se encontró dentro en {filepath}')

        # en caso de que la imagen no sea png
        if filepath.suffix != '.png':
            raise RuntimeError('Por el momento, solo funciono con imágenes png')

        self.image = Image.open(filepath, 'r')
        self.width, self.height = self.image.size

        # En caso de que la imagen cuente con valor de transparencia
        _ = self.image.mode
        self.pixel_size, self.offset = (3, 0) if _ == 'RGB' else (4, 1)

        # Convirtiendo la imagen en un arreglo de pixeles
        self.pixel_array = array(list(self.image.getdata()))

        # Calculando cuantos pixeles tiene la imagen
        self.total_pixels = self.pixel_array.size // self.pixel_size

    @staticmethod
    def __message_to_bin(message: str) -> str:
        """Convierte una cadena en un arreglo de cadenas en código binario.

        :param message: Mensaje a convertir en binario.
        :type message: str
        :return : cadena convertida a binario.
        :rtype : str
        """
        return ''.join([format(ord(letter), "08b") for letter in message])

    def encode(self, message: str, output_name: str, end_sequence: str = '::end'):
        """Esconde un mensaje en una imagen.

        :param message: Mensaje a ocultar.
        :type message: str
        :param output_name: Nombre de la imagen resultante.
        :type output_name: str
        :param end_sequence: Secuencia de texto para señalar el final del mensaje,
            evitará recorrer todos los pixeles de la imagen si al decodificar
            el mensaje ya ha sido al encontrado en su totalidad.
        :type end_sequence: str
        """
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
                    # modificando tuplas de enteros representantes de un pixel RGB o RGBA
                    self.pixel_array[index][pixel] = int(bin(self.pixel_array[index][pixel])[2:9] + bin_message[i], 2)
                    i += 1

        # Creando nueva imagen a partir del arreglo de pixeles creado
        self.pixel_array = self.pixel_array.reshape(self.height, self.width, self.pixel_size)
        encoded_image = Image.fromarray(self.pixel_array.astype('uint8'), self.image.mode)

        # Guardando imagen en output/
        output_path = Path.cwd().joinpath(f'output/{output_name}')
        encoded_image.save(output_path)

    def decode(self, end_sequence : str = "::end") -> str:
        """ Encuentra un mensaje oculto en una imagen previamente tratada con encode.

        :return : Mensaje encontrado en una imagen.
        :rtype : str
        """
        hidden_message_bits = ""
        # Recorremos pixel por pixel toda la imagen para extraer la
        # cadena binaria que lo representa
        for index in range(self.total_pixels):
            for pixel in range(self.offset, self.pixel_size):
                # anexamos lo obtenido a la cadena
                hidden_message_bits += bin(self.pixel_array[index][pixel])[2:][-1]

        # Separando la cadena binaria en fragmentos de 8 caracteres
        hidden_message_bits = [hidden_message_bits[i:i+8] for i in range(0, len(hidden_message_bits), 8)]

        message = ""
        for i in range(len(hidden_message_bits)):
            # En caso de que la cadena no haya terminado ya
            if message[-1 * len(end_sequence):] != end_sequence:
                # Agregamos la representación de un caracter ascii del binario
                # a la cadena final
                message += chr(int(hidden_message_bits[i], 2))

        # Si el mensaje existe, es decir, es diferente a ""
        if message:
            return f"Mensaje: {message[:-1 * len(end_sequence)]}"

        # en caso contrario, el else no es necesario dado el previo return
        return "No se encontró ningún mensaje en esta imagen"