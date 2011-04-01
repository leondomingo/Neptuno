# -*- coding: utf-8 -*-

"""
Created on 03/09/2009

Recibe un feed con COD_VISTA, Posicion, ResultadosPorPagina
y devuelve un feed con la estructura de la función 'favoritos' de los datos de la vista personalizada "COD_VISTA"

@author: Domingo
"""

from sqlalchemy.schema import MetaData, Table
from sqlalchemy.databases.firebird import FBDate, FBString, FBInteger, FBFloat
from libpy.firebird.gestorolympo import GestorOlympo
from libpy.firebird.util import nombre_tabla, operador_insensitive
from libpy.firebird.const_olympo import cl_VistasPersonalizadas,\
    cl_CamposDeVistasPersonalizadas, cl_AtributosDeVista, cl_FiltrosPorDefecto,\
    cl_RelacionesDeVistasPersonalizadas, rdvp_vista, rdvp_atributo, rdvp_orden,\
    vipe_textosql, cdvp_nombre, cdvp_expresion, cdvp_vista,\
    adv_vistapersonalizada, adv_posicion, adv_nombredelacolumna,\
    adv_titulodelacolumna, adv_posicionparaordenacion, adv_ordenacion,\
    adv_visible, fpd_vista, fpd_valor, fpd_atributo, fpd_columna, vipe_clasebase,\
    fpd_enlace, fpd_operador
from libpy.firebird.const_datos_olympo import BOOL_TRUE, TVAL_FECHA, TVAL_BLOB,\
    TVAL_CARACTER, TVAL_ENTERO, TVAL_REAL, ENLACE_AND, ENLACE_OR, ORDECA_NINGUNA,\
    ORDECA_ASCENDENTE
from libpy.dataset import DataSet
from sqlalchemy.sql.expression import not_, desc
    
def sin_espacios(cadena):
    """Devuelve una cadena en minúsculas, sin espacios y cambiando las letras acentuadas por su correspondiente sin acentuar"""
    
    # 123456789012345678901234567890
    # RVICIOSREALIZADOS_FECHADECOBRO -> 30
    
    cadena = cadena.upper().replace(' ', '') #.replace('.VALOR', '')
    
    resultado = ''            
    for c in cadena:
        if c in [u'Á', u'É', u'Í', u'Ó', u'Ú', u'Ü', u'Ñ', '.', '(', ')'] or str(c).isalpha() or str(c).isdigit():
            if c == u'Á':
                c = 'A'
            elif c == u'É':
                c = 'E'
            elif c == u'Í': 
                c = 'I'
            elif c == u'Ó':
                c = u'O'
            elif c in [u'Ú', u'Ü']:
                c = 'U'
            elif c == u'Ñ':
                c = 'N'
            elif c in ['.', '(', ')']:
                c = '_'
        else:
            c = ''
            
        resultado += c
    
    return resultado

