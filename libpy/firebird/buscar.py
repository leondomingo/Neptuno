#-*- coding: utf-8 -*-

from sqlalchemy.databases.firebird import FBDate, FBTime, FBDateTime, FBFloat,\
    FBNumeric
import simplejson
from sqlalchemy import MetaData, Table #, func
from unidadescompartidasNeptuno import usuariosNeptuno 
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.const_datos_neptuno import CAMPOS
from libpy.conexion import Conexion
from nucleo.const_datos import ROL_TABLAS, ROL_COLUMNAS
from nucleo.definicion_clases import DEFINICION_CLASES
from libpy.roles import RolColumnas,  RolTablas
usuariosNeptuno.privl_tabla = RolTablas(ROL_TABLAS)
usuariosNeptuno.privl_columna = RolColumnas(ROL_COLUMNAS)

def procesar_resultado(conector, query, limite_resultados=None, pos=None, 
                       numero_resultados=False, orderbyid=False):
    """Ejecuta la consulta 'query' y procesa los resultados"""
    
    if orderbyid:
        query = query.order_by('id')
    
    resultado = []
    for fila in conector.conexion.execute(query.limit(limite_resultados).offset(pos)):
        fila_resultado = []
        for c in fila.keys():
            col = {}
            if not 'busqueda' in c and not c.startswith('id_'):                     
                col[c] = str(fila[c] or '')
                fila_resultado.append(col)
                
        resultado.append(fila_resultado)

    # calcular el número de resultados devolverlo en el último objeto de 'resultado'
    fila_resultado = []
    if numero_resultados:
        col = {}
        col['numero_resultados'] = conector.conexion.execute(query).rowcount
        col['limite_resultados'] = str(limite_resultados or '')
        
        fila_resultado.append(col)
        
        resultado.append(fila_resultado)
        
    return simplejson.dumps(resultado)


def search(tabla, id_usuario, busqueda=None, campos=None, id_registro=None, \
           limite_resultados=None, pos=0, numero_resultados=100, orderbyid=False):
    """
    Busca en la 'tabla' y el 'campo' el 'valor' indicados por parámetro. Se puede especificar un número máximo de resultados
    a través del parámetro 'limite_resultados'.
    
    Se utiliza 'id_usuario' para controlar los permisos de acceso.
    
    Entrada:
        busqueda
        tabla        
        campos -> Una lista de pares (campo,valor) de la forma [[c1,v1], [c2, v2], ...]
        id_registro -> Para buscar un registro concreto con un cierto 'id'
        id_usuario
        limite_resultados -> Número de registros máximo a devolver
		pos -> Posición a partir de la cual devuelve los registros
        numero_resultados -> Si se pasa, devuelve el número total de resultados
        orderbyid -> a cierto ordena por id, a falso no le aplica orderby
    """
    
    def sin_acentos(texto):
        
        return texto.lower().\
                replace('á', '_').\
                replace('é', '_').\
                replace('í', '_').\
                replace('ó', '_').\
                replace('ú', '_')
    
    conector = Conexion()    
    try:
        meta = MetaData(bind=conector.engine)
        objtabla = Table('vb_%s' % tabla, meta, autoload=True)
        
        if busqueda is None:
            if id_registro is None:
                filtros = []
                for campo in campos:
                    filtros.append('%(campo)s = \'%(valor)s\'' % {'campo': campo[0], 'valor': campo[1]})
                    
                if len(filtros) > 0:
                    SQL = ' AND '.join(filtros)                
            else:
                SQL = objtabla.c.cod_objeto == id_registro
        else:
            # quitar caracteres especiales            
            busqueda = busqueda.replace("'", "''")
#                replace('(', ' ').replace(')', ' ').\
#                replace('?', ' ').replace('¿', ' ').\
#                replace('!', ' ').replace('¡', ' ').\
#                replace('#', ' ').\
#                replace('@', ' ')
                
            terminos_de_busqueda = busqueda.split()
                        
            if '*' in busqueda:
                SQL = None
            else:
                sql_termino = []
                SQL = None
                for termino in terminos_de_busqueda:                    
                        
                    termino = sin_acentos(termino)
                    
                    if termino.strip() != '':
                        sql_campo = []
#                        cond_campo = None
                        for columna in objtabla.columns:
                            if columna.name != 'cod_objeto': 
                                try:
