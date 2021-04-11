from argparse import ArgumentParser

from core.steganography import Steg


class Interface:

    parser = ArgumentParser(description='Esteganografía con python.')
    parser.add_argument('action', help='encode o decode dependiendo de la acción deseada.')
    parser.add_argument('input_file', help='nombre de la imagen con extensión.')
    parser.add_argument('-m', '--message', help='mensaje a esconder, solo usar si action == encode')
    parser.add_argument('-o', '--output', help="Nombre del archivo de salida", default="enc_output.jpg")

    parser = parser.parse_args()
    steganography = Steg(parser.input_file)

    @classmethod
    def encode(cls):
        cls.steganography.encode(cls.parser.message, cls.parser.output)

    @classmethod
    def decode(cls):
        print(cls.steganography.decode())

    @classmethod
    def launch(cls):
        if cls.parser.action == 'encode':
            cls.encode()
        elif cls.parser.action == 'decode':
            cls.decode()
