class Nodo:
    def __init__(self, datos):
        self.datos = datos
        self.hijos = []
        self.padre = None

    def get_datos(self):
        return self.datos

    def get_hijos(self):
        return self.hijos

    def set_hijos(self, hijos):
        self.hijos = hijos

    def set_padre(self, padre):
        self.padre = padre

    def get_padre(self):
        return self.padre