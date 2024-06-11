import conexion as con

class ListadoData():

    def buscarPorFecha(self, fechaDesde): #Cuando tenga los inicios y fin, se piden ambas
        self.db = con.Conexion().conectar()
        self.cursor = self.db.cursor()
        sql = """
            SELECT * FROM pacientes p
            WHERE p.fechaNacimiento = '{}'    
        """.format(fechaDesde)
        print(sql)
        res = self.cursor.execute(sql)
        data = res.fetchall() #Muestro todo lo que me devuelva
        return data