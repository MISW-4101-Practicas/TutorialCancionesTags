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

    def test_editar_album(self):
        self.coleccion.editar_album(2, "Clara luna-Mix", 1982, "Sin descripción", "DISCO")
        consulta = self.session.query(Album).filter(Album.id == 2).first()
        self.assertIsNot(consulta.titulo, "Live Killers")

    def test_eliminar_album(self):
        self.coleccion.eliminar_album(1)
        consulta = self.session.query(Album).filter(Album.id == 1).first()
        self.assertIsNone(consulta)

    def test_dar_albumes(self):
        consulta1 = self.coleccion.dar_albumes()
        self.coleccion.agregar_album("New life", 2018, "Album escrito para...", "CD")
        consulta2 = self.coleccion.dar_albumes()
        self.assertGreaterEqual(len(consulta2), len(consulta1))
