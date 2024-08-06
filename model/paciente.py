import datetime


class Paciente():

    def __init__(self, nombre:str, apellido:str, domicilio:str, localidad:str, 
                 documento:int, fechaNacimiento:str, obraSocial:str, numAfiliado:int, 
                 telefono:int, fechaIngreso:str, fechaEgreso:str, motivo:str,
                 familiar:str, parentesco:str, telFamiliar:str,  modulo:str, submodulo:str, equip:str, sopNutri:str, asisRespi:str):
        self._nombre = nombre
        self._apellido = apellido
        self._domicilio = domicilio
        self._localidad = localidad
        self._documento = documento
        self._fechaNacimiento = fechaNacimiento
        self._obraSocial = obraSocial
        self._numAfiliado = numAfiliado
        self._telefono = telefono
        self._fechaIngreso = fechaIngreso
        self._fechaEgreso = fechaEgreso
        self._motivo = motivo
        self._familiar = familiar
        self._parentesco = parentesco
        self._telFamiliar = telFamiliar
        self._modulo = modulo
        self._submodulo = submodulo
        self._equip = equip
        self._sopNutri = sopNutri
        self._asisRespi = asisRespi

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def apellido(self):
        return self._apellido
    
    @property
    def domicilio(self):
        return self._domicilio
    
    @property
    def fechaNacimiento(self):
        return self._fechaNacimiento
    
    @property
    def telefono(self):
        return self._telefono
        