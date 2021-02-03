
from PyQt5.QtWidgets import QScrollArea, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore

class Ventana_Lista_Canciones(QWidget):
    '''
    Clase de la ventana con la lista de las canciones
    '''

    def __init__(self, app):
        '''
        Constructor de la ventana
        '''
        super().__init__()
        self.interfaz = app
        #Se establecen las características de la ventana
        self.title = 'Mi música - canciones'
        self.left = 80
        self.top = 80
        self.width = 550
        self.height = 475
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        '''
        Método para inicializar los componentes gráficos
        '''
        
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_album = QVBoxLayout()
        self.setLayout(self.distr_album)

        #Area con barra de desplazamiento

        self.lista_canciones = QScrollArea()
        self.caja_canciones = QWidget()
        self.lista_canciones.setWidget(self.caja_canciones)
        self.lista_canciones.setFixedHeight(225)
        self.lista_canciones.setWidgetResizable(True)
        layout_canciones = QGridLayout()
        self.caja_canciones.setLayout(layout_canciones)

        #Creación del logo

        logo=QLabel(self)
        pixmap = QPixmap("src/recursos/Banner.png") 
        pixmap = pixmap.scaledToWidth(self.width)       
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)

        self.distr_album.addWidget(logo)

        #Creación de los títulos

        self.titulos = ["Título de la canción", "Compositor", "Duración", "Acciones"]
        for i in range(len(self.titulos)):
            etiqueta = QLabel(self.titulos[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            layout_canciones.addWidget(etiqueta,0,i,  QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        #Creación de los botones

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.mostrar_ventana_buscar)

        self.boton_nuevo = QPushButton("Nuevo")
        self.boton_nuevo.clicked.connect(self.agregar_nueva_cancion)

        self.boton_albumes = QPushButton("Ver Álbumes")
        self.boton_albumes.clicked.connect(self.mostrar_ventana_lista_albums)

        self.distr_album.addWidget(self.lista_canciones)

        self.widget_botones = QWidget()
        self.widget_botones.setLayout(QHBoxLayout())
        self.distr_album.addWidget(self.widget_botones)

        #Se añaden los botones al distribuidor

        self.widget_botones.layout().addWidget(self.boton_buscar)
        self.widget_botones.layout().addWidget(self.boton_nuevo)
        self.widget_botones.layout().addWidget(self.boton_albumes)

    def limpiar_canciones(self):
        '''
        Método para limpiar las canciones del área
        '''
        while self.caja_canciones.layout().count()>len(self.titulos):
            child = self.caja_canciones.layout().takeAt(len(self.titulos))
            if child.widget():
                child.widget().deleteLater()
            self.caja_canciones.layout().setRowStretch(0,0)


    def mostrar_canciones(self, canciones):
        '''
        Método para mostrar la información de las canciones
        '''
        self.limpiar_canciones()
        self.botones = []
        fila = 1
        for cancion in canciones:
            texto_titulo = QLineEdit(cancion["titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_titulo,fila,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            texto_interpretes = QLineEdit(cancion.get("compositor",cancion["compositor"]))
            texto_interpretes.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_interpretes,fila,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            
            texto_duracion = QLineEdit("{}:{}".format(cancion["minutos"],cancion["segundos"]))
            texto_duracion.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_duracion,fila,2, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            
            boton_ver = QPushButton("Ver")
            boton_ver.setFixedSize(50, 25)
            boton_ver.clicked.connect(lambda estado, x=cancion["id"]: self.ver_cancion(x))

            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedSize(50, 25)
            boton_borrar.clicked.connect(lambda estado, x=cancion["id"]: self.eliminar_cancion(x))

            widget_botones = QWidget()
            widget_botones.setLayout(QGridLayout())
            widget_botones.setFixedWidth(110)
        
            widget_botones.layout().addWidget(boton_ver,0,0)
            widget_botones.layout().addWidget(boton_borrar,0,1)
            widget_botones.layout().setContentsMargins(0,0,0,0)

            self.caja_canciones.layout().addWidget(widget_botones, fila,3, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            fila+=1
        #Esta instrucción permite compactar los resultados
        self.caja_canciones.layout().setRowStretch(fila+1, 1)

    
    def ver_cancion(self, id_cancion):
        '''
        Método para mostrar una canción en particular
        '''
        self.interfaz.mostrar_ventana_cancion(id_cancion=id_cancion)
        self.hide()

    def eliminar_cancion(self, id_cancion):
        '''
        Método para eliminar una canción
        '''
        self.interfaz.eliminar_cancion(id_cancion)

    def agregar_nueva_cancion(self):
        '''
        Método para crear una nueva canción
        '''
        self.hide()
        self.interfaz.mostrar_ventana_cancion(nueva=True)         

    def mostrar_ventana_lista_albums(self):
        '''
        Método para mostrar la ventana con la lista de albumes
        '''
        self.hide()
        self.interfaz.mostrar_ventana_lista_albums()   

    def mostrar_ventana_buscar(self):
        '''
        Método para mostrar la ventana de búsquedas
        '''
        self.hide()
        self.interfaz.mostrar_ventana_buscar()
