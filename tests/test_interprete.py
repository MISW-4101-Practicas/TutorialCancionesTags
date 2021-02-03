import unittest

from src.logica.coleccion import Coleccion
from src.modelo.declarative_base import Session


class InterpreteTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()
