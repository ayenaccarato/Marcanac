import datetime


class Paciente():

    def __init__(self, nombre:str, apellido:str, tipo:str, documento:str, fechaNacimiento:str, sexo:str):
        self._nombre = nombre
        self._apellido = apellido
        self._tipo = tipo
        self._documento = documento
        self._fechaNacimiento = fechaNacimiento
        self._sexo = sexo
        