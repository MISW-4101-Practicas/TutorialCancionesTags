import unittest

from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.declarative_base import Session


class AlbumTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()

    def test_agregar_album(self):
        self.coleccion.agregar_album("Mio", 2000, "Sin descripción", "CD")
        self.coleccion.agregar_album("Live Killers", 1975, "Sin descripción", "CASETE")
        self.coleccion.agregar_album("Clara luna", 1992, "Sin descripción", "CASETE")
        consulta1 = self.session.query(Album).filter(Album.titulo == "Mio").first()
        consulta2 = self.session.query(Album).filter(Album.id == 2).first()
        self.assertEqual(consulta1.titulo, "Mio")
        self.assertIsNotNone(consulta2)
