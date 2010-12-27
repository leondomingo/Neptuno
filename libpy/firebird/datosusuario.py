# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe login y password en atributos extendidos de un feed atom, y devuelve:

a) Si existe el usuario web (de la clase usuarios web) con ese login y password el objeto (con la misma estructura que
   la función 'ContenidoObjeto')
b) Si no existe un atom vacío

@author: Domingo García (ender)
"""

from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.expression import and_, func
from libpy.firebird.util import nombre_tabla
from libpy.firebird.const_olympo import cl_UsuariosWeb, uswe_nombredeusuario,\
    uswe_contrasena
from libpy.firebird.exc.usuariosweb import ENoExisteUsuarioWeb
from libpy.firebird.contenidoobjeto import contenido_objeto

def datos_usuario(login, password, conector):
    """
    IN
      login <str> Login del usuario web (case insensitive)
      password <str> Password del usuario web (case sensitive)
    
    OUT
      Un objeto según la estructura de "contenidoobjeto"
    
    EXC
      ENoExisteUsuarioWeb
            
    """
    
    meta = MetaData(bind=conector.engine)
    tbl_uweb = Table(nombre_tabla(cl_UsuariosWeb), meta, autoload=True)
    
    # buscar usuario web
    usuario = \
        conector.conexion.\
        execute(tbl_uweb.\
                select(and_(func.upper(tbl_uweb.c[uswe_nombredeusuario]) == login.upper(),
                            tbl_uweb.c[uswe_contrasena] == password))).fetchone()
                            
    if usuario is None:
        raise ENoExisteUsuarioWeb(login)
    
    return contenido_objeto(cl_UsuariosWeb, usuario.cod_objeto, conector.id_usuario, None, conector)