from argparse import ArgumentParser

from core.steganography import Steg

class Interface:

    def __init__(self):
        self.parser = ArgumentParser(description='Esteganografía con python.')
        self.parser.add_argument('action', help='encode o decode dependiendo de la acción deseada.')
        self.parser.add_argument('input_file', help='nombre de la imagen con extensión.')
        self.parser.add_argument('-m', '--message', help='mensaje a esconder, solo usar si action == encode')
        self.parser.parse_args()

        self.steganpgraphy = Steg()
