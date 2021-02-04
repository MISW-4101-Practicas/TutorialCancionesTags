import unittest

from faker import Faker

from src.logica.coleccion import Coleccion
from src.modelo.cancion import Cancion
from src.modelo.declarative_base import Session
from src.modelo.interprete import Interprete


class InterpreteTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()
        # Generación de datos con libreria Faker
        self.data_factory = Faker()

    def testAgregarInterprete(self):
        nombre_interprete = self.data_factory.name()
        texto_curiosidades = self.data_factory.text()
        self.coleccion.agregar_interprete(nombre_interprete, texto_curiosidades, -1)
        consulta = self.session.query(Interprete).filter(Interprete.nombre == nombre_interprete).first().nombre
        self.assertEqual(consulta, nombre_interprete)

    def testEditarInterprete(self):
        nombre_interprete = self.data_factory.name()
        texto_curiosidades = self.data_factory.text()
        self.coleccion.agregar_interprete(nombre_interprete, texto_curiosidades, -1)
        consulta1 = self.session.query(Interprete).filter(Interprete.nombre == nombre_interprete).first().id
        consulta2 = self.coleccion.editar_interprete(consulta1, nombre_interprete, texto_curiosidades)
        self.assertTrue(consulta2)

    def testEliminarInterprete(self):
        self.coleccion.eliminar_interprete(3)
        consulta = self.session.query(Interprete).filter(Interprete.id == 3).first()
        self.assertIsNone(consulta)

    def test_buscar_sin_parametros(self):
        consulta1 = self.session.query(Cancion).all()
        consulta2 = self.coleccion.buscar_canciones_por_interprete("")
        self.assertEqual(len(consulta1), len(consulta2))

    def test_buscar_coincidencia_exacta(self):
        consulta1 = self.session.query(Interprete).filter(Interprete.nombre == "Jorge Celedón").first()
        if consulta1 is None:
            # Texto aleatorio
            texto_curiosidades = self.data_factory.text()
            self.coleccion.agregar_interprete("Jorge Celedón", texto_curiosidades, -1)
            # Nombre aleatorio
            titulo_cancion = self.data_factory.name()
            # Número aleatorio entre 0 y 60
            minutos_cancion = self.data_factory.pyint(0, 60)
            segundos_cancion = self.data_factory.pyint(0, 60)
            compositor_cancion = self.data_factory.name()
            self.coleccion.agregar_cancion(titulo_cancion, minutos_cancion, segundos_cancion, compositor_cancion, -1,
                                           [{'id': 'n', 'nombre': "Jorge Celedón",
                                             'texto_curiosidades': texto_curiosidades}])
        consulta2 = self.coleccion.buscar_canciones_por_interprete("Jorge Celedón")
        self.assertEqual(len(consulta2), 1)

    def test_buscar_cualquier_coincidencia(self):
        consulta1 = self.session.query(Interprete).filter(Interprete.nombre == "Jorge Velosa").first()
        if consulta1 is None:
            texto_curiosidades = self.data_factory.text()
            self.coleccion.agregar_interprete("Jorge Velosa", texto_curiosidades, -1)
            titulo_cancion = self.data_factory.name()
            minutos_cancion = self.data_factory.pyint(0, 60)
            segundos_cancion = self.data_factory.pyint(0, 60)
            compositor_cancion = self.data_factory.name()
            self.coleccion.agregar_cancion(titulo_cancion, minutos_cancion, segundos_cancion, compositor_cancion, -1,
                                           [{'id': 'n', 'nombre': 'Jorge Velosa',
                                             'texto_curiosidades': texto_curiosidades}])
        consulta2 = self.coleccion.buscar_canciones_por_interprete("Jorge")
        self.assertEqual(len(consulta2), 2)
