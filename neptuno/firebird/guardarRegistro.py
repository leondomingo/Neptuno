#-*- coding: utf-8 -*-

from neptuno import Neptuno
from libpy.conexion import Conexion

def save(tabla, id_usuario, datos=None):
    """
    Guardar los datos de un registro de una tabla.
    
    IN
      id_usuario
      tabla
      datos
        
    OUT
      id del registro que acabamos de guardar
        
    EXC      
      NoExisteUsuario
      NoExisteTabla
    """
    
    conector = Conexion()

    la_tabla = Neptuno(conector, tabla, id_usuario)
    id_registro = la_tabla.update_registro(datos)

    if id_registro == -405:
        raise Exception
    else:
        return id_registro
    