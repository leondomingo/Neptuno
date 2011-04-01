#-*- coding: utf-8 -*-

from sqlalchemy.exc import NoSuchTableError
from neptuno import Neptuno
from libpy.conexion import Conexion

def delete(id_usuario, tabla, id_registro, conector=None):
    """
    Borrar un registro de una tabla.
    
    IN
      id_usuario   <int>
      tabla        <str>
      id_registro  <int>
    """

    if conector is None:
        conector = Conexion()
        
    try:
        la_tabla = Neptuno(conector, tabla, id_usuario)
        
    except NoSuchTableError:
        la_tabla = Neptuno(conector, str(tabla).replace('vista_busqueda_', ''), 
                           id_usuario)
    
    if la_tabla.delete_registro(id_registro):
        return '{}'
    else:
        raise Exception