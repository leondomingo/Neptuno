# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe COD_CLASE, COD_USUARIO y COD_OBJETO y devuelve un atributo extendido TITULO 
con el resultado de la función Olympo "TituloObjeto", es decir, los atributos 
que estén en el orden corto de la clase para ese usuario, separados por comas.

@author: Domingo García (ender)
"""

from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.expression import and_
from libpy.firebird.util import nombre_tabla
from libpy.firebird.const_olympo import cl_Atributos, cl_PrivilegiosDeAtributo,\
    pda_atributo, pda_usuariodelatributo, pda_ordencorto, atri_tipodeatributo,\
    atri_clase, atri_tipodevalor, atri_clasedeatributoenlazado
from libpy.firebird.const_datos_olympo import TATR_VALOR, TATR_COLECCION,\
    TVAL_FECHA, TVAL_HORA, TVAL_FECHAYHORA, TVAL_REAL, TATR_OBJETO

def titulo_objeto(cod_clase, cod_objeto, cod_usuario, conector):
    """
    Devuelve el 'orden corto' para el objeto 'cod_objeto' de la clase
    'cod_clase' para el usuario 'cod_usuario'.
    
    IN
      cod_clase    <int>
      cod_objeto   <int>
      cod_usuario  <int>
      conector     <Conexion>
      
    OUT
      <str>    
    """

    meta = MetaData(bind=conector.engine)
    tbl_temporal = Table(nombre_tabla(cod_clase), meta, autoload=True)
    objeto = conector.conexion.\
                    execute(tbl_temporal.\
                            select(tbl_temporal.c.cod_objeto == cod_objeto)).fetchone()
                 
    # no existe el objeto solicitado           
    if objeto is None:
        return ''                
    
    tbl_atri = Table(nombre_tabla(cl_Atributos), meta, autoload=True)
    tbl_pda = Table(nombre_tabla(cl_PrivilegiosDeAtributo), meta, autoload=True)
    
    qry = \
        tbl_atri.\
        join(tbl_pda,
             and_(tbl_atri.c.cod_objeto == tbl_pda.c[pda_atributo],
                  tbl_pda.c[pda_usuariodelatributo] == cod_usuario,
                  tbl_pda.c[pda_ordencorto] != -1,
                  tbl_atri.c[atri_tipodeatributo] != TATR_COLECCION)).\
        select(tbl_atri.c[atri_clase] == cod_clase,
               use_labels=True)
        
    resultado = []                    
    for atributo in conector.conexion.\
            execute(qry.order_by(tbl_pda.c[pda_ordencorto])):
        
        atr = 'ATR_%d' % atributo[tbl_atri.c.cod_objeto]
        if atributo[tbl_atri.c[atri_tipodeatributo]] == TATR_VALOR:
            tipo_valor = atributo[tbl_atri.c[atri_tipodevalor]]
            valor = objeto[atr]
            
            if valor != None:
                # fecha
                if tipo_valor == TVAL_FECHA:
                    resultado.append(objeto[atr].strftime('%d/%m/%Y'))
                
                # hora
                elif tipo_valor == TVAL_HORA:
                    resultado.append(objeto[atr].strftime('%H:%M:%S'))
                
                # fecha/hora
                elif tipo_valor == TVAL_FECHAYHORA:
                    resultado.append(objeto[atr].strftime('%d/%m/%Y %H:%M:%S'))
                    
                # real
                elif tipo_valor == TVAL_REAL:
                    resultado.append(('%2.2f' % objeto[atr]).replace('.', ','))
                
                # resto de tipos de valor
                else:
                    valor = objeto[atr]
                    if isinstance(valor, unicode):
                        resultado.append(valor.encode('utf-8'))
                    else:
                        resultado.append(str(valor))
            else:
                resultado.append('')
                
        elif atributo[tbl_atri.c[atri_tipodeatributo]] == TATR_OBJETO:
            titulo = titulo_objeto(atributo[tbl_atri.c[atri_clasedeatributoenlazado]], 
                                   objeto[atr], cod_usuario)
            if len(titulo) > 0:
                resultado.append(titulo)
            
    return '.'.join(resultado)