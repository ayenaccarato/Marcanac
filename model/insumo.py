import datetime


class Insumo():

    def __init__(self, fechaEntrega:str, nombre:str, cantidad:int, paciente:int):
        self._fechaEntrega = fechaEntrega
        self._nombre = nombre
        self._cantidad = cantidad
        self._paciente = paciente #ID del apciente