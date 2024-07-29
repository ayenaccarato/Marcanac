import sqlite3

import bcrypt

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
        nombre TEXT,
        usuario TEXT UNIQUE,
        clave TEXT,
        rol TEXT,)"""
        cur = self.con.cursor()
        cur.execute(sql_create_table1)
        cur.close()

    def crearAdmin(self):
        try:
            hashed_password = bcrypt.hashpw("12345".encode('utf-8'), bcrypt.gensalt())
            sql_insert = """INSERT INTO usuarios (nombre, usuario, clave, rol) VALUES (?, ?, ?, ?);"""
            cur = self.con.cursor()
            cur.execute(sql_insert, ("Administrador", "admin", hashed_password.decode('utf-8'), "admin"))
            cur.close()
            print("Usuario 'admin' creado correctamente.")        
        except Exception as ex:
            print(ex)

    def conectar(self):
        return self.con

            