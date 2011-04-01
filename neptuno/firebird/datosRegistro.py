# -*- encoding: utf-8 -*-

from sqlalchemy.exc import NoSuchTableError
from neptuno import Neptuno
from libpy.excepciones.eneptuno import NoTienePrivilegios
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.conexion import Conexion

def record_data(id_usuario, tabla, id_registro=None):
    """
    Devuelve los datos de un registro (o de todos) de una tabla en forma de lista de campos.
    
    IN
      id_usuario                  -> Identificador en la tabla 'usuarios'
      tabla                       -> Nombre de la tabla
      id_registro=None (opcional) -> Si no se indica nada aquí se devuelven todos
        
    OUT
      Un json de la forma:
        [{campo1}, {campo2}, ..., {campoI}]
            
      Cada "campoX", a su vez, tiene la forma:
      campo = 
      {
       'nombre': '...',
       'tipo': '...',
       'valor': '...',
       'etiqueta': '...'
      }
        
    EXC
      NoExisteUsuario
      NoTienePrivilegios
    """
    
    conector = Conexion()
    try:
        la_tabla = Neptuno(conector, tabla, id_usuario)
    except NoSuchTableError:
        la_tabla = Neptuno(conector, str(tabla).replace('vista_busqueda_', ''), id_usuario)
    except (NoExisteUsuario, NoTienePrivilegios):
        raise
    
    if id_registro != None:
        return la_tabla.query_registro(id_registro)
    else:
        return la_tabla.query_tabla()
    
