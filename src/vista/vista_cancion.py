
from PyQt5.QtWidgets import QMessageBox, QScrollArea, QPlainTextEdit, QComboBox, QDialog, QWidget, QPushButton, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtCore

class Ventana_Cancion(QWidget):
    '''
    Ventana que permite ver una canción
    '''
    def __init__(self, interfaz):
        '''
        Método constructor de la ventana
        '''
        super().__init__()
        self.interfaz = interfaz
        #Se establecen las características de la ventana
        self.title = 'Mi música - canción'
        self.left = 80
        self.top = 80
        self.width = 550
        self.height = 570
        #Inicializamos la ventana principal
        self.inicializar_ventana()

    def inicializar_ventana(self):
        '''
        Inicialización de los componentes gráficos
        '''
        self.cancion_actual = None
        self.interpretes = []
        self.id_album = -1
        self.interpretes_a_eliminar = []

        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)

        self.distr_cancion = QVBoxLayout()
        self.setLayout(self.distr_cancion)
        
        self.caja_datos = QGroupBox()
        layout_datos = QGridLayout()
        self.caja_datos.setLayout(layout_datos)

        #Creación del logo

        logo=QLabel(self)
        pixmap = QPixmap("src/recursos/Banner.png") 
        pixmap = pixmap.scaledToWidth(self.width)       
        logo.setPixmap(pixmap)
        logo.setAlignment(QtCore.Qt.AlignCenter)

        #Creación de las etiquetas básicas

        datos = ["Canción", "Duración", "Compositor"]
        for i in range(len(datos)):
            etiqueta = QLabel(datos[i])
            etiqueta.setFont(QFont("Times",weight=QFont.Bold))
            etiqueta.setAlignment(QtCore.Qt.AlignCenter)
            layout_datos.addWidget(etiqueta,i,0)

        #Creación de los campos editables

        self.texto_cancion = QLineEdit()
        layout_datos.addWidget(self.texto_cancion, 0, 1, 1, 3)

        self.texto_minutos = QLineEdit(maxLength=2)
        layout_datos.addWidget(self.texto_minutos, 1, 1)

        layout_datos.addWidget(QLabel(":"),1,2)

        self.texto_segundos = QLineEdit(maxLength=2)
        layout_datos.addWidget(self.texto_segundos, 1, 3)

        self.texto_compositor = QLineEdit()
        layout_datos.addWidget(self.texto_compositor, 2, 1, 1, 3)

        self.caja_botones = QWidget()
        layout_botones = QVBoxLayout()
        self.caja_botones.setLayout(layout_botones)

        #Creación de los botones

        self.boton_guardar = QPushButton("Guardar datos editados")
        self.boton_guardar.clicked.connect(lambda: self.guardar_cancion())
        layout_botones.addWidget(self.boton_guardar)

        self.boton_adicionar = QPushButton("Adicionar intérprete")
        self.boton_adicionar.clicked.connect(lambda: self.mostrar_dialogo_crear_interprete())
        layout_botones.addWidget(self.boton_adicionar)

        self.boton_canciones = QPushButton("Ver lista de canciones")
        self.boton_canciones.clicked.connect(self.mostrar_lista_canciones)
        layout_botones.addWidget(self.boton_canciones)

        #Creación del area con barra de desplazamiento de los intérpetes

        self.lista_interpretes = QScrollArea()
        self.lista_interpretes.setFixedHeight(200)
        self.lista_interpretes.setWidgetResizable(True)
        self.caja_interpretes = QWidget()
        self.caja_interpretes.setLayout(QGridLayout())
        self.lista_interpretes.setWidget(self.caja_interpretes)

        layout_datos.addWidget(self.caja_botones, 0, 4, 3, 1)

        #Creación de las etiquetas del área de intérpretes

        etiqueta_interpretes = QLabel("Intérpretes")
        etiqueta_interpretes.setFont(QFont("Times",weight=QFont.Bold))
        etiqueta_interpretes.setAlignment(QtCore.Qt.AlignCenter)

        etiqueta_nombre_interprete = QLabel("Nombre")
        etiqueta_nombre_interprete.setFont(QFont("Times",weight=QFont.Bold))
        self.caja_interpretes.layout().addWidget(etiqueta_nombre_interprete, 0, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        etiqueta_acciones = QLabel("Acciones")
        etiqueta_acciones.setFont(QFont("Times",weight=QFont.Bold))
        self.caja_interpretes.layout().addWidget(etiqueta_acciones, 0, 1,  QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

        #Se añaden los componentes al distribuidor principal

        self.distr_cancion.addWidget(logo)
        self.distr_cancion.addWidget(self.caja_datos)
        self.distr_cancion.addWidget(etiqueta_interpretes,  QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.distr_cancion.addWidget(self.lista_interpretes)

    def mostrar_cancion(self, cancion=None, interpretes=None):
        '''
        Método para mostrar los datos de una canción
        '''
        self.cancion_actual = cancion 
        self.interpretes = interpretes if interpretes is not None else []
        self.texto_cancion.setText(cancion.get("titulo","") if cancion is not None else "")
        self.texto_minutos.setText(str(cancion.get("minutos","")) if cancion is not None else "")
        self.texto_segundos.setText(str(cancion.get("segundos","")) if cancion is not None else "")
        self.texto_compositor.setText(cancion.get("compositor","") if cancion is not None else "")        
        self.mostrar_interpretes(self.interpretes)

    def limpiar_interpretes(self):
        '''
        Método para quitar todos los intérpretes del área de resultados
        '''

        #Se elimina todo menos los títulos del área
        while self.caja_interpretes.layout().count() > 2:
            child = self.caja_interpretes.layout().takeAt(2)
            if child.widget():
                child.widget().deleteLater()

    def mostrar_interpretes(self, interpretes):
        '''
        Método para mostrar todos los intérpretes de la canción
        '''
        self.interpretes = interpretes
        fila = 1
        self.limpiar_interpretes()
        for i, interprete in enumerate(interpretes):
            campo_nombre = QLineEdit(interprete["nombre"])
            campo_nombre.setFixedWidth(300)
            campo_nombre.setReadOnly(True)

            widget_botones = QWidget()
            widget_botones.setLayout(QGridLayout())

            self.caja_interpretes.layout().addWidget(campo_nombre,fila,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            boton_ver = QPushButton("Ver")
            boton_ver.setFixedSize(50,25)
            boton_ver.clicked.connect(lambda estado, n_interprete=i: self.mostrar_dialogo_crear_interprete(n_interprete))
            widget_botones.layout().addWidget(boton_ver,fila,0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            boton_borrar = QPushButton("Borrar")
            boton_borrar.setFixedWidth(50)
            boton_borrar.setFixedSize(50,25)
            boton_borrar.clicked.connect(lambda estado, n_interprete=i: self.eliminar_interprete(n_interprete))
            widget_botones.layout().addWidget(boton_borrar,fila,1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)

            widget_botones.layout().setContentsMargins(0,0,0,0)
            
            self.caja_interpretes.layout().addWidget(widget_botones, fila, 1, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
            fila+=1
        #Esta función nos permite mostrar los resultados compactados hacia arriba
        self.caja_interpretes.layout().setRowStretch(fila+2, 1)

    def guardar_cancion(self):
        '''
        Función para guardar los cambios en una canción
        '''

        #Si no hay intérpretes, se lanza un mensaje de error.
        if len(self.interpretes) == 0:
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar canción")
            mensaje_error.setText("La canción debe tener al menos un intérprete")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        else:
            if self.cancion_actual == None:
                #Si no hay una canción actual definida, la canción es nueva y se debe crear en la lógica
                self.interfaz.crear_cancion({"titulo":self.texto_cancion.text(),"minutos":self.texto_minutos.text(), "segundos":self.texto_segundos.text(), "compositor":self.texto_compositor.text()}, self.interpretes, id_album=self.id_album)
            else:
                #Si ya hay una canción actual, se debe actualizar
                for id in self.interpretes_a_eliminar:
                    if id != "n":
                        self.interfaz.eliminar_interprete(id)
                self.interpretes_a_eliminar = []
                self.cancion_actual["titulo"]=self.texto_cancion.text()
                self.cancion_actual["minutos"]=self.texto_minutos.text()
                self.cancion_actual["segundos"]=self.texto_segundos.text()
                self.cancion_actual["compositor"]=self.texto_compositor.text()
                if self.cancion_actual["titulo"] == "" or self.cancion_actual["minutos"] == "" or self.cancion_actual["segundos"] == "":
                    mensaje_error = QMessageBox()
                    mensaje_error.setIcon(QMessageBox.Critical)
                    mensaje_error.setWindowTitle("Error al guardar canción")
                    mensaje_error.setText("Ningún campo debe estar vacio")
                    mensaje_error.setStandardButtons(QMessageBox.Ok)
                    mensaje_error.exec_()
                elif int(self.cancion_actual["minutos"]) == 0 and int(self.cancion_actual["segundos"]) < 10:
                    mensaje_error = QMessageBox()
                    mensaje_error.setIcon(QMessageBox.Critical)
                    mensaje_error.setWindowTitle("Error al guardar canción")
                    mensaje_error.setText("La duración de la canción debe ser mínimo de 10 sg")
                    mensaje_error.setStandardButtons(QMessageBox.Ok)
                    mensaje_error.exec_()
                else:
                    self.interfaz.guardar_cancion(self.cancion_actual, self.interpretes)

            if self.id_album != -1:
                #Si hay un album definido, se regresa a la vista del album, de lo contrario, se creo la canción sola.
                self.hide()
                self.interfaz.mostrar_ventana_album(self.id_album)
                self.id_album = -1

    def eliminar_interprete(self, n_interprete):
        '''
        Método para eliminar intérpretes de la ventana
        '''
        dialogo_confirmacion = QMessageBox()
        dialogo_confirmacion.setIcon(QMessageBox.Question)
        dialogo_confirmacion.setText("¿Está seguro que desea borrar el intérprete?")
        dialogo_confirmacion.setWindowTitle("Confirmación")
        dialogo_confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if dialogo_confirmacion.exec_() == QMessageBox.Yes:
            self.interpretes_a_eliminar.append(self.interpretes[n_interprete]["id"])
            self.interpretes.pop(n_interprete)
        self.mostrar_interpretes(self.interpretes)
        
    def mostrar_dialogo_crear_interprete(self, n_interprete=-1):
        '''
        Método para desplegar el diálogo de crear/editar intérprete
        '''
        self.dialogo_nuevo_interprete = QDialog(self)

        layout = QGridLayout()
        self.dialogo_nuevo_interprete.setLayout(layout)
        self.dialogo_nuevo_interprete.setFixedSize(400,300)

        lab1 = QLabel("Nombre:")
        txt1 = QLineEdit()
        
        layout.addWidget(lab1,0,0)
        layout.addWidget(txt1,0,1)
        
        lab2 = QLabel("Curiosidades:")
        txt2 = QPlainTextEdit()
        
        if n_interprete != -1:
            txt1.setText(self.interpretes[n_interprete].get("nombre",""))
            txt2.setPlainText(self.interpretes[n_interprete].get("texto_curiosidades",""))

        txt2.setFixedWidth(275)
        layout.addWidget(lab2, 1, 0, 1, 1, QtCore.Qt.AlignTop)
        layout.addWidget(txt2, 1, 1, 1, 4)

        widget_botones = QWidget()
        widget_botones.setFixedHeight(50)
        widget_botones.setLayout(QGridLayout())

        butAceptar = QPushButton("Aceptar")
        butCancelar = QPushButton("Cancelar")

        widget_botones.layout().addWidget(butAceptar,0,0)
        widget_botones.layout().addWidget(butCancelar,0,1)

        layout.addWidget(widget_botones, 4,0,1,2)

        if n_interprete == -1:
            self.dialogo_nuevo_interprete.setWindowTitle("Añadir nuevo interprete")
            butAceptar.clicked.connect(lambda: self.agregar_interprete(txt1.text(), txt2.toPlainText()))
        else:
            self.dialogo_nuevo_interprete.setWindowTitle("Modificar interprete")
            butAceptar.clicked.connect(lambda: self.modificar_interprete(n_interprete, txt1.text(), txt2.toPlainText()))
        butCancelar.clicked.connect(lambda: self.dialogo_nuevo_interprete.close())
        self.dialogo_nuevo_interprete.exec_()

    def modificar_interprete(self, n_interprete, nombre, texto_curiosidades):
        '''
        Método para modificar un intérprete en la ventana
        '''
        self.interpretes[n_interprete]["nombre"] = nombre
        self.interpretes[n_interprete]["texto_curiosidades"] = texto_curiosidades
        self.mostrar_interpretes(self.interpretes)
        self.dialogo_nuevo_interprete.hide()


    def agregar_interprete(self, nombre, texto_curiosidades):
        '''
        Método para agregar un intérprete en la ventana
        '''
        if nombre == "" or texto_curiosidades == "":
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error al guardar intérprete")
            mensaje_error.setText("Ningún campo debe estar vacio")
            mensaje_error.setStandardButtons(QMessageBox.Ok)
            mensaje_error.exec_()
        else:
            self.interpretes.append({"id":"n", "nombre":nombre, "texto_curiosidades":texto_curiosidades})
            self.mostrar_interpretes(self.interpretes)
        self.dialogo_nuevo_interprete.close()

    def mostrar_lista_canciones(self):
        '''
        Método para ir a la lista de canciones
        '''
        self.hide()
        self.interfaz.mostrar_ventana_lista_canciones()