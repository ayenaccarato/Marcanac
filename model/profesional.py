import datetime


class Profesional():

    def __init__(self, nombre:str, apellido:str, domicilio:str, localidad:str, 
                 CUIT:int, fechaNacimiento:str, codPostal:int, matricula:str, 
                 telefono:int, cbu1:str, cbu2:str, alias:str, mail:str, monotributo:bool, 
                 coord:bool, profesional:str, codTransf:str):
        self._nombre = nombre
        self._apellido = apellido
        self._domicilio = domicilio
        self._localidad = localidad
        self._CUIT = CUIT
        self._fechaNacimiento = fechaNacimiento
        self._codPostal = codPostal
        self._matricula = matricula
        self._telefono = telefono
        self._cbu1 = cbu1
        self._cbu2 = cbu2
        self._alias = alias
        self._mail = mail
        self._monotributo = monotributo
        self._coord = coord
        self._profesional = profesional
        self._codTransf = codTransf
        