from src.modelo.declarative_base import engine, Base


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
        return None

    def dar_canciones_de_album(self, album_id):
        return []

    def buscar_canciones_por_titulo(self, cancion_titulo):
        return None

    def agregar_interprete(self, nombre, texto_curiosidades, cancion_id):
        return None

    def editar_interprete(self, interprete_id, nombre, texto_curiosidades):
        return None

    def eliminar_interprete(self, interprete_id):
        return None