#                                    cond_campo = or_(cond_campo,
#                                                    func.upper(columna).like(func.upper('%%%s%%' % termino)))
                                    
                                    texto = "UPPER(%s) LIKE UPPER('%%%s%%')" % (columna.name, termino)
                                    sql_campo.append(texto)
                                except:
                                    return termino
                            
                        texto_sql_campo = ' OR\n '.join(sql_campo)
                        texto_sql_campo = ' (' + texto_sql_campo + ')'
                        
                        sql_termino.append(texto_sql_campo)
                        
#                        SQL = and_(SQL, cond_campo)
                        
                SQL = ' AND\n '.join(sql_termino)
                
#        usuario =
        usuariosNeptuno.comprobar_usuario(conector, id_usuario)
        
#        if usuario.getPrivilegioTabla(tabla) == PRIVL_NINGUNO:
#            raise NoTienePrivilegios(usuario.nombre_usuario, tabla)
        
#        tbl_atributos = Table(nombre_tabla(cl_Atributos), meta, autoload=True)
#        
#        nombres = []
#        campos = []
#        for atributo in tbl_atributos.select(tbl_atributos.c[atributos_clase] == tabla).execute():
#            campos.append('atr_%d' % atributo.cod_objeto)
#            nombres.append(atributo[atributos_nombre])
#        
#        gestor = GestorOlympo(conector)
#        
#        # usuario, fecha de creación y fecha de actualización
#        atributos_estandar = [gestor.atributo_fechadecreacion(tabla),
#                              gestor.atributo_fechadeactualizacion(tabla),
#                              gestor.atributo_usuario(tabla)]
        
        qry = objtabla.select(whereclause=SQL)
        
        if orderbyid:
            qry = qry.order_by(objtabla.c.cod_objeto)
            
        if DEFINICION_CLASES.has_key(tabla):
            columnas = [columna[0] for columna in DEFINICION_CLASES[tabla][CAMPOS]]
            nombres = [nombre[1] for nombre in DEFINICION_CLASES[tabla][CAMPOS]]
            
        else:
            # en caso de que no haya definición para esa tabla
            columnas = [c.name for c in objtabla.columns]
            nombres = columnas
        
        resultado = []    
        for fila in conector.conexion.execute(qry.limit(limite_resultados).offset(pos)):
            fila_resultado = []
            for c in objtabla.columns:
                col = {}
                if not c.name.startswith('id_'):
                    
                    if c.name != 'cod_objeto':
                        try:
                            nombre_columna = nombres[columnas.index(c.name)]
                        except ValueError:
                            nombre_columna = c.name                    
                    
                    # fecha
                    if isinstance(c.type, FBDate):
                        col[nombre_columna] = (fila[c.name].strftime('%d/%m/%Y') \
                                               if fila[c.name] != None else '')
                        
                    # hora
                    elif isinstance(c.type, FBTime):
                        col[nombre_columna] = (fila[c.name].strftime('%H:%M:%S') \
                                               if fila[c.name] != None else '')

                    # fecha/hora
                    elif isinstance(c.type, FBDateTime):
                        col[nombre_columna] = (fila[c.name].strftime('%d/%m/%Y %H:%M:%S') \
                                               if fila[c.name] != None else '')
                        
                    # real
                    elif isinstance(c.type, FBFloat) or isinstance(c.type, FBNumeric):
                        col[nombre_columna] = ('%2.2f' % fila[c.name] \
                                               if fila[c.name] != None else '')
                                                
                    else:
                        # renombrar 'cod_objeto' por 'id'
                        if c.name == 'cod_objeto':
                            col['id'] = str(fila[c.name] or '')
                        else:
                            if isinstance(fila[c.name], unicode):
                                col[nombre_columna] = fila[c.name].encode('utf-8')
                                
                            elif isinstance(fila[c.name], str):
                                col[nombre_columna] = fila[c.name].decode('iso-8859-1').encode('utf-8')
                            
                            else:
                                col[nombre_columna] = str(fila[c.name] or '')
                        
                    fila_resultado.append(col)
                    
            resultado.append(fila_resultado)
            
        # calcular el número de resultados y devolverlo en el último objeto de 'resultado'
        fila_resultado = []
        if numero_resultados:
            col = {}
            col['numero_resultados'] = len(resultado)
            col['limite_resultados'] = str(limite_resultados or '')
            
            fila_resultado.append(col)
            
            resultado.append(fila_resultado)
            
        return resultado
                
    except (NoExisteUsuario, SesionIncorrecta):
        raise