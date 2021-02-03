from PyQt5.QtWidgets import QScrollArea, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, \
    QLineEdit, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore

class Ventana_Album(QWidget):
    '''
    Clase de la ventana en dónde se muestra un album
    '''

    def __init__(self, interfaz):
        '''
        Método constructor de la ventana
        '''
        super().__init__()
        self.interfaz = interfaz
        #Se establecen las características de la ventana
        self.title = 'Mi música - album'
        self.left = 80
        self.top = 80
        self.width = 550
        self.height = 650
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        '''
        Método de inicialización de componentes gráficos
        '''

        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        #Definición de los distribuidores y cajas de agrupamiento

        self.distr_album = QVBoxLayout()
        self.setLayout(self.distr_album)       

        self.caja_album = QGroupBox()
        self.caja_album.setLayout(QHBoxLayout())

        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)

        #Creación del logo

        logo=QLabel(self)
        pixmap = QPixmap("src/recursos/Banner.png") 
        pixmap = pixmap.scaledToWidth(self.width)       
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)
    
        #Creación de etiquetas

        etiqueta_titulo = QLabel("Título")
        etiqueta_titulo.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_titulo, 0, 0)

        etiqueta_ano = QLabel("Año")
        etiqueta_ano.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_ano, 1, 0)

        etiqueta_descripcion = QLabel("Descripción")
        etiqueta_descripcion.setFont(QFont("Times",weight=QFont.Bold))
        layout_datos.addWidget(etiqueta_descripcion, 2, 0)

        etiqueta_medio = QLabel("Medio")
        etiqueta_medio.setFont(QFont("Times",weight=QFont.Bold))      
        layout_datos.addWidget(etiqueta_medio, 3, 0)

        #Creación de campos de texto editable y la lista desplegable

        self.texto_album = QLineEdit()
        layout_datos.addWidget(self.texto_album, 0, 1)
        self.texto_anio = QLineEdit()
        layout_datos.addWidget(self.texto_anio, 1, 1)
        self.texto_descripcion = QLineEdit()
        layout_datos.addWidget(self.texto_descripcion, 2, 1)
        self.lista_medios = QComboBox()
        self.lista_medios.addItems(self.interfaz.dar_medios())
        layout_datos.addWidget(self.lista_medios, 3, 1)

        #Creación de los botones

        self.caja_botones = QGroupBox()
        layout_botones = QVBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        self.boton_guardar = QPushButton("Guardar datos editados")
        self.boton_guardar.clicked.connect(self.guardar_album)
        layout_botones.addWidget(self.boton_guardar)
        
        self.boton_adicionar_nueva_cancion = QPushButton("Agregar nueva canción")
        layout_botones.addWidget(self.boton_adicionar_nueva_cancion)
        self.boton_adicionar_nueva_cancion.clicked.connect(self.crear_cancion)

        self.boton_adicionar_cancion_existente = QPushButton("Agregar canción existente")
        self.boton_adicionar_cancion_existente.clicked.connect(self.mostrar_dialogo_agregar_cancion)
        layout_botones.addWidget(self.boton_adicionar_cancion_existente)

        self.caja_album.layout().addWidget(self.caja_datos)
        self.caja_album.layout().addWidget(self.caja_botones)

        self.boton_albums = QPushButton("Ver lista de albums")
        self.boton_albums.clicked.connect(self.mostrar_lista_albums)

        #Creación de la tabla de canciones del album

        self.etiqueta_canciones = QLabel("Canciones")
        self.etiqueta_canciones.setFont(QFont("Times",weight=QFont.Bold))
        self.etiqueta_canciones.setAlignment(QtCore.Qt.AlignCenter)

        self.lista_canciones = QScrollArea()
        self.lista_canciones.setWidgetResizable(True)
        self.caja_canciones = QWidget()
        self.caja_canciones.setLayout(QGridLayout())
        self.lista_canciones.setWidget(self.caja_canciones)

        #Títulos de la tabla

        self.titulos_cancion = ["Título de la canción", "Compositor", "Duración", "Acciones"]
        for i in range(len(self.titulos_cancion)):
            etiqueta = QLabel(self.titulos_cancion[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            self.caja_canciones.layout().addWidget(etiqueta,0,i, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        #Se agregan los elementos al distribuidor

        self.distr_album.addWidget(logo)
        self.distr_album.addWidget(self.caja_album)
        self.distr_album.addWidget(self.etiqueta_canciones)
        self.distr_album.addWidget(self.lista_canciones)
        self.distr_album.addWidget(self.boton_albums)

    def mostrar_album(self, album):
        '''
        Método para mostrar los datos del album
        '''
        self.album_actual = album
        self.texto_album.setText(album["titulo"])
        self.texto_anio.setText(str(album["ano"]))
        self.texto_descripcion.setText(album["descripcion"])
        self.lista_medios.setCurrentIndex(self.interfaz.dar_medios().index(album["medio"].name))

    def limpiar_canciones(self):
        '''
        Método para limpiar la lista de canciones (salvo por los títulos)
        '''
        while self.caja_canciones.layout().count()>len(self.titulos_cancion):
            child = self.caja_canciones.layout().takeAt(len(self.titulos_cancion))
            if child.widget():
                child.widget().deleteLater()

    def mostrar_canciones(self, canciones):
        '''
        Método para mostrar las canciones del album (popular el área de resultados)
        '''
        self.limpiar_canciones()
        self.botones = []
        fila = 1
        for cancion in canciones:
            texto_titulo = QLineEdit(cancion["titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_titulo,fila,0)

            texto_interpretes = QLineEdit(cancion["compositor"])
            texto_interpretes.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_interpretes,fila,1)
            
            texto_duracion = QLineEdit("{}:{}".format(cancion["minutos"],cancion["segundos"]))
            texto_duracion.setReadOnly(True)
            self.caja_canciones.layout().addWidget(texto_duracion,fila,2)
            
            boton_quitar = QPushButton("Ver")
            boton_quitar.clicked.connect(lambda estado, x=cancion: self.ver_cancion(x))
            self.caja_canciones.layout().addWidget(boton_quitar,fila,3)
            fila+=1

        self.caja_canciones.layout().setRowStretch(fila, 1)

    def ver_cancion(self, cancion):
        '''
        Método para mostrar la canción
        '''
        self.hide()
        self.interfaz.mostrar_ventana_cancion(id_album=self.album_actual["id"],  id_cancion=cancion["id"])

    def guardar_album(self):
        '''
        Método para guardar los datos del album
        '''
        album_modificado = {"titulo":self.texto_album.text(),"interpretes":self.texto_descripcion.text(), "medio":self.lista_medios.currentText(),"ano":self.texto_anio.text(),"descripcion":self.texto_descripcion.text()}
        # Si hay campos vacios, se lanza un mensaje de error.
        if album_modificado['titulo'] == '' or album_modificado['ano'] == '' or album_modificado['descripcion'] == '':
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar los cambios")
            mensaje_error.setText("Ningún campo debe estar vacio")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        else:
            self.interfaz.guardar_album(self.album_actual["id"], album_modificado)

    def eliminar_album(self):
        '''
        Método para eliminar el album
        '''
        self.interfaz.eliminar_album(self.album_actual)

    def mostrar_lista_albums(self):
        '''
        Método para volver a la lista de albums
        '''
        self.interfaz.mostrar_ventana_lista_albums()
        self.hide()

    def crear_cancion(self):
        '''
        Método para crear una canción
        '''
        self.hide()
        self.interfaz.mostrar_ventana_cancion(nueva=True, id_album=self.album_actual["id"])

    def mostrar_dialogo_agregar_cancion(self):
        '''
        Método para desplegar el diálogo para agregar una canción existente
        '''
        self.dialogo_agregar_cancion = QDialog(self)
        
        layout = QGridLayout()
        self.dialogo_agregar_cancion.setLayout(layout)

        lab1 = QLabel("Canciones")
        layout.addWidget(lab1,0,0)

        lista_canciones = QComboBox()
        for cancion in self.interfaz.dar_canciones():
            lista_canciones.addItem("{}".format(cancion["titulo"]), cancion["id"] )
        layout.addWidget(lista_canciones,1,0)

        butAceptar = QPushButton("Agregar")
        butCancelar = QPushButton("Cancelar")
        
        caja_botones = QWidget()
        caja_botones.setLayout(QGridLayout())

        caja_botones.layout().addWidget(butAceptar,0,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        caja_botones.layout().addWidget(butCancelar,0,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        
        layout.addWidget(caja_botones, 3, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter )

        butAceptar.clicked.connect(lambda: self.asociar_cancion_a_album( lista_canciones.currentData()))
        butCancelar.clicked.connect(lambda: self.dialogo_agregar_cancion.close())

        self.dialogo_agregar_cancion.setWindowTitle("Añadir nueva canción")
        self.dialogo_agregar_cancion.exec_()
        self.dialogo_agregar_cancion.close()
    
    def asociar_cancion_a_album(self, id_cancion):
        '''
        Método para asociar la canción existente al album
        '''
        self.interfaz.asociar_cancion(self.album_actual["id"], id_cancion)
        self.dialogo_agregar_cancion.close()
        

