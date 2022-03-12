from modelo.album import Album, Medio
from modelo.cancion import Cancion
from modelo.declarative_base import engine, Base, session
from modelo.interprete import Interprete


class Coleccion():

    def __init__(self):
        Base.metadata.create_all(engine)

    def agregar_album(self, titulo, anio, descripcion, medio):
        busqueda = session.query(Album).filter(Album.titulo == titulo).all()
        if len(busqueda) == 0:
            album = Album(titulo=titulo, ano=anio, descripcion=descripcion, medio=medio)
            session.add(album)
            session.commit()
            return True
        else:
            return False

    def dar_medios(self):
        return [medio.name for medio in Medio]

    def editar_album(self, album_id, titulo, anio, descripcion, medio):
        busqueda = session.query(Album).filter(Album.titulo == titulo, Album.id != album_id).all()
        if len(busqueda) == 0:
            album = session.query(Album).filter(Album.id == album_id).first()
            album.titulo = titulo
            album.ano = anio
            album.descripcion = descripcion
            album.medio = medio
            session.commit()
            return True
        else:
            return False

    def eliminar_album(self, album_id):
        try:
            album = session.query(Album).filter(Album.id == album_id).first()
            session.delete(album)
            session.commit()
            return True
        except:
            return False

    def dar_albumes(self):
        albumes = [elem.__dict__ for elem in session.query(Album).all()]
        for album in albumes:
            album["interpretes"] = self.dar_interpretes_de_album(album["id"])
        return albumes

    def dar_interpretes_de_album(self, album_id):
        canciones = session.query(Cancion).filter(Cancion.albumes.any(Album.id.in_([album_id]))).all()
        interpretes = []
        for cancion in canciones:
            for interprete in cancion.interpretes:
                interpretes.append(interprete.nombre)
        return interpretes

    def dar_album_por_id(self, album_id):
        return session.query(Album).get(album_id).__dict__

    def buscar_albumes_por_titulo(self, album_titulo):
        albumes = [elem.__dict__ for elem in
                   session.query(Album).filter(Album.titulo.ilike('%{0}%'.format(album_titulo))).all()]
        return albumes

    def agregar_cancion(self, titulo, minutos, segundos, compositor, album_id, interpretes):
        interpretesCancion = []
        if len(interpretes) == 0:
            return False
        else:
            if album_id > 0:
                busqueda = session.query(Cancion).filter(Cancion.albumes.any(Album.id.in_([album_id])),
                                                         Cancion.titulo == titulo).all()
                if len(busqueda) == 0:
                    album = session.query(Album).filter(Album.id == album_id).first()
                    nuevaCancion = Cancion(titulo=titulo, minutos=minutos, segundos=segundos, compositor=compositor,
                                           albumes=[album])
                    for item in interpretes:
                        interprete = Interprete(nombre=item["nombre"], texto_curiosidades=item["texto_curiosidades"],
                                                cancion=nuevaCancion.id)
                        session.add(interprete)
                        interpretesCancion.append(interprete)
                    nuevaCancion.interpretes = interpretesCancion
                    session.add(nuevaCancion)
                    session.commit()
                    return True
                else:
                    return False
            else:
                nuevaCancion = Cancion(titulo=titulo, minutos=minutos, segundos=segundos, compositor=compositor)
                for item in interpretes:
                    interprete = Interprete(nombre=item["nombre"], texto_curiosidades=item["texto_curiosidades"],
                                            cancion=nuevaCancion.id)
                    session.add(interprete)
                    interpretesCancion.append(interprete)
                nuevaCancion.interpretes = interpretesCancion
                session.add(nuevaCancion)
                session.commit()
                return True

    def editar_cancion(self, cancion_id, titulo, minutos, segundos, compositor, interpretes):
        busqueda = session.query(Cancion).filter(Cancion.titulo == titulo, Cancion.id != cancion_id).all()
        if len(busqueda) == 0:
            cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
            cancion.titulo = titulo
            cancion.minutos = minutos
            cancion.segundos = segundos
            cancion.compositor = compositor
            for item in interpretes:
                if item["id"] == "n":
                    interprete = Interprete(nombre=item["nombre"], texto_curiosidades=item["texto_curiosidades"],
                                            cancion=cancion.id)
                    session.add(interprete)
                    cancion.interpretes.append(interprete)
                else:
                    self.editar_interprete(item["id"], item["nombre"], item["texto_curiosidades"])
            session.commit()
            return True
        else:
            return False

    def eliminar_cancion(self, cancion_id):
        try:
            cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
            if cancion is not None:
                session.delete(cancion)
                session.commit()
                return True
            else:
                return False
        except:
            return False

    def dar_canciones(self):
        canciones = [elem.__dict__ for elem in session.query(Cancion).all()]
        return canciones

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

    def buscar_canciones_por_interprete(self, interprete_nombre):
        if interprete_nombre == "":
            canciones = session.query(Cancion).all()
        else:
            canciones = session.query(Cancion).filter(
                Cancion.interpretes.any(Interprete.nombre.ilike('%{0}%'.format(interprete_nombre)))).all()
        return canciones
    
    def asociar_cancion(self, cancion_id, album_id):
        cancion = session.query(Cancion).filter(Cancion.id == cancion_id).first()
        album = session.query(Album).filter(Album.id == album_id).first()
        if cancion is not None and album is not None:
            album.canciones.append(cancion)
            session.commit()
            return True
        else:
            return False

    def agregar_interprete(self, nombre, texto_curiosidades, cancion_id):
        busqueda = session.query(Interprete).filter(Interprete.nombre == nombre).all()
        if len(busqueda) == 0:
            if cancion_id > 0:
                nuevoInterprete = Interprete(nombre=nombre, texto_curiosidades=texto_curiosidades, cancion=cancion_id)
            else:
                nuevoInterprete = Interprete(nombre=nombre, texto_curiosidades=texto_curiosidades)
            session.add(nuevoInterprete)
            session.commit()
            return True
        else:
            return False

    def editar_interprete(self, interprete_id, nombre, texto_curiosidades):
        busqueda = session.query(Interprete).filter(Interprete.id != interprete_id, Interprete.nombre == nombre).all()
        if len(busqueda) == 0:
            interprete = session.query(Interprete).filter(Interprete.id == interprete_id).first()
            interprete.nombre = nombre
            interprete.texto_curiosidades = texto_curiosidades
            session.commit()
            return True
        else:
            return False

    def eliminar_interprete(self, interprete_id):
        try:
            interprete = session.query(Interprete).filter(Interprete.id == interprete_id).first()
            session.delete(interprete)
            session.commit()
            return True
        except:
            return False

    def dar_interpretes(self):
        interpretes = [elem.__dict__ for elem in session.query(Interprete).all()]
        return interpretes

    def buscar_interpretes_por_nombre(self, interprete_nombre):
        interpretes = [elem.__dict__ for elem in session.query(Interprete).filter(
            Interprete.nombre.ilike('%{0}%'.format(interprete_nombre))).all()]
        return interpretes