import unittest

from src.logica.coleccion import Coleccion
from src.modelo.cancion import Cancion
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

    def testEliminarInterprete(self):
        self.coleccion.eliminar_interprete(3)
        self.consulta = self.session.query(Interprete).filter(Interprete.id == 3).first()
        self.assertIsNone(self.consulta)

    def test_buscar_sin_parametros(self):
        self.consulta1 = self.session.query(Cancion).all()
        self.consulta2 = self.coleccion.buscar_canciones_por_interprete("")
        self.assertEqual(len(self.consulta1), len(self.consulta2))

    def test_buscar_coincidencia_exacta(self):
        consulta1 = self.session.query(Interprete).filter(Interprete.nombre == "Jorge Celedón").first()
        if consulta1 is None:
            self.coleccion.agregar_interprete("Jorge Celedón", "Primera canción vallenata...", -1)
            self.coleccion.agregar_cancion("Tan natural", 2, 53, "Manuel Julian", -1,
                                           [{'id': 'n', 'nombre': 'Jorge Celedón',
                                             'texto_curiosidades': 'Primera canción vallenata...'}])
        consulta2 = self.coleccion.buscar_canciones_por_interprete("Jorge Celedón")
        self.assertEqual(len(consulta2), 1)
