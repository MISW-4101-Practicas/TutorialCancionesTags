from src.modelo.cancion import Cancion
from src.modelo.declarative_base import engine, Base, session
from src.modelo.interprete import Interprete


class Coleccion():

    def __init__(self):
        Base.metadata.create_all(engine)

    def agregar_album(self, titulo, anio, descripcion, medio):
        return None

    def editar_album(self, album_id, titulo, anio, descripcion, medio):
        return None

    def eliminar_album(self, album_id):
        return None

    def dar_albumes(self):
        return None

    def dar_album_por_id(self, album_id):
        return None

    def buscar_albumes_por_titulo(self, album_titulo):
        return None

    def editar_cancion(self, cancion_id, titulo, minutos, segundos, compositor, interpretes):
        return None

    def eliminar_cancion(self, cancion_id):
        return None

    def dar_cancion_por_id(self, cancion_id):
        cancion = session.query(Cancion).filter_by(id=cancion_id).first()
        cancion_dict = cancion.__dict__
        cancion_dict["interpretes"] = [self.dar_interprete_por_id(interprete.id) for interprete in cancion.interpretes]
        return cancion_dict

    def dar_interprete_por_id(self, interprete_id):
        return session.query(Interprete).filter_by(id=interprete_id).first().__dict__

    def dar_canciones_de_album(self, album_id):
        return []

    def buscar_canciones_por_titulo(self, cancion_titulo):
        canciones = [elem.__dict__ for elem in
                     session.query(Cancion).filter(Cancion.titulo.ilike('%{0}%'.format(cancion_titulo))).all()]
        return canciones

    def agregar_interprete(self, nombre, texto_curiosidades, cancion_id):
        return None

    def editar_interprete(self, interprete_id, nombre, texto_curiosidades):
        return None

    def eliminar_interprete(self, interprete_id):
        return None
