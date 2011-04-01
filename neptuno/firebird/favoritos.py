# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe en un feed atom:

- COD_Usuario
- Posicion
- ResultadosPorPagina 

Devuelve la lista de favoritos del COD_Usuario indicado, paginado según 
Posicion y ResultadosPorPagina, con el siguiente formato:

- Una entrada para cada favorito, con la estructura de la función "ContenidoObjeto" 
como atributos extendidos de cada entrada. 

@author: Domingo García (ender)
"""
from sqlalchemy.schema import MetaData, Table
from libpy.firebird.util import nombre_tabla
from libpy.firebird.const_olympo import cl_Favoritos, favo_usuario
from libpy.firebird.contenidoobjeto import contenido_objeto

def favoritos(cod_usuario, posicion, resultados_por_pagina, conector):
    """
    Devuelve la lista de favoritos del usuario 'cod_usuario'
    
    IN
      cod_usuario           <int> -> Identificador del usuario (Usuarios)
      posicion              <int> -> Posición actual entre todos los favoritos del usuario
      resultados_por_pagina <int> -> Nº de elementos que se devolverán
    
    OUT
      Una lista de objetos (según la estructura de "contenidoobjeto") que representan
      los favoritos del usuario.
    
    EXC
      ENoExisteUsuario
    """

    resultado = []
    
    # comprobar existencia de 'cod_usuario' en Usuarios
#    conector.comprobar_usuario(cod_usuario)
    
    # calcular la lista de favoritos del usuario
    meta = MetaData(bind=conector.engine)
    tbl_favoritos = Table(nombre_tabla(cl_Favoritos), meta, autoload=True)
    
    for fav in conector.conexion.\
            execute(tbl_favoritos.\
                    select(tbl_favoritos.c[favo_usuario] == cod_usuario).\
                    limit(resultados_por_pagina).\
                    offset(posicion)):
        
        resultado.append(contenido_objeto(cl_Favoritos, fav.cod_objeto, cod_usuario))        
    
    return resultado