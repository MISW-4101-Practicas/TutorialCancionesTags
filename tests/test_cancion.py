import unittest

from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.cancion import Cancion
from src.modelo.declarative_base import Session
from src.modelo.interprete import Interprete


class CancionTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()

    def test_dar_cancion_por_id(self):
        cancion = self.session.query(Cancion).filter(Cancion.titulo == "Baby blues").first()
        if cancion is None:
            nuevo_album = Album(titulo="Amapola azul", ano=2020, descripcion="Instrumental", medio="CD")
            nuevo_interprete = Interprete(nombre="Andrea Echeverri", texto_curiosidades="En ese año nacio su hijo...",
                                          cancion=-1)
            nueva_cancion = Cancion(titulo="Baby blues", minutos=3, segundos=20, compositor="Desconocido",
                                    albumes=[nuevo_album])
            nueva_cancion.interpretes.append(nuevo_interprete)
            nuevo_interprete.cancion = nueva_cancion.id
            self.session.add(nuevo_album)
            self.session.add(nuevo_interprete)
            self.session.add(nueva_cancion)
            self.session.commit()
            consulta = self.coleccion.dar_cancion_por_id(nueva_cancion.id)
        else:
            consulta = self.coleccion.dar_cancion_por_id(cancion.id)
        self.assertIsNotNone(consulta)
