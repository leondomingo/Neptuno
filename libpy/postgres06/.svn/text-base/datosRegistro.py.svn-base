# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, Table
from sqlalchemy.exc import NoSuchTableError
from neptuno import Neptuno
from libpy.excepciones.eneptuno import NoTienePrivilegios
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.conexion import Conexion
from datetime import date, time
from decimal import Decimal

def record_data(id_usuario, tabla, id_registro=None, conector=None, **kwargs):
    """
    Devuelve los datos de un registro (o de todos) de una tabla en forma de 
    lista de campos.
    
    IN
      id_usuario  <int>         -> Identificador en la tabla <usuarios>
      tabla       <str>         -> Nombre de la tabla
      id_registro <int> => None -> Si no se indica nada aquí se devuelven todos
        
    OUT
      Un JSON de la forma:
        [{campo1}, {campo2}, ...]
            
      Cada "campoX", a su vez, tiene la forma:
      campo = {
               'nombre':            <str>,
               'tipo':              <str>,
               'valor':             <str>,
               'etiqueta':          <str>,
               'requerido':         <bool>
               'solo_lectura':      <bool>,
               'tabla_relacionada': <str>,
               'utilizar_selector': <bool>,
               'valores':           [[{campo}, ...], ...]
              }
              
    EXC
      NoExisteUsuario
      NoTienePrivilegios
    """
    
    if conector is None:
        conector = Conexion()
        
    try:
        la_tabla = Neptuno(conector, tabla, id_usuario)
    except NoSuchTableError:
        la_tabla = Neptuno(conector, str(tabla).replace('vista_busqueda_', ''), id_usuario)
    except (NoExisteUsuario, NoTienePrivilegios):
        raise
    
    if id_registro != None:
        return la_tabla.query_registro(id_registro, **kwargs)
    else:
        return la_tabla.query_tabla()
    
def format_value(value):
    if isinstance(value, date):
        return value.strftime('%d/%m/%Y')
    
    elif isinstance(value, time):
        return value.strftime('%H:%M:%S')
    
    elif isinstance(value, Decimal) or isinstance(value, float):
        return '%2.2f' % value
    
    else:
        return value
    
def raw_data(tabla, id_reg, campos=None, conn=None):
    """
    IN
      tabla      <str>
      id         <int>
      campos     [<str>, ...]
      conn       <ConexionNeptuno> (opcional)
      
    OUT
      {<campo1>, <campo2>, ...}
    """

    if not conn:
        conn = Conexion()

    meta = MetaData(bind=conn.engine)
    tbl = Table(tabla, meta, autoload=True)

    registro = tbl.select(whereclause=tbl.c.id == id_reg).execute().fetchone()
    
    # si "campos" está vacío utilizamos todas las columnas
    if not campos:
        campos = [c.name for c in tbl.columns]

    data = {}
    for c in campos:
        if tbl.columns.has_key(c):
            data[c] = format_value(registro[c])

    return data