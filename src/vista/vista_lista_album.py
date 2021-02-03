from PyQt5.QtWidgets import QScrollArea, QDialog, QComboBox, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, \
    QLabel, QLineEdit, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore


class Ventana_Lista_Album(QWidget):
    '''
    Clase con la lista de albums
    '''

    def __init__(self, interfaz):
        '''
        Constructor de la ventana
        '''
        super().__init__()
        self.interfaz = interfaz
        # Se establecen las características de la ventana
        self.title = 'Mi música - albums'
        self.left = 80
        self.top = 80
        self.width = 550
        self.height = 450
        # Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        '''
        Método para inicializar los elementos gráficos
        '''
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        logo = QLabel(self)
        pixmap = QPixmap("src/recursos/Banner.png")
        pixmap = pixmap.scaledToWidth(self.width)
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)

        # Creación de los distribuidores

        self.distr_lista_canciones = QVBoxLayout()
        self.setLayout(self.distr_lista_canciones)

        self.lista_albums = QScrollArea()
        self.lista_albums.setWidgetResizable(True)
        self.caja_albums = QWidget()
        self.caja_albums.setLayout(QGridLayout())
        self.lista_albums.setWidget(self.caja_albums)

        # Creación de los títulos

        self.titulos = ["Titulo del album", "Intérpretes", "Medio", "Acciones"]

        for i in range(len(self.titulos)):
            etiqueta_titulo = QLabel(self.titulos[i])
            etiqueta_titulo.setFont(QFont("Times", weight=QFont.Bold))
            etiqueta_titulo.setAlignment(QtCore.Qt.AlignCenter)
            self.caja_albums.layout().addWidget(etiqueta_titulo, 0, i, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        self.caja_botones = QGroupBox()
        layout_botones = QHBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        # Creación de los botones

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.mostrar_ventana_buscar)

        self.boton_nuevo = QPushButton("Nuevo")
        self.boton_nuevo.clicked.connect(self.mostrar_dialogo_nuevo_album)

        self.boton_canciones = QPushButton("Ver Canciones")
        self.boton_canciones.clicked.connect(self.mostrar_ventana_lista_canciones)

        # Se agregan los botones

        layout_botones.addWidget(self.boton_buscar)
        layout_botones.addWidget(self.boton_nuevo)
        layout_botones.addWidget(self.boton_canciones)

        # Se añaden los elementos organizadores al distribuidor
        self.distr_lista_canciones.addWidget(logo)
        self.distr_lista_canciones.addWidget(self.lista_albums)
        self.distr_lista_canciones.addWidget(self.caja_botones)

    def limpiar_albums(self):
        '''
        Método para limpiar los álbumes (salvo los títulos)
        '''
        while self.caja_albums.layout().count() > len(self.titulos):
            child = self.caja_albums.layout().takeAt(len(self.titulos))
            if child.widget():
                child.widget().deleteLater()

    def mostrar_albums(self, albumes):
        '''
        Método para mostrar todos los albums en el área de resultados
        '''
        self.limpiar_albums()

        fila = 1
        for album in albumes:
            # Se añaden las filas con los resultados
            texto_titulo = QLineEdit(album["titulo"])
            texto_titulo.setReadOnly(True)
            self.caja_albums.layout().addWidget(texto_titulo, fila, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            texto_interpretes = QLineEdit(";".join(album.get("interpretes", [])))
            texto_interpretes.setReadOnly(True)
            self.caja_albums.layout().addWidget(texto_interpretes, fila, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            texto_medio = QLineEdit(album["medio"].name)
            texto_medio.setReadOnly(True)
            self.caja_albums.layout().addWidget(texto_medio, fila, 2, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            widget_botones = QWidget()
            widget_botones.setLayout(QGridLayout())

            boton_ver = QPushButton("Ver")
            boton_ver.setFixedSize(50, 25)
            boton_ver.clicked.connect(lambda estado, x=album["id"]: self.ver_album(x))
            widget_botones.layout().addWidget(boton_ver, 0, 0)

            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedSize(50, 25)
            boton_borrar.clicked.connect(lambda estado, x=album["id"]: self.interfaz.eliminar_album(x))
            widget_botones.layout().addWidget(boton_borrar, 0, 1)

            widget_botones.layout().setContentsMargins(0, 0, 0, 0)

            self.caja_albums.layout().addWidget(widget_botones, fila, 3, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            fila += 1

        # Con esto se compacta la lista
        self.caja_albums.layout().setRowStretch(fila, 1)

    def ver_album(self, id_album):
        '''
        Método para ver a un álbum específico
        '''
        self.hide()
        self.interfaz.mostrar_ventana_album(id_album)

    def mostrar_ventana_buscar(self):
        '''
        Método para ir a la ventana de búsquedas
        '''
        self.hide()
        self.interfaz.mostrar_ventana_buscar()

    def mostrar_dialogo_nuevo_album(self, nuevo_album):
        '''
        Método para desplegar el diálogo para añadir un nuevo album
        '''
        self.dialogo_nuevo_album = QDialog(self)
        self.dialogo_nuevo_album.setFixedWidth(300)

        layout = QGridLayout()
        self.dialogo_nuevo_album.setLayout(layout)

        lab1 = QLabel("Título")
        txt1 = QLineEdit()
        layout.addWidget(lab1, 0, 0)
        layout.addWidget(txt1, 0, 1)

        lab2 = QLabel("Anio")
        txt2 = QLineEdit()
        layout.addWidget(lab2, 1, 0)
        layout.addWidget(txt2, 1, 1)

        lab3 = QLabel("Descripcion")
        txt3 = QLineEdit()
        layout.addWidget(lab3, 2, 0)
        layout.addWidget(txt3, 2, 1)

        lab4 = QLabel("Medio")
        combo4 = QComboBox()
        combo4.addItems(self.interfaz.dar_medios())
        layout.addWidget(lab4, 3, 0)
        layout.addWidget(combo4, 3, 1)

        butAceptar = QPushButton("Aceptar")
        butCancelar = QPushButton("Cancelar")

        layout.addWidget(butAceptar, 4, 0)
        layout.addWidget(butCancelar, 4, 1)

        butAceptar.clicked.connect(lambda: self.crear_album(
            {"titulo": txt1.text(), "interpretes": "", "medio": combo4.currentText(), "ano": txt2.text(),
             "descripcion": txt3.text()}))
        butCancelar.clicked.connect(lambda: self.dialogo_nuevo_album.close())

        self.dialogo_nuevo_album.setWindowTitle("Añadir nuevo album")
        self.dialogo_nuevo_album.exec_()

    def crear_album(self, nuevo_album):
        '''
        Método para crear un nuevo album
        '''

        # Si hay campos vacios, se lanza un mensaje de error.
        if nuevo_album['titulo'] == '' or nuevo_album['ano'] == '' or nuevo_album['descripcion'] == '':
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar álbum")
            mensaje_error.setText("Ningún campo debe estar vacio")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        else:
            self.interfaz.crear_album(nuevo_album)
            self.dialogo_nuevo_album.close()

    def mostrar_ventana_lista_canciones(self):
        '''
        Método para ir a la lista de canciones
        '''
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()
