# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe un COD_USUARIO, Posicion, ResultadosPorPagina y devuelve una lista de las vistas personalizadas que puede
ver el usuario, con la estructura de la función "Favoritos" (utiliza la función Olympo "RellenarConTabla") 

@author: Domingo García (ender)
"""

from sqlalchemy.sql.expression import or_, and_, select
from libpy.firebird.const_olympo import cl_VistasPersonalizadas, vipe_especial, \
    vipe_nombre, vipe_usuarios
from libpy.firebird.const_datos_olympo import BOOL_TRUE
from sqlalchemy.schema import MetaData, Table
from libpy.firebird.contenidoobjeto import contenido_objeto
from libpy.firebird.util import nombre_tabla, nombre_coleccion, cod_atributo

def vistas_personalizadas(cod_usuario, posicion, por_pagina, conector):
    """Devuelve una lista de las vistas personalizadas del usuario con la 
    estructura de 'contenido_objeto' para cada una de ellas
    
    IN
      cod_usuario  <int>
      posicion     <int>
      por_pagina   <int>
      conector     <Conexion>
      
    OUT
      ???
    """
    
    #conector.comprobar_usuario(cod_usuario)
    meta = MetaData(bind=conector.engine)
    tbl_vipe = Table(nombre_tabla(cl_VistasPersonalizadas), meta, autoload=True)
    col_vipe = Table(nombre_coleccion(cl_VistasPersonalizadas), meta, autoload=True)
    
    # vistas del usuario 'cod_usuario'
    qry_vistas = \
        tbl_vipe.\
        join(col_vipe,
             and_(col_vipe.c.cod_objeto == tbl_vipe.c.cod_objeto,
                  col_vipe.c.cod_atributo == cod_atributo(vipe_usuarios),
                  col_vipe.c.cod_objetoincluido == cod_usuario,
                  ))

    # ...tal que:
    # - <vistas personalizadas.especial> = 'Sí', o
    # - <vistas personalizadas.especial> = NULL
    sel = select([tbl_vipe],
                 from_obj=qry_vistas,
                 whereclause=or_(tbl_vipe.c[vipe_especial] == None,
                                 tbl_vipe.c[vipe_especial] == BOOL_TRUE))
    
    # ...ordenadas por <vistas personalizadas.nombre>
    vistas = []
    for vista in conector.conexion.\
            execute(sel.limit(por_pagina).\
                    offset(posicion).\
                    order_by(tbl_vipe.c[vipe_nombre])):
                    
        vistas.append(contenido_objeto(cl_VistasPersonalizadas,
                                       vista[tbl_vipe.c.cod_objeto], cod_usuario))
                    
    return vistas