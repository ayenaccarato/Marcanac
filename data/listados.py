import conexion as con

class ListadoData():

    def buscarPaciente(self, documento, apellido): 
        '''Busco pacientes por distintos datos, dependiendo que se ingresa
        puede ser documento o apellido'''
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql = """
            SELECT * FROM pacientes p
            WHERE p.documento = '{}' or p.apellido = '{}'  
        """.format(documento, apellido)
        print(sql)
        res = self.cursor.execute(sql)
        data = res.fetchall() #Muestro todo lo que me devuelva
        return data
    
    def buscarProfesional(self, cuit, apellido, profesion): 
        '''Busco profesionales por distintos datos, dependiendo que se ingresa
        puede ser cuit, apellido o profesión'''
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql = """
            SELECT * FROM profesionales p
            WHERE p.cuit = '{}' or p.apellido = '{}' or p.profesional = '{}'  
        """.format(cuit, apellido, profesion)
        print(sql)
        res = self.cursor.execute(sql)
        data = res.fetchall() #Muestro todo lo que me devuelva
        return data