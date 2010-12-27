# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe en atributos extendidos de un feed atom COD_Clase y COD_Objeto, y devuelve
todos los atributos del objeto de la base de datos identificado por el par de valores.

Los valores se devuelven en los atributos extendidos, con las siguientes propiedades:

nombre = nombre del atributo;
cod_atributo = COD_Objeto del atributo;
visible = 'true' en los atributos normales, 'false' en COD_Objeto, FechaCreacion, FechaActualizacion, Usuario
valor = valor en texto del atributo;
solo_lectura = 'false' o 'true' dependiendo de los privilegios del atributo
cod_clase_objeto = COD_Objeto de la clase del atributo enlazado
tipo = 'valor', 'objeto', 'coleccion'
longitud := tamaño de los strings


@author: Domingo García (ender)
"""

from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.expression import and_
from libpy.firebird.util import nombre_tabla
from libpy.firebird.exc.excepciones import ENoExisteRegistro
from libpy.firebird.const_datos_olympo import TVAL_ENTERO, TATR_COLECCION,\
    NIDEPR_NINGUNO, TATR_OBJETO, TVAL_CARACTER, NIDEPR_LECTURA
from libpy.firebird.unidadescompartidasNeptuno import AtributosOlympo
from libpy.firebird.gestorolympo import GestorOlympo

def contenido_objeto(cod_clase, cod_objeto, cod_usuario, atributos=None, conector=None):
    """Devuelve una lista de atributos de la clase 'cod_clase' para el objeto
    'cod_objeto' de la forma:
    [<atributo1>, <atributo2>, ..., <atributoN>]
    <atributo> = 
    {
        'nombre':
        'valor':
        'cod_atributo':
        'cod_clase':
        'tipo':
        'longitud'
        'visible':
        'solo_lectura'
    }
    
    El parámetro 'atributos' nos permite especificar la lista de atributos
    que se utilizarán para el resultado. Además, hay que tener en cuenta que
    los atributos que aparezcan dependerán de los privilegios que tenga el 
    usuario 'cod_usuario'.
    
    Se lanzará 'ENoExisteRegistro' en caso de que no exista el registro 'cod_objeto'
    en la clase 'cod_clase'.
    
    Se lanzará 'ENoExisteUsuario' en caso de que no exista el usuario 'cod_usuario'."""
    
#    if conector is None:
#        conector = conexion(configuracion=CONFIGURACION)

    # comprobar usuario
#    conector.comprobar_usuario(cod_usuario)

    go = GestorOlympo(conector)
    
    resultado = [] 
                 
    meta = MetaData(bind=conector.engine)
    tabla = Table(nombre_tabla(cod_clase), meta, autoload=True)       
    
    objeto = conector.conexion.\
                execute(tabla.select(tabla.c.cod_objeto == cod_objeto)).\
                fetchone()
        
    if objeto is None:
        raise ENoExisteRegistro(cod_objeto)

    # COD_OBJETO
    atributo = dict(nombre='COD_OBJETO',
                    valor=cod_objeto,
                    cod_atributo='COD_OBJETO',
                    cod_clase=cod_clase,
                    visible=False,
                    solo_lectura=False,
                    tipo=TVAL_ENTERO,
                    longitud=0)
        
    resultado.append(atributo)
    
    # atributos de la clase que no son "colección"
    for atributo in conector.conexion.query(AtributosOlympo).\
            filter(and_(AtributosOlympo.id_clases_clase == cod_clase, \
                        AtributosOlympo.id_tda_tipodeatributo != TATR_COLECCION)).\
            all():
        
        # obtener privilegio del usuario sobre este atributo
        # * Ninguno: No se muestra (no se añade el AtributoExtendido a la entrada)
        # * Lectura: solo_lectura=True
        # * Lectura/Escritura: solo_lectura=False
        atr = 'ATR_%d' % atributo.id
        if atributos == None or\
            atr.upper() in [a.upper() for a in atributos]:            
        
            priv = go.privilegio_atributo(cod_usuario, atr)
            if priv != NIDEPR_NINGUNO:                        
                
                clase = cod_clase
                longitud = 0
                value = objeto[atr]
                
                #atributo = AtributosOlympo()
                    
                # tipo = 'OBJETO'
                if atributo.id_tda_tipodeatributo == TATR_OBJETO:
                    clase = atributo.id_clas_clasedeatributoenlazado
                    
                else:
                    # tipo = 'VALOR'
                    # formatear valor
                    
                    # carácter
                    #if atributo.id_tiposdeatributo_tipodeatributo==TVAL_BLOB:
                    #    value=value.decode('iso-8859-1').encode('utf-8')
                    
                    if atributo.id_tdv_tipodevalor == TVAL_CARACTER:
                        longitud = atributo.tamano
                                            
                # visible
                visible = not atributo.nombre.upper().startswith('FECHA DE CREAC') and \
                    not atributo.nombre.upper().startswith('FECHA DE ACTUALIZ')                    
                    
                resultado.append(dict(nombre=atributo.nombre,
                                      valor=value,
                                      cod_atributo=atr,
                                      cod_clase=clase,
                                      tipo=atributo.id_tdv_tipodevalor,
                                      longitud=longitud,
                                      visible=visible,
                                      solo_lectura=priv == NIDEPR_LECTURA))
            
    return resultado
