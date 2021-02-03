from PyQt5.QtWidgets import QDialog, QScrollArea, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore, Qt

class Ventana_Inicial(QWidget):

    def __init__(self, interfaz):
        super().__init__()

        #Asignamos la interfaz
        self.interfaz = interfaz
        #Se establecen las características de la ventana
        self.title = 'Mi música - Búsqueda'
        self.left = 80
        self.top = 80
        self.width = 550
        self.height = 500
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    
    def inicializar_ventana(self):

        #inicializamos la ventana
        self.setWindowTitle(self.title)
        self.setFixedSize( self.width, self.height)
        
        
        self.distr_caja_busquedas = QGridLayout()
        self.setLayout(self.distr_caja_busquedas)

        #Creación del logo

        logo=QLabel(self)
        pixmap = QPixmap("src/recursos/Banner.png") 
        pixmap = pixmap.scaledToWidth(self.width)       
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)

        #Etiquetas principales de la caja de búsquedas

        self.etiqueta_album = QLabel('Título del album')
        self.txt_album = QLineEdit()

        self.boton_buscar_album = QPushButton("Buscar")
        self.boton_buscar_album.clicked.connect(self.buscar_album)

        self.boton_ver_albumes = QPushButton("Ver todos")
        self.boton_ver_albumes.clicked.connect(self.ver_albumes)

        self.etiqueta_cancion = QLabel('Título de la canción')
        self.txt_cancion = QLineEdit()

        #Botones de acción

        self.boton_buscar_cancion = QPushButton("Buscar")
        self.boton_buscar_cancion.clicked.connect(self.buscar_cancion)

        self.boton_ver_canciones = QPushButton("Ver todas")
        self.boton_ver_canciones.clicked.connect(self.ver_canciones)

        self.etiqueta_interprete = QLabel('Intérprete de la canción')
        self.txt_interprete = QLineEdit()

        self.boton_buscar_interprete = QPushButton("Buscar")
        self.boton_buscar_interprete.clicked.connect(self.buscar_interprete)

        #self.boton_ver_interpretes = QPushButton("Ver todos")
        #self.boton_ver_interpretes.clicked.connect(self.ver_interpretes)

        self.etiqueta_resultados = QLabel('Resultados')
        self.etiqueta_resultados.setFont(QFont("Times", weight=QFont.Bold))

        #Se añaden los elementos a los distribuidores
        
        self.distr_caja_busquedas.addWidget(logo, 0, 0, 1, 4)

        self.distr_caja_busquedas.addWidget(self.etiqueta_album, 1,0)
        self.distr_caja_busquedas.addWidget(self.txt_album, 1, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_album, 1, 2)
        self.distr_caja_busquedas.addWidget(self.boton_ver_albumes, 1, 3)

        self.distr_caja_busquedas.addWidget(self.etiqueta_cancion, 2,0)
        self.distr_caja_busquedas.addWidget(self.txt_cancion, 2, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_cancion, 2, 2)
        self.distr_caja_busquedas.addWidget(self.boton_ver_canciones, 2, 3)

        self.distr_caja_busquedas.addWidget(self.etiqueta_interprete, 3,0)
        self.distr_caja_busquedas.addWidget(self.txt_interprete, 3, 1)
        self.distr_caja_busquedas.addWidget(self.boton_buscar_interprete, 3, 2)

        self.distr_caja_busquedas.addWidget(self.etiqueta_resultados, 4, 0, 1, 4)
        self.distr_caja_busquedas.setAlignment(self.etiqueta_resultados, QtCore.Qt.AlignCenter)

        #Se crea un área con barra de desplazamiento para mostrar los resultados

        self.tabla_resultados = QScrollArea()
        self.tabla_resultados.setFixedHeight(200)
        self.tabla_resultados.setWidgetResizable(True)
        self.widget_tabla_resultados = QWidget()
        self.widget_tabla_resultados.setLayout(QGridLayout())
        self.tabla_resultados.setWidget(self.widget_tabla_resultados)
        self.distr_caja_busquedas.addWidget(self.tabla_resultados, 4, 0, 1, 4)


    def limpiar_resultados(self):
        '''
        Método para limpiar el área de resultados
        '''
        while self.widget_tabla_resultados.layout().count()>0:
            child = self.widget_tabla_resultados.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def mostrar_resultados_albumes(self, lista_albums):
        '''
        Método para mostrar la lista de álbumes
        '''
        self.limpiar_resultados()

        etiqueta_titulo = QLabel("Título")
        etiqueta_titulo.setFixedSize(200,30)
        etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_tabla_resultados.layout().addWidget(etiqueta_titulo, 0, 0, 1, 2)
        self.widget_tabla_resultados.layout().setAlignment(etiqueta_titulo, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)  

        fila = 1
        for album in lista_albums:
            etiqueta_nombre = QLabel(album["titulo"])
            etiqueta_nombre.setFixedSize(200,30)
            self.widget_tabla_resultados.layout().addWidget(etiqueta_nombre, fila, 0, 1, 2)  
            self.widget_tabla_resultados.layout().setAlignment(etiqueta_nombre, QtCore.Qt.AlignTop)
            boton_ver = QPushButton("Ver")
            boton_ver.clicked.connect(lambda estado, id=album["id"]: self.ver_album(id))
            boton_ver.setFixedSize(40,30)
            self.widget_tabla_resultados.layout().addWidget(boton_ver, fila, 1)   
            self.widget_tabla_resultados.layout().setAlignment(boton_ver, QtCore.Qt.AlignTop)
            fila+=1
        #Esto añade un componente que nos permite compactar los resultados
        self.widget_tabla_resultados.layout().setRowStretch(fila, 1)
    
    def mostrar_resultados_canciones(self, lista_canciones):
        '''
        Método para mostrar la lista de canciones
        '''
        self.limpiar_resultados()

        etiqueta_titulo = QLabel("Título")
        etiqueta_titulo.setFixedSize(200,30)
        etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_tabla_resultados.layout().addWidget(etiqueta_titulo, 0, 0, 1, 2)
        self.widget_tabla_resultados.layout().setAlignment(etiqueta_titulo, QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)  

        fila = 1
        for cancion in lista_canciones:
            etiqueta_nombre = QLabel(cancion["titulo"])
            etiqueta_nombre.setFixedSize(200,30)
            self.widget_tabla_resultados.layout().addWidget(etiqueta_nombre, fila, 0, 1, 2)  
            self.widget_tabla_resultados.layout().setAlignment(etiqueta_nombre, QtCore.Qt.AlignTop)
            boton_ver = QPushButton("Ver")
            boton_ver.clicked.connect(lambda estado, id=cancion["id"]: self.ver_cancion(id))
            boton_ver.setFixedSize(40,30)
            self.widget_tabla_resultados.layout().addWidget(boton_ver, fila, 1)   
            self.widget_tabla_resultados.layout().setAlignment(boton_ver, QtCore.Qt.AlignTop)
            fila+=1

        #Esto añade un componente que nos permite compactar los resultados
        self.widget_tabla_resultados.layout().setRowStretch(fila, 1)
    
    def mostrar_resultados_interpretes(self, lista_interpretes):
        '''
        Método para mostrar la lista de intérpretes
        '''
        self.limpiar_resultados()

        etiqueta_titulo = QLabel("Nombre")
        etiqueta_titulo.setFixedSize(200,30)
        etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
        etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)

        self.widget_tabla_resultados.layout().addWidget(etiqueta_titulo, 0, 0, 1, 2,  QtCore.Qt.AlignCenter)

        fila = 1
        
        for interprete in lista_interpretes:
            etiqueta_nombre = QLabel(interprete["nombre"])
            etiqueta_nombre.setFixedSize(200,30)
            self.widget_tabla_resultados.layout().addWidget(etiqueta_nombre, fila, 0, QtCore.Qt.AlignLeft)  

            boton_ver = QPushButton("Ver canción")
            boton_ver.clicked.connect(lambda estado, id=interprete["cancion"]: self.ver_cancion(id))
            boton_ver.setFixedSize(100,30)
            self.widget_tabla_resultados.layout().addWidget(boton_ver, fila, 1)   
            fila+=1

        #Esto añade un componente que nos permite compactar los resultados
        self.widget_tabla_resultados.layout().setRowStretch(fila, 1)


    def buscar_album(self):
        '''
        Método para buscar un album por nombre
        '''
        self.interfaz.mostrar_resultados_albumes(self.txt_album.text())

    def ver_album(self, indice_album):
        '''
        Método para ver un álbum
        '''
        self.hide()
        self.interfaz.mostrar_ventana_album(indice_album)


    def ver_albumes(self):
        '''
        Método para ir a todos los albumes
        '''
        self.hide()
        self.interfaz.mostrar_ventana_lista_albums()


    def buscar_cancion(self):
        '''
        Método para buscar una canción por nombre
        '''
        self.interfaz.mostrar_resultados_canciones(self.txt_cancion.text())

    def ver_cancion(self, indice_cancion):
        '''
        Método para ver una canción
        '''
        self.hide()
        self.interfaz.mostrar_ventana_cancion(id_cancion=indice_cancion)

    def ver_canciones(self):
        '''
        Método para ir a ver todas las canciones
        '''
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()
     
    def buscar_interprete(self):
        '''
        Método para buscar un intérprete por nombre
        '''
        self.interfaz.mostrar_resultados_interpretes(self.txt_interprete.text())


    def ver_interpretes(self):
        '''
        Método para ir a ver todos los interpretes
        '''
        self.hide()
        self.interfaz.mostrar_ventana_lista_interpretes()

 
