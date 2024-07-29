class Usuario():

    def __init__(self, usuario, nombre=None, clave=None, rol=None):
        self._nombre = nombre
        self._usuario = usuario
        self._clave = clave
        self._rol = rol

    @property
    def nombre(self):
        return self._nombre

    @property
    def usuario(self):
        return self._usuario

    @property
    def clave(self):
        return self._clave

    @property
    def rol(self):
        return self._rol
    
    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_rol(self, rol):
        self._rol = rol