def mostrar_vista(cod_vista, posicion, por_pagina, conector):
    """
    IN
      cod_vista   <int>
      posicion    <int>
      por_pagina  <int>
      conector    <Conexion>
      
    OUT
      ???
    """

    meta = MetaData(bind=conector.engine)
    tbl_vistas = Table(nombre_tabla(cl_VistasPersonalizadas), meta, autoload=True)
    tbl_campos = Table(nombre_tabla(cl_CamposDeVistasPersonalizadas), meta, 
                       autoload=True)
    tbl_atrvistas = Table(nombre_tabla(cl_AtributosDeVista), meta, autoload=True)
    tbl_filtros = Table(nombre_tabla(cl_FiltrosPorDefecto), meta, autoload=True)
    tbl_relaciones = Table(nombre_tabla(cl_RelacionesDeVistasPersonalizadas), 
                           meta, autoload=True)
    
    go = GestorOlympo(conector)

    relaciones = [(r[rdvp_orden],
                   r[rdvp_atributo],
                   go.cod_clase_enlazada('ATR_%d' % r[rdvp_atributo]),) \
                   for r in conector.conexion.\
                        execute(tbl_relaciones.\
                                select(tbl_relaciones.c[rdvp_vista] == cod_vista))]
    
    # obtener la vista 'cod_vista'
    vista = \
        conector.conexion.\
        execute(tbl_vistas.\
                select(tbl_vistas.c.cod_objeto == cod_vista)).\
        fetchone()
    
    if vista is None:
        raise Exception('No existe la vista %d' % cod_vista)
                   
    # TextoSQL                   
    textoSQL = vista[vipe_textosql]
    if textoSQL is None:
        raise Exception('La vista no está definida')
    
    print textoSQL

    # campos de vista
    campos_vista = \
        [(campo.cod_objeto,
          sin_espacios(campo[cdvp_nombre])[-30:],
          campo[cdvp_expresion]) \
          for campo in conector.conexion.\
                execute(tbl_campos.\
                        select(tbl_campos.c[cdvp_vista] == cod_vista))]
    
    campos_vista.append((-1, u'COD_OBJETO', 'ORIGEN.COD_OBJETO',))
        
    # atributos de vista (ordenados por "atributos de vista.posición")
    atributos_vista = [] 
    for atributo in conector.conexion.\
            execute(tbl_atrvistas.select(tbl_atrvistas.c[adv_vistapersonalizada] == cod_vista).\
                    order_by(tbl_atrvistas.c[adv_posicion])):
        
        #print campos_vista
        expresion = ''
        for c in campos_vista:
            #print c[1]
            if c[1] == atributo[adv_nombredelacolumna].upper():
                expresion = c[2].strip()
                
        if not expresion:
            print campos_vista
            print atributo
            exit(1)
        
        t = (atributo[adv_nombredelacolumna],
             atributo[adv_titulodelacolumna],
             expresion,
             atributo.cod_objeto,
             atributo[adv_posicionparaordenacion],
             atributo[adv_ordenacion],
             atributo[adv_visible] == BOOL_TRUE,)
        
        atributos_vista.append(t)
    
    # filtros
    filtros = []
    for f in conector.conexion.\
            execute(tbl_filtros.\
                    select(tbl_filtros.c[fpd_vista] == cod_vista)):
        
        expresion_campo = ''
        tipo_dato = FBString
        valor = f[fpd_valor] or ''
        if f[fpd_atributo] != None:
            atributo = 'ATR_%d' % f[fpd_atributo]
            orden = \
                [r[0] for r in relaciones 
                 if r[2] == go.clase_atributo(atributo).id][0]
            
            expresion_campo = 'RELACION_%d.%s' % (orden, atributo)
            
            # tipos de dato
            tipo_dato = conector.tipo_de_valor(atributo)
            if tipo_dato == TVAL_FECHA:
                tipo_dato = FBDate
            elif tipo_dato == TVAL_BLOB:
                tipo_dato = FBString
            elif tipo_dato == TVAL_CARACTER:
                tipo_dato = FBString
            elif tipo_dato == TVAL_ENTERO:
                tipo_dato = FBInteger
            elif tipo_dato == TVAL_REAL:
                tipo_dato = FBFloat
            else:
                tipo_dato = FBString
                
        else:                
            # columna
            
            # buscar el campo que corresponde al atributo de vista
            expresion_campo = \
                [a[2] for a in atributos_vista if a[3] == f[fpd_columna]][0]
                               
            # averiguar el tipo de dato del campo
            tabla_campo = expresion_campo.split('.')
            if tabla_campo[0].upper() == 'ORIGEN':
                tabla = Table(nombre_tabla(vista[vipe_clasebase]), meta, autoload=True)
            else:
                orden = int(tabla_campo[0].replace('RELACION_', ''))
                cod_atributo = \
                    [r[1] for r in relaciones if r[0] == orden][0]
                
                atributo_relacion = 'ATR_%d' % cod_atributo
                tabla = Table(nombre_tabla(go.clase_enlazada(atributo_relacion).id), 
                              meta, autoload=True)
            
            tipo_dato = tabla.columns[tabla_campo[1].lower()].type
                            
        # calcular texto del filtro                
        filtro = (f[fpd_enlace],
                  operador_insensitive(expresion_campo, f[fpd_operador],
                                       valor, tipo_dato),)
        
        filtros.append(filtro)
        
    texto_filtros = ''
    primero = True    
    for filtro in filtros:
        if primero:
            texto_filtros = filtro[1]
            primero = False
        else:
            if filtro[0] == ENLACE_AND:
                texto_filtros += '\nAND '
            elif filtro[0] ==  ENLACE_OR:
                texto_filtros += '\nOR '
            else:
                texto_filtros += '\nAND '
                
            texto_filtros += filtro[1]
           
    # si hay filtros 
    if len(filtros) > 0:            
        if textoSQL.upper().count('WHERE') == 0:
            textoSQL = textoSQL.replace('/*FIN_TABLAS*/', 
                                        '/*FIN_TABLAS*/ WHERE %s' % texto_filtros)
        else:
            textoSQL = textoSQL.replace('WHERE', 
                                        'WHERE %s AND ' % texto_filtros)

    def ordenar(x, y):
        if x[4] > y[4]:
            return -1
        elif x[4] == y[4]:
            return 0
        else:
            return 1

    # ordenación
    texto_ordenacion = []
    for a in sorted(atributos_vista, ordenar):
        if a[4] != None and a[5] != ORDECA_NINGUNA:
            sentido = ' DESC'
            if a[5] == ORDECA_ASCENDENTE:
                sentido = ' ASC'
                
            texto_ordenacion.append('%(atr)s %(sen)s' % \
                                    dict(atr=a[2], sen=sentido))

    if texto_ordenacion:
        texto_ordenacion = ', '.join(texto_ordenacion)
        textoSQL += ' ORDER BY %s' % texto_ordenacion
        
    # posición / resultados por página            
    texto_first = ''
    if por_pagina != None:
        texto_first = ' FIRST %d ' % por_pagina
        
    texto_posicion = ''
    if posicion != None:
        texto_posicion = ' SKIP %d ' % posicion
                                    
    textoSQL = textoSQL.replace('SELECT', 
                                'SELECT %s' % (texto_first + texto_posicion))
    
    atributos_vista_visible = [av[0] for av in atributos_vista if av[6]]
    
    print textoSQL
        
    resultado = DataSet(columnas=['id'] + atributos_vista_visible)
    for registro in conector.conexion.execute(textoSQL):
        fila = [registro.cod_objeto]
        for av in atributos_vista_visible:
            fila.append(registro[av])
            
        resultado.append(fila)
        
    return resultado

if __name__ == '__main__':
    
    from sqlalchemy import and_
    from libpy.conexion import Conexion
    from libpy.firebird.const_olympo import vipe_nombre
    conector = Conexion()
    
    meta = MetaData(bind=conector.engine)
    tbl_vistas = Table(nombre_tabla(cl_VistasPersonalizadas), meta, autoload=True)
    
    errores = [80, 100, 102, 109, 110, 244, 698, 1084, 1287, ]
    
    for vista in conector.conexion.\
            execute(tbl_vistas.\
                    select(and_(tbl_vistas.c[vipe_textosql] != None,
                                tbl_vistas.c[vipe_nombre] != None,
                                tbl_vistas.c.cod_objeto > errores[-1],
                                not_(tbl_vistas.c.cod_objeto.in_(errores)),
                                )).\
                    order_by(desc(tbl_vistas.c.cod_objeto))):
        try:
            print '\n\n\n', vista.cod_objeto, vista[vipe_nombre]
            print '--------------------------------------------------------'
            r = mostrar_vista(vista.cod_objeto, None, 10, conector)
            print r.tostring()
                    
        except Exception, e:
            raise
            print vista.cod_objeto, '*' * 20, str(e), '\n'
#            exit()