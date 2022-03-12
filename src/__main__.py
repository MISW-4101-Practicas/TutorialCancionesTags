import sys

import vista.interfaz_coleccion as ic
from logica.coleccion import Coleccion
from modelo.declarative_base import session, Base, engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session.close()
    
    coleccion = Coleccion()
    print("Test Change")
    app = ic.App(sys.argv, coleccion)
    sys.exit(app.exec_())