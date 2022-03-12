from PyQt5.QtWidgets import QApplication, QMessageBox
from vista.vista_album import Ventana_Album
from vista.vista_busqueda import Ventana_Inicial
from vista.vista_cancion import Ventana_Cancion
from vista.vista_lista_album import Ventana_Lista_Album
from vista.vista_lista_cancion import Ventana_Lista_Canciones


class App(QApplication):
    '''
    Clase principal de la interfaz
    '''

    def __init__(self, sys_argv, logica):
        '''
        Constructor de la interfaz
        '''
        super(App, self).__init__(sys_argv)

        # Lógica de la aplicación
        self.logica = logica

        # Se inicializan todas las ventanas
        self.ventana_buscar = Ventana_Inicial(self)
        self.ventana_lista_album = Ventana_Lista_Album(self)
        self.ventana_album = Ventana_Album(self)
        self.ventana_lista_canciones = Ventana_Lista_Canciones(self)
        self.ventana_cancion = Ventana_Cancion(self)

        # Se comienza en la lista de albums
        self.mostrar_ventana_lista_albums()

    def mostrar_ventana_lista_albums(self):
        '''
        Método para mostrar la ventana de la lista de albums
        '''
        self.ventana_lista_album.show()
        self.ventana_lista_album.mostrar_albums(self.logica.dar_albumes())

    def mostrar_ventana_album(self, indice_album):
        '''
        Método para mostrar un album en particular
        '''
        self.ventana_album.show()
        self.ventana_album.mostrar_album(self.logica.dar_album_por_id(indice_album))
        self.ventana_album.mostrar_canciones(self.logica.dar_canciones_de_album(indice_album))

    def mostrar_ventana_lista_canciones(self):
        '''
        Método para mostrar la ventana de la lista de canciones
        '''
        self.ventana_lista_canciones.show()
        self.ventana_lista_canciones.mostrar_canciones(self.logica.dar_canciones())

    def mostrar_ventana_cancion(self, nueva=False, id_album=-1, id_cancion=-1):
        '''
        Método para mostrar la ventana de una canción.
        Si el parámetro nueva es True, se crea para añadir una nueva canción.
        El parámetro id_album indica si la ventana se despliega desde un album.
        El parámetro id_cancion indica que canción existente se debe mostrar
        '''
        self.ventana_cancion.id_album = id_album
        if not nueva:
            cancion = self.logica.dar_cancion_por_id(
                self.ventana_cancion.cancion_actual["id"] if id_cancion == -1 else id_cancion)
            self.ventana_cancion.mostrar_cancion(cancion)
            self.ventana_cancion.mostrar_interpretes(cancion["interpretes"])
        else:
            self.ventana_cancion.mostrar_cancion()
        self.ventana_cancion.show()

    def mostrar_ventana_buscar(self):
        '''
        Método para desplegar la ventana de búsquedas
        '''
        self.ventana_buscar.show()

    def guardar_album(self, n_album, nuevo_album):
        '''
        Método para guardar un album
        '''
        guardar_album = self.logica.editar_album(n_album, nuevo_album["titulo"], nuevo_album["ano"],
                                                 nuevo_album["descripcion"],
                                                 nuevo_album["medio"])
        if guardar_album is False:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar los cambios")
            mensaje_error.setText("Ya existe un album con el título " + nuevo_album["titulo"])
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()


    def guardar_cancion(self, nueva_cancion, interpretes):
        '''
        Método para editar una canción
        '''
        res = self.logica.editar_cancion(nueva_cancion["id"], nueva_cancion["titulo"], nueva_cancion["minutos"],
                                         nueva_cancion["segundos"], nueva_cancion["compositor"], interpretes)

    def eliminar_album(self, id_album):
        '''
        Método para eliminar un album
        '''
        dialogo_confirmacion = QMessageBox()
        dialogo_confirmacion.setIcon(QMessageBox.Question)
        dialogo_confirmacion.setText("¿Está seguro que desea borrar el álbum?")
        dialogo_confirmacion.setWindowTitle("Confirmación")
        dialogo_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if dialogo_confirmacion.exec_() == QMessageBox.Yes:
            self.logica.eliminar_album(id_album)
        self.ventana_lista_album.mostrar_albums(self.logica.dar_albumes())


    def eliminar_cancion(self, id_cancion):
        '''
        Método para eliminar una canción
        '''
        dialogo_confirmacion = QMessageBox()
        dialogo_confirmacion.setIcon(QMessageBox.Question)
        dialogo_confirmacion.setText("¿Está seguro que desea borrar la canción?")
        dialogo_confirmacion.setWindowTitle("Confirmación")
        dialogo_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if dialogo_confirmacion.exec_() == QMessageBox.Yes:
            self.ventana_cancion.hide()
            self.logica.eliminar_cancion(id_cancion)
        self.ventana_lista_canciones.mostrar_canciones(self.logica.dar_canciones())

    def eliminar_interprete(self, id_interprete):
        '''
        Método para eliminar un intérprete
        '''
        self.logica.eliminar_interprete(id_interprete)

    def crear_album(self, nuevo_album):
        '''
        Método para crear un album
        '''
        crear_album = self.logica.agregar_album(nuevo_album["titulo"], nuevo_album["ano"], nuevo_album["descripcion"],
                                                nuevo_album["medio"])
        if crear_album is False:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar álbum")
            mensaje_error.setText("Ya existe un album con el título " + nuevo_album["titulo"])
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        self.ventana_lista_album.mostrar_albums(self.logica.dar_albumes())

    def crear_cancion(self, nueva_cancion, interpretes, id_album=-1):
        '''
        Método para crear una nueva canción. 
        El parámetro id_album indica si la canción está o no asociada a un album
        '''
        if nueva_cancion["titulo"] == "" or nueva_cancion["minutos"] == "" or nueva_cancion["segundos"] == "":
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar canción")
            mensaje_error.setText("Ningún campo debe estar vacio")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        else:
            if int(nueva_cancion["minutos"]) == 0 and int(nueva_cancion["segundos"]) < 10:
                mensaje_error = QMessageBox()
                mensaje_error.setIcon(QMessageBox.Critical)
                mensaje_error.setWindowTitle("Error al guardar canción")
                mensaje_error.setText("La duración de la canción debe ser mínimo de 10 sg")
                mensaje_error.setStandardButtons(QMessageBox.Ok)
                mensaje_error.exec_()
            else:
                if id_album == -1:
                    self.logica.agregar_cancion(nueva_cancion["titulo"], nueva_cancion["minutos"], nueva_cancion["segundos"],
                                                nueva_cancion["compositor"], id_album, interpretes)
                else:
                    operacion = self.logica.agregar_cancion(nueva_cancion["titulo"], nueva_cancion["minutos"], nueva_cancion["segundos"],
                                                            nueva_cancion["compositor"], id_album, interpretes)
                    if operacion is False:
                        mensaje_error = QMessageBox()
                        mensaje_error.setIcon(QMessageBox.Critical)
                        mensaje_error.setWindowTitle("Error al guardar canción")
                        mensaje_error.setText("Ya existe una canción con el título " + nueva_cancion["titulo"] + " en el álbum")
                        mensaje_error.setStandardButtons(QMessageBox.Ok)
                        mensaje_error.exec_()

    def mostrar_resultados_albumes(self, nombre_album):
        '''
        Método para mostrar los resultados de búsqueda de albumes por nombre
        '''
        albumes = self.logica.buscar_albumes_por_titulo(nombre_album)
        if len(albumes) == 0:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al buscar álbum")
            mensaje_error.setText("No hay álbumes con el título " + nombre_album)
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        self.ventana_buscar.mostrar_resultados_albumes(albumes)

    def mostrar_resultados_canciones(self, nombre_cancion):
        '''
        Método para mostrar los resultados de búsqueda de canciones por nombre
        '''
        canciones = self.logica.buscar_canciones_por_titulo(nombre_cancion)
        if len(canciones) == 0:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al buscar álbum")
            mensaje_error.setText("No hay canciones con el título " + nombre_cancion)
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        self.ventana_buscar.mostrar_resultados_canciones(canciones)

    def mostrar_resultados_interpretes(self, nombre_interprete):
        '''
        Método para mostrar los resultados de búsqueda de intérpretes por nombre
        '''
        interpretes = self.logica.buscar_interpretes_por_nombre(nombre_interprete)
        if len(interpretes) == 0:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al buscar álbum")
            mensaje_error.setText("No hay canciones con el interprete " + nombre_interprete)
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        self.ventana_buscar.mostrar_resultados_interpretes(interpretes)

    def agregar_interprete(self, id_cancion, nombre, texto_curiosidades):
        '''
        Método para agregar un nuevo intérprete en una canción
        '''
        self.logica.agregar_interprete(nombre, texto_curiosidades, id_cancion)
        self.ventana_cancion.mostrar_cancion(self.logica.dar_cancion_por_id(id_cancion))

    def asociar_cancion(self, id_album, id_cancion):
        '''
        Método para asociar una canción a un album
        '''
        self.logica.asociar_cancion(id_cancion, id_album)
        self.ventana_album.mostrar_album(self.logica.dar_album_por_id(id_album))
        self.ventana_album.mostrar_canciones(self.logica.dar_canciones_de_album(id_album))

    def dar_canciones(self):
        '''
        Método para dar todas las canciones
        '''
        return self.logica.dar_canciones()

    def dar_medios(self):
        '''
        Método para obtener los valores de la enumeración medios del mundo
        '''
        return self.logica.dar_medios()

    def dar_interpretes(self):
        '''
        Método para dar todos los intérpretes
        '''
        return self.logica.dar_interpretes()
