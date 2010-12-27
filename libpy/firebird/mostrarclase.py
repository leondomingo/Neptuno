# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe un feed con COD_CLASE, COD_USUARIO, Posicion, ResultadosPorPagina

y devuelve un feed con la estructura de la función 'favoritos' de los datos de 
la vista estándar de esa clase y ese usuario

@author: Domingo García (ender)
"""
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.expression import and_, select
from libpy.firebird.const_olympo import vipe_clasebase, cl_VistasPersonalizadas, \
    vipe_usuarios
from libpy.firebird.mostrarvista import mostrar_vista
from libpy.firebird.util import nombre_tabla, nombre_coleccion, cod_atributo

def mostrar_clase(cod_clase, cod_usuario, posicion, por_pagina, conector):
    """
    IN
      cod_clase    <int>
      cod_usuario  <int>
      posicion     <int>
      por_pagina   <int>
      conector     <Conexion>
      
    OUT
      ???
    """
    
    meta = MetaData(bind=conector.engine)
    col_vipe = Table(nombre_coleccion(cl_VistasPersonalizadas), meta, autoload=True)
    tbl_vipe = Table(nombre_tabla(cl_VistasPersonalizadas), meta, autoload=True)
    
    qry = \
        tbl_vipe.\
        join(col_vipe,
             and_(col_vipe.c.cod_objeto == tbl_vipe.c.cod_objeto,
                  col_vipe.c.cod_atributo == cod_atributo(vipe_usuarios),
                  col_vipe.c.cod_objetoincluido == cod_usuario,
                  ))

    sel = select([tbl_vipe],
                 from_obj=qry,
                 where=tbl_vipe.c[vipe_clasebase] == cod_clase)
    
    vista = conector.conexion.execute(sel).fetchone()
    
    return mostrar_vista(vista.cod_objeto, posicion, por_pagina)