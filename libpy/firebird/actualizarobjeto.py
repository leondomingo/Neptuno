# -*- coding: utf-8 -*-
"""
Created on 03/09/2009

función que recibe un feed con los cambios que hay que hacer en una tabla de olympo, 
guardados como atributos extendidos:

  - COD_CLASE: El código de la clase
  - COD_OBJETO: El COD_objeto que hay que actualizar
  - COD_Usuario: USuario del cambio
  
  después, los atributos extendidos contienen los cambios... en COD_ATRIBUTO el 
  COD_OBJETO del atributo que hay que cambiar y en 'valor' el nuevo valor

@author: Domingo García (ender)
"""

from sqlalchemy import MetaData, Table
from sqlalchemy.sql.expression import and_, func
from datetime import datetime
from libpy.firebird.util import nombre_tabla
from libpy.firebird.unidadescompartidasNeptuno import AtributosOlympo
from libpy.firebird.const_olympo import cl_Usuarios
from libpy.firebird.const_datos_olympo import TATR_OBJETO

def actualizar_objeto(cod_clase, cod_objeto, cod_usuario, atributos, conector):
    """Actualiza el objeto 'cod_objeto' de la clase 'cod_clase' por parte del usuario 'cod_usuario'.
    Si 'cod_objeto' es None, se crea el objeto correspondiente.
    'atributos' es un diccionario de la forma:
        {
            <atributo1>: <valor1>,
            <atributo2>: <valor2>,
            ...
            <atributoN>: <valorN>
        }
         
        Por ejemplo:
        {
            'ATR_4': 'Hola',
            'ATR_100': 12.50
        }
        
    Salida:
        True -> En caso de actualización correcta, o False en caso contrario
    """
    
    # comprobar usuario
    #conector.comprobar_usuario(cod_usuario)
    
    # mapear la tabla correspondiente
    meta = MetaData(bind=conector.engine)        
    tabla = Table(nombre_tabla(cod_clase), meta, autoload=True)
    
    # usuario
    atr_usuario = \
        conector.conexion.query(AtributosOlympo).\
        filter(and_(AtributosOlympo.id_clas_clasedeatributoenlazado == cl_Usuarios,
                    AtributosOlympo.id_clases_clase == cod_clase,
                    AtributosOlympo.id_tda_tipodeatributo == TATR_OBJETO,
                    func.upper(AtributosOlympo.nombre) == 'USUARIO')).\
        first()

    atributos['atr_%d' % atr_usuario.id] = cod_usuario
    
    # fecha de actualización
    atr_fechaactualizacion = \
        conector.conexion.query(AtributosOlympo).\
        filter(and_(AtributosOlympo.id_clases_clase == cod_clase,
                    func.upper(AtributosOlympo.nombre).like('FECHA DE ACTUALIZAC%'))).\
        first()
    
    atributos['atr_%d' % atr_fechaactualizacion.id] = datetime.now()                
                    
    # crear objeto
    if cod_objeto is None:
        # cod_objeto
        atributos['cod_objeto'] = conector.getcod_objeto(cod_clase)
        
        # fecha de creación
        atr_fechacreacion = \
            conector.conexion.query(AtributosOlympo).\
            filter(and_(AtributosOlympo.id_clases_clase == cod_clase,
                        func.upper(AtributosOlympo.nombre).like('FECHA DE CREAC%'))).\
            first()
                        
        atributos['atr_%d' % atr_fechacreacion.id] = datetime.now()
        
        qry = tabla.insert(values=atributos)
        
    else:
        # actualizar
        qry = tabla.update(tabla.c.cod_objeto == cod_objeto, 
                           values=atributos)
        
    # ejecutar query
    conector.conexion.execute(qry)
    conector.conexion.flush()
    
    return True        