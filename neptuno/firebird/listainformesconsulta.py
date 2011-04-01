# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe un COD_CONSULTA y devuelve una lista de los informes de esa consulta, 
en el atributo extendido "Nombre" de los atributos del feed.

@author: Domingo García (ender)
"""

from sqlalchemy.schema import MetaData, Table
import os
from libpy.firebird.util import nombre_tabla
from libpy.firebird.const_olympo import cl_Variables, cl_Consultas,\
    vari_rutaconsultas, cons_nombre
from libpy.firebird.exc.excepciones import ENoExisteConsulta
from libpy.firebird.const_datos_olympo import BOOL_FALSE

def lista_informes(cod_consulta, conector):
    """Devuelve una lista de informes para la consulta 'cod_consulta'.
    Si la consulta no existe se lanza la excepción 'ENoExisteConsulta'"""
    
    meta = MetaData(bind=conector.engine)
    tbl_variables = Table(nombre_tabla(cl_Variables), meta, autoload=True)
    tbl_consultas = Table(nombre_tabla(cl_Consultas), meta, autoload=True)
    
    # variable
    variable = conector.conexion.execute(tbl_variables.select()).fetchone()
    
    # ruta consultas
    ruta_consultas = variable[vari_rutaconsultas]
    
    # consulta
    consulta = conector.conexion.\
                        execute(tbl_consultas.\
                                select(tbl_consultas.c.cod_objeto == cod_consulta)).\
                        fetchone()
    if consulta is None:
        raise ENoExisteConsulta(cod_consulta)
    
    # nombre
    nombre_consulta = consulta[cons_nombre].replace(' ', '_')
    
    # es RAVE o Fast Report
    extension = '.FR'
    if consulta.atr_100268 == BOOL_FALSE:
        nombre_consulta += '_RAV'
        extension = '.RAV'
        
    ruta = os.path.join(ruta_consultas, 'CONS_%s' % nombre_consulta)
    
    return [os.path.splitext(n)[0].encode('utf-8')
            for n in os.listdir(ruta) \
            if os.path.splitext(n)[1].upper().startswith(extension)]
    