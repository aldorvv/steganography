from argparse import ArgumentParser

from core.steganography import Steg


class Interface:

    def __init__(self):
        _ = ArgumentParser(description='Esteganografía con python.')
        _.add_argument('action', help='encode o decode dependiendo de la acción deseada.')
        _.add_argument('input_file', help='nombre de la imagen con extensión.')
        _.add_argument('-m', '--message', help='mensaje a esconder, solo usar si action == encode')
        _.add_argument('-o', '--output', help="Nombre del archivo de salida", default="enc_output.jpg")
        self.parser = _.parse_args()

        self.steganography = Steg(self.parser.input_file)

    def encode(self):
        self.steganography.encode(self.parser.message, self.parser.output)

    def decode(self):
        print(self.steganography.decode())

    def launch(self):
        if self.parser.action == 'encode':
            self.encode()
        elif self.parser.action == 'decode':
            self.decode()