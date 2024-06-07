import sqlite3

class Conexion():
    def __init__(self):
        try:
            self.con = sqlite3.connect("marcanac.bd")
            self.crearTablas()
        except Exception as ex:
            print(ex)

    def crearTablas(self):
        sql_create_table1 = """ CREATE TABLE IF NOT EXISTS usuarios
        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        rol TEXT, 
        usuario TEXT UNIQUE,
        clave TEXT)"""
        cur = self.con.cursor()
        cur.execute(sql_create_table1)
        cur.close()

    def conectar(self):
        return self.con

            