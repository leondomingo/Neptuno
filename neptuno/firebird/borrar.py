#-*- coding: utf-8 -*-

from sqlalchemy.exc import NoSuchTableError
from neptuno import Neptuno
from libpy.conexion import Conexion

def delete(id_usuario, tabla, id_registro):
    """
    Borrar un registro de una tabla.
    
    Entrada:
        id_usuario
        tabla
        id_registro
    """

    conector = Conexion()

    try:
        la_tabla = Neptuno(conector, tabla, id_usuario)
    except NoSuchTableError:
        la_tabla = Neptuno(conector, str(tabla).replace('vista_busqueda_', ''), id_usuario)
    
    if la_tabla.delete_registro(id_registro):
        return '{}'
    else:
        raise Exception
        