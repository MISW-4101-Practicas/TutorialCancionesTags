import unittest

from src.logica.coleccion import Coleccion
from src.modelo.declarative_base import Session
from src.modelo.interprete import Interprete


class InterpreteTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()

    def testAgregarInterprete(self):
        self.coleccion.agregar_interprete("Adele", "La artista tenia gripa...", -1)
        consulta = self.session.query(Interprete).filter(Interprete.nombre == "Adele").first().nombre
        self.assertEqual(consulta, "Adele")

    def testEditarInterprete(self):
        self.coleccion.agregar_interprete("Lady Gaga", "Los trajes usados...", -1)
        consulta1 = self.session.query(Interprete).filter(Interprete.nombre == "Lady Gaga").first().id
        consulta2 = self.coleccion.editar_interprete(consulta1, "Lady Gaga",
                                                     "Los trajes usados fueron elaborados...")
        self.assertTrue(consulta2)
