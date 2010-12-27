#-*- coding: utf-8 -*-

from neptuno import Neptuno
from libpy.conexion import Conexion

def save(tabla, id_usuario, datos=None, conector=None):
    """
    Guardar los datos de un registro de una tabla.
    
    IN
      id_usuario <int>
      tabla <str>
      datos {<campo1>: valor1, campo2: valor2, ...}
        
    OUT
      <int>
      id del registro que acabamos de guardar
        
    EXC
      NoExisteUsuario
      NoExisteTabla
    """
    
    if conector is None:
        conector = Conexion()

    la_tabla = Neptuno(conector, tabla, id_usuario)
    id_registro = la_tabla.update_registro(datos)

    if id_registro == -405:
        raise Exception
    else:
        return id_registro
    