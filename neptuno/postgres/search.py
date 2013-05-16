# -*- coding: utf-8 -*-

from neptuno.dataset import DataSet
from neptuno.util import strtotime
from sqlalchemy import Table, MetaData, select, exists
from sqlalchemy.sql.expression import and_, Select, or_, alias
from sqlalchemy.types import DATE, TIME, DATETIME, INTEGER, NUMERIC, BOOLEAN, BIGINT
import re
import datetime as dt

_CONSTANT_DATE_TODAY       = 'today'
_CONSTANT_DATE_START_WEEK  = 'start_week'
_CONSTANT_DATE_END_WEEK    = 'end_week'
_CONSTANT_DATE_START_MONTH = 'start_month'
_CONSTANT_DATE_END_MONTH   = 'end_month'
_CONSTANT_DATE_START_YEAR  = 'start_year'
_CONSTANT_DATE_END_YEAR    = 'end_year'
_CONSTANT_DAY              = 'd'
_CONSTANT_WEEK             = 'w'
_CONSTANT_MONTH            = 'm'
_CONSTANT_YEAR             = 'y'

class Busqueda(object):
    
    def __init__(self, tabla, texto_busqueda, columnas_trans=None, strtodatef=None):
        self.tabla = tabla
        self.cols = []
        self.types = []
        for col in self.tabla.columns:
            self.cols.append(col.name)
            self.types.append(col.type)

        self.cache_campo = {}
        
        # string to date conversion function
        self.strtodatef = strtodatef
        
        if not columnas_trans:
            self.cols_trans = [re.sub(r'[^a-z0-9]*', '', self.quitar_acentos(col))
                               for col in self.cols]
        else:
            self.cols_trans = columnas_trans
            
        if texto_busqueda:
            
            if isinstance(texto_busqueda, str):
                texto_busqueda = texto_busqueda.decode('utf-8').lower().encode('utf-8')
                
            elif isinstance(texto_busqueda, unicode):
                texto_busqueda = texto_busqueda.lower().encode('utf-8')
                
            self.condicion = self.condicion_busqueda(texto_busqueda)
            self.orden = self.orden_busqueda(texto_busqueda)
            
        else:
            self.condicion = self.orden = None

    def sin_acentos(self, texto):
        
        resultado = texto
        resultado = re.sub(r'(a|á|à|ä)', '(a|á|à|ä)', resultado)
        resultado = re.sub(r'(e|é|è|ë)', '(e|é|è|ë)', resultado)
        resultado = re.sub(r'(i|í|ì|ï)', '(i|í|ì|ï)', resultado)
        resultado = re.sub(r'(o|ó|ò|ö)', '(o|ó|ò|ö)', resultado)
        resultado = re.sub(r'(u|ú|ù|ü)', '(u|ú|ù|ü)', resultado)
        
        return resultado
        
    def quitar_especiales(self, texto):
        texto = texto.encode('utf-8')
        
        return texto.\
            replace("'", "''").\
            replace('(', ' ').replace(')', ' ').\
            replace('?', ' ').replace('¿', ' ').\
            replace('@', ' ')
            
    def quitar_acentos(self, texto):
        texto = texto.encode('utf-8')
        
        return texto.lower().\
            replace('á', 'a').\
            replace('é', 'e').\
            replace('í', 'i').\
            replace('ó', 'o').\
            replace('ú', 'u').\
            replace('ü', 'u')
            
    def orden_busqueda(self, busqueda):
        terminos = busqueda.decode('utf-8').split(',')

        orden = []
        for termino in terminos:
            termino = termino.strip()
            if termino != '':
                m  = re.search(r'^(\+|-)(\w+)', termino)                
                if m is None:
                    continue
                
                operador = m.group(1)
                
                campos = termino.split(operador)
                
                c = self.get_col(campos[1].strip())
                if c:
                    if operador == '+':
                        operador = ' ASC'
                    elif operador == '-':
                        operador = ' DESC'
                        
                    orden.append('"%s" %s' % (c, operador))
                        
#        print 'ORDEN =' + '\n'.join(orden)
        return ', '.join(orden)
    
    def get_col(self, campo):
        
        if self.cache_campo.has_key(campo.lower()):
            return self.cache_campo[campo.lower()]
        
        else:
            col = None
            for ct, c in zip(self.cols_trans, self.cols):
                
                if ct.startswith(campo.lower()):
                    if not col or col['length'] > len(ct):
                        col = dict(name=c, length=len(ct))
                        
            if col:
                self.cache_campo[campo.lower()] = col['name']
                return col['name']
            
            else:
                return None
            
    def process_date_constants(self, termino):

        def _sub(m):
            cons = m.group(1)
            s = m.group(3)
            q = int(m.group(4) or 0)
            t = m.group(5) or _CONSTANT_DAY
            
            r = None
            if cons == _CONSTANT_DATE_TODAY:
                r = dt.date.today()
            
            elif cons == _CONSTANT_DATE_START_WEEK:
                wd = dt.date.today().weekday()
                r = dt.date.today() - dt.timedelta(days=wd)
            
            elif cons == _CONSTANT_DATE_END_WEEK:
                wd = 6 - dt.date.today().weekday()
                r = dt.date.today() + dt.timedelta(days=wd)
            
            elif cons == _CONSTANT_DATE_START_MONTH:
                today = dt.date.today()
                r = dt.date(today.year, today.month, 1)
            
            elif cons == _CONSTANT_DATE_END_MONTH:
                today = dt.date.today()
                next_month = today + dt.timedelta(days=30)
                r = dt.date(next_month.year, next_month.month, 1) - dt.timedelta(days=1)
            
            elif cons == _CONSTANT_DATE_START_YEAR:
                today = dt.date.today()
                r = dt.date(today.year, 1, 1)
            
            elif cons == _CONSTANT_DATE_END_YEAR:
                today = dt.date.today()
                r = dt.date(today.year, 12, 31)
            
            if r:    
                if s and q:
                    if t == _CONSTANT_DAY:
                        if s == '-':
                            n = -q
                        else:
                            n = q
                        
                        r = r + dt.timedelta(days=n)
                            
                    elif t == _CONSTANT_WEEK:
                        if s == '-':
                            n = -q*7
                        else:
                            n = q*7
                        
                        r = r + dt.timedelta(days=n)
                    
                    elif t == _CONSTANT_MONTH:
                        
                        r_ = r
                        
                        if s == '-':
                            n = -1
                        else:
                            n = +1

                        def _next_month(d, inc):
                            year = d.year
                            if inc > 0:
                                if d.month < 12:
                                    month = d.month + inc

                                elif d.month == 12:
                                    month = 1
                                    year += 1
                            else:
                                if d.month > 1:
                                    month = d.month + inc

                                else:
                                    month = 12
                                    year -= 1

                            return dt.date(year, month, 1)
                            
                        i = 0
                        while abs(i) != q:
                            next_month = _next_month(r_, n)

                            if cons == _CONSTANT_DATE_END_MONTH:
                                day = (_next_month(next_month, 1) - dt.timedelta(days=1)).day

                            else:
                                day = r.day

                            r_ = dt.date(next_month.year, next_month.month, day)
                            
                            i += n
                            
                        r = r_
                            
                    elif t == _CONSTANT_YEAR:
                        if s == '-':
                            n = -q
                            
                        else:
                            n = +q
                            
                        r = dt.date(r.year + n, r.month, r.day)
                        
                return r.strftime('%Y-%m-%d')
            
            else:
                return m.group(0)
        
        return re.sub(r'\{\s*(\w+)(\s+([\+\-])\s*(\d+)\s*(\w{0,1}))?\s*\}', _sub, termino)
    
    def busqueda_campos(self, busqueda):

        terminos = self.process_date_constants(busqueda).split(',')
        
        resultado = None
        sql = []
        for termino in terminos:
            termino = termino.strip()
            if termino != '':
                
                m = re.search(r'^(\w*)\s*(<>|<=|>=|==|=|<|>|#|!)(.+)', termino)                
                if m is None:
                    continue

                operador = m.group(2)
                campos = termino.split(operador)
                
                if operador == '#' or operador == '!':
                    campo = m.group(3).strip()
                    
                else:
                    campo = m.group(1).strip()
                    if m.group(3).strip() == '':
                        continue
                    
                c = self.get_col(campo)
                if not c:
                    continue
                
                col = self.tabla.columns[c]
                
                if operador in ['#', '!']:
                    
                    # fecha y hora
                    if isinstance(col.type, DATE) or \
                    isinstance(col.type, TIME) or \
                    isinstance(col.type, DATETIME):
                        # no es nulo
                        if operador == '#':
                            # "Fecha inicio" IS NOT NULL
                            sql.append('"%s" IS NOT NULL' % c.encode('utf-8'))
                            
                        # es nulo
                        elif operador == '!':
                            # "Fecha inicio" IS NULL
                            sql.append('"%s" IS NULL' % c.encode('utf-8'))

                        elif operador == '==':
                            sql.append('"%s" = \'%s\'' % (c.encode('utf-8'),
                                                          campos[1].strip()))

                    # números (integer, biginteger, numeric)
                    elif isinstance(col.type, INTEGER) or \
                    isinstance(col.type, NUMERIC) or \
                    isinstance(col.type, BIGINT):
                    
                        # no es nulo
                        if operador == '#':
                            # "Nº de alumnos" IS NOT NULL
                            sql.append('"%s" IS NOT NULL' % c.encode('utf-8'))
                            
                        # es nulo
                        elif operador == '!':
                            # "Nº de alumnos" IS NULL
                            sql.append('"%s" IS NULL' % c.encode('utf-8'))
                            
                        elif operador == '==':
                            # Nº de alumnos = 10
                            sql.append('"%s" = %s' % (c.encode('utf-8'),
                                                      campos[1].strip()))
                            
                    # booleano
                    elif isinstance(col.type, BOOLEAN):
                        
                        if operador == '#':
                            sql.append('"%s" = True' % c.encode('utf-8'))
                            
                        elif operador == '!':
                            sql.append('"%s" = False' % c.encode('utf-8'))                                         

                    # texto (o cualquier otra cosa)
                    else:
                        # no es nulo
                        if operador == '#':
                            # trim(coalesce("---" as Text), '')) <> ''
                            sql.append('TRIM(COALESCE(CAST("%s" as Text), \'\')) <> \'\'' % \
                                       c.encode('utf-8'))
                            
                        # es nulo
                        elif operador == '!':
                            # trim(coalesce("---" as Text), '')) = ''
                            sql.append('TRIM(COALESCE(CAST("%s" as Text), \'\')) = \'\'' % \
                                       c.encode('utf-8'))
                            
                        elif operador == '==':
                            sql.append('TRIM(COALESCE(CAST("%s" as Text), \'\')) = \'%s\'' % \
                                        (c.encode('utf-8'),
                                         campos[1]))                                         

                else:
                    explicitos = re.findall(r'"([^"]+)"', campos[1], re.I)
                    
                    # quitar los explícitos y los caracteres "especiales"
                    texto = self.quitar_especiales(re.sub(r'"[^"]+"', '', campos[1], re.I))
                    
                    terminos2 = texto.split()
                    expresiones = []
                    
                    expresion_novacio = 'TRIM(COALESCE(CAST("%s" as Text), \'\')) <> \'\'' % c.encode('utf-8')

                    for termino2 in terminos2:
                        termino2 = self.sin_acentos(termino2)

                        # fecha, hora o fecha-hora
                        if isinstance(col.type, DATE) or \
                        isinstance(col.type, TIME) or \
                        isinstance(col.type, DATETIME):

                            # convert to date
                            if self.strtodatef:
                                try:
                                    termino2 = self.strtodatef(termino2).strftime('%Y-%m-%d')
                                except:
                                    pass
                        
                            if operador in ['=', '<>']:
                                expresion_novacio = None
                                
                                # "Fecha inicio" = '01/01/2010'                   
                                expresion = '"%s" %s \'%s\'' % \
                                    (c.encode('utf-8'),
                                     operador.encode('utf-8'),
                                     termino2)

                            else:
                                # <, >, <=, >=
                                expresion_novacio = '"%s" IS NOT NULL' % c.encode('utf-8')
                                
                                # "Fecha inicio" >= '01/01/2010'
                                expresion = '"%s" %s \'%s\'' % \
                                    (c.encode('utf-8'), 
                                     operador.encode('utf-8'), 
                                     termino2)
                                    
                        # número
                        elif isinstance(col.type, INTEGER) or \
                        isinstance(col.type, NUMERIC) or \
                        isinstance(col.type, BIGINT):

                            if operador in ['=', '<>']:
                                # "Nº de alumnos" = 10                   
                                expresion = '"%s" %s %s' % \
                                    (c.encode('utf-8'),
                                     operador.encode('utf-8'),
                                     termino2)

                            else:
                                # <, >, <=, >=
                                expresion_novacio = '"%s" IS NOT NULL' % c.encode('utf-8')

                                # "Nº de alumnos" >= 10
                                expresion = '"%s" %s %s' % \
                                    (c.encode('utf-8'), 
                                     operador.encode('utf-8'), 
                                     termino2)

                        # texto (o cualquier otra cosa)
                        else: 
                            if operador == '=':                            
                                expresion = "UPPER(CAST(\"%s\" as Text)) SIMILAR TO UPPER('%%%s%%')" % \
                                                (c.encode('utf-8'), termino2)

                            elif operador == '<>':
                                expresion = "UPPER(CAST(\"%s\" as Text)) NOT SIMILAR TO UPPER('%%%s%%')" % \
                                                (c.encode('utf-8'), termino2)

                            else:
                                # <, >, <=, >=
                                expresion_novacio = '"%s" IS NOT NULL' % c.encode('utf-8')

                                expresion = "\"%s\" %s '%s'" % \
                                    (c.encode('utf-8'), operador.encode('utf-8'), termino2)

                        expresiones.append(expresion)
                        
                    # explícitos ("---")
                    for exp in explicitos:

                        if not (isinstance(col.type, DATE) or 
                                isinstance(col.type, TIME) or
                                isinstance(col.type, DATETIME)):

                            if operador == '=':
                                expresion = "UPPER(CAST(\"%s\" as Text)) LIKE UPPER('%%%s%%')" % \
                                                (c.encode('utf-8'), exp.encode('utf-8'))

                            elif operador == '<>':
                                expresion = "UPPER(CAST(\"%s\" as Text)) NOT LIKE UPPER('%%%s%%')" % \
                                                (c.encode('utf-8'), exp.encode('utf-8'))

                        else:
                            # date, time and datetime

                            # convert to date
                            if self.strtodatef:
                                try:
                                    termino2 = self.strtodatef(termino2).strftime('%Y-%m-%d')
                                except:
                                    pass

                            if operador in ['=', '<>']:
                                expresion_novacio = None

                                # "Fecha inicio" = '01/01/2010'
                                expresion = '"%s" %s \'%s\'' % \
                                    (c.encode('utf-8'), 
                                     operador.encode('utf-8'), 
                                     exp.encode('utf-8'))

                            else:
                                # <, >, <=, >=
                                expresion_novacio = '"%s" IS NOT NULL' % c.encode('utf-8')

                                # "Fecha inicio" >= '01/01/2010'
                                expresion = '"%s" %s \'%s\'' % \
                                    (c.encode('utf-8'), 
                                     operador.encode('utf-8'), 
                                     exp.encode('utf-8'))

                        expresiones.append(expresion)
                    
                    expresion_novacio = ('%s AND \n(' % expresion_novacio 
                                         if expresion_novacio else '')
                    
                    if expresion_novacio:
                        sql.append('(' + expresion_novacio + ' AND\n'.join(expresiones) + '))')
                        
                    else:
                        sql.append('(' + ' AND\n'.join(expresiones) + ')')
                            
        if len(sql) > 0:
            resultado = ' AND\n'.join(sql).decode('utf-8')
        
        return resultado
                
    def condicion_busqueda(self, busqueda):
        
        filtros = [f.replace("'", "''").strip() for f in busqueda.decode('utf-8').split(',')]
        
        sql = None
        sql_filtros = []
        for filtro in filtros:

            m = re.search(r'^([^"]*)(<>|<=|>=|==|=|<|>|#|!|\+|-)(.+)', filtro)  
            if m:
                sql_filtro = self.busqueda_campos(filtro)
                
            else:
                sql_termino = []
                
                explicitos = re.findall(r'"([^"]+)"', filtro, re.I)
                
                filtro = re.sub(r'"[^"]+"', '', filtro, re.I | re.U)
                
                # remove special characters
                filtro = filtro.\
                    replace(u'(', u' ').replace(u')', u' ').\
                    replace(u'?', u' ').replace(u'¿', u' ').\
                    replace(u'@', u' ')
                
                search_items = filtro.split()
                
                for item in search_items:

                    # is_date
                    is_date = False
                    item_date = None
                    if self.strtodatef:
                        item_date = self.strtodatef(item)
                        if item_date is not None:
                            item_date = item_date.strftime('%Y-%m-%d')
                            is_date = True

                    # is_time
                    is_time = False
                    try:
                        item_time = strtotime(item)
                        if item_time is not None:
                            is_time = True
                    except:
                        pass

                    if item.strip():
                        sql_campo = []
                        
                        for col_name, tipo in zip(self.cols, self.types):

                            col_name = col_name.encode('utf-8')

                            # DATE
                            if isinstance(tipo, DATE) and is_date:
                                sql_campo.append('"%s" IS NOT NULL AND "%s" = \'%s\'' % (col_name, col_name, item_date))

                            # TIME
                            elif isinstance(tipo, TIME) and is_time:
                                sql_campo.append('"%s" IS NOT NULL AND "%s" = \'%s\'' % (col_name, col_name, item_time))                                

                            # rest of types
                            else:
                                if col_name != 'id' and not col_name.startswith('id_') and not col_name.startswith('_') and not is_date and not is_time:
                                    try:
                                        args_ = (col_name, col_name, self.sin_acentos(item.encode('utf-8')),)
                                        texto  = "(CAST(\"%s\" as Text) <> '' AND UPPER(CAST(\"%s\" as Text)) SIMILAR TO UPPER('%%%s%%'))" % args_
                                        sql_campo.append(texto)

                                    except:
                                        pass
                            
                        texto_sql_campo = ' OR\n'.join(sql_campo)
                        texto_sql_campo = ' (' + texto_sql_campo + ')'
                        
                        sql_termino.append(texto_sql_campo)
                
                # explícitos ("---")        
                for exp in explicitos:
                    
                    item = exp.encode('utf-8')
                    
                    if item.strip():
                        sql_campo = []
                        
                        for col_name in self.cols:
                            if col_name != 'id' and not col_name.startswith('id_') and not col_name.startswith('_'):
                                try:
                                    texto = "(CAST(\"%s\" as Text) <> '' AND UPPER(CAST(\"%s\" as Text)) LIKE UPPER('%%%s%%'))" % (col_name, col_name, item)
                                    sql_campo.append(texto)

                                except:
                                    raise
                            
                        texto_sql_campo = ' OR\n'.join(sql_campo)
                        texto_sql_campo = ' (' + texto_sql_campo + ')'
                        
                        sql_termino.append(texto_sql_campo)
                        
                sql_filtro = ' AND\n'.join(sql_termino)
                sql_filtro = sql_filtro.decode('utf-8')
                
            if sql_filtro:
                sql_filtros.append(sql_filtro)
                
        if sql_filtros:
            sql = ' AND\n'.join(sql_filtros)
        
        return sql

def search(session, table_name, q=None, rp=100, offset=0, show_ids=False, 
           strtodatef=None, filters=None, collection=None):
    """
    IN
      session     <sqlalchemy.orm.session.Session>
      table_name  <str>
      q           <str>
      rp          <int>
      offset      <int>
      show_ids    <bool> (opcional=False)
      strtodatef  <function> (opcional=None)
      filters     [<tuple>, ...]
      collecion   <tuple> (<str>, <str>, <int>,)
      
    OUT
      <DataSet>
    """ 
    
    meta = MetaData(bind=session.bind)
    
    if isinstance(table_name, Select):
        tbl = table_name
        
    else:
        tbl = Table(table_name, meta, autoload=True)
    
    sql = None
    order = ''
    if q:
        
        # process "q"
        qres = Busqueda(tbl, q, strtodatef=strtodatef)
        
        # apply search conditions
        sql = and_(qres.condicion, sql)
        
        # apply order
        if qres.orden:
            order = qres.orden
         
    # apply filters
    if filters:
        filters_tuple = (sql,)
        for f in filters:
            if len(f) > 2:
                # (<field name>, <field value>, <operator>,)
                # different
                if f[2] == '!=':
                    filters_tuple += (tbl.c[f[0]] != f[1],)
                    
                # greater
                elif f[2] == '>':
                    filters_tuple += (tbl.c[f[0]] > f[1],)
                
                # greater or equal
                elif f[2] == '>=':
                    filters_tuple += (tbl.c[f[0]] >= f[1],)
                    
                # less
                elif f[2] == '<':
                    filters_tuple += (tbl.c[f[0]] < f[1],)
                    
                # less or equal
                elif f[2] == '<=':
                    filters_tuple += (tbl.c[f[0]] <= f[1],)
                    
                # equal (and anything else...)
                else:
                    filters_tuple += (tbl.c[f[0]] == f[1],)
                    
            elif len(f) == 2:
                # (<field name>, <field value>,)
                # equal (by default) 
                filters_tuple += (tbl.c[f[0]] == f[1],)
                
            elif len(f) == 1:
                filters_tuple += (f[0],)
        
        sql = and_(*filters_tuple)
    
    if collection:
        
        child_table_name = collection[0]
        child_attr = collection[1]
        parent_id = collection[2]
        
        child_table = Table(child_table_name, meta, autoload=True)
        
        sel = select([child_table.c.id], from_obj=child_table,
                     whereclause=and_(child_table.c[child_attr] == parent_id,
                                      child_table.c.id == tbl.c.id,
                                      ),
                     ).correlate(tbl)
        
        sql = and_(sql, exists(sel))
            
    # where
    if isinstance(tbl, Select):
        qry = tbl.where(sql)
            
    else:
        qry = tbl.select(whereclause=sql)
        
    # order by
    if order:
        qry = qry.order_by(order)
        
    return DataSet.procesar_resultado(session, qry, rp, offset, show_ids)

class Search(object):
    
    def __init__(self, session, table_name, strtodatef=None):
        self.session = session
        self.table_name = table_name
        
        self.meta = MetaData(bind=self.session.bind)
        self.strtodatef = strtodatef
        self.sql = None
        self.order = ''
        
        if isinstance(self.table_name, Select):
            self.tbl = self.table_name
            
        else:
            self.tbl = Table(self.table_name, self.meta, autoload=True)
        
        self.from_ = self.tbl
            
    def apply_qry(self, q):
        
        if q:
            if isinstance(q, unicode):
                q = q.encode('utf-8')

            # process "q"
            qres = Busqueda(self.tbl, q, strtodatef=self.strtodatef)
            
            # apply search conditions    
            self.sql = and_(qres.condicion, self.sql)
            
            # apply order
            if qres.orden:
                self.order = qres.orden
                
    def and_(self, *cond):
        self.sql = and_(self.sql, *cond)
        
    def or_(self, cond):
        self.sql = or_(self.sql, cond)
        
    def join(self, *args, **kwargs):
        self.from_ = self.from_.join(*args, **kwargs)
        
    def outerjoin(self, *args, **kwargs):
        self.from_ = self.from_.outerjoin(*args, **kwargs)
                
    def apply_filters(self, filters):
        
        tbl = self.tbl
        
        # apply filters
        if filters:
            filters_tuple = (self.sql,)
            for f in filters:
                if len(f) > 2:
                    # (<field name>, <field value>, <operator>,)
                    # different
                    if f[2] == '!=':
                        filters_tuple += (tbl.c[f[0]] != f[1],)
                        
                    # greater
                    elif f[2] == '>':
                        filters_tuple += (tbl.c[f[0]] > f[1],)
                    
                    # greater or equal
                    elif f[2] == '>=':
                        filters_tuple += (tbl.c[f[0]] >= f[1],)
                        
                    # less
                    elif f[2] == '<':
                        filters_tuple += (tbl.c[f[0]] < f[1],)
                        
                    # less or equal
                    elif f[2] == '<=':
                        filters_tuple += (tbl.c[f[0]] <= f[1],)
                        
                    # equal (and anything else...)
                    else:
                        filters_tuple += (tbl.c[f[0]] == f[1],)
                        
                elif len(f) == 2:
                    # (<field name>, <field value>,)
                    # equal (by default) 
                    filters_tuple += (tbl.c[f[0]] == f[1],)
                    
                elif len(f) == 1:
                    filters_tuple += (f[0],)
            
            self.sql = and_(*filters_tuple)
        
    def __call__(self, rp=100, offset=0, collection=None, no_count=False, show_ids=False):
        """
        IN
          rp          <int>
          offset      <int>
          filters     [<tuple>, ...]
          collecion   <tuple> (<str>, <str>, <int>,)
          no_count    <bool> => False
          show_ids    <bool> => False
          
        OUT
          <DataSet>
        """ 
        
        sql = self.sql
        if collection:

            child_table_name = collection[0]
            child_attr = collection[1]
            parent_id = collection[2]

            child_attr_alias = '%s$' % child_attr
            if self.tbl.c.has_key(child_attr_alias):
                sql = and_(sql, self.tbl.c[child_attr_alias] == parent_id)

            else:
                child_table = alias(Table(child_table_name, self.meta, autoload=True))
                
                self.from_ = self.from_.\
                    join(child_table,
                         and_(child_table.c.id == self.tbl.c.id,
                              child_table.c[child_attr] == parent_id))
            
        # where
        if isinstance(self.tbl, Select):
            qry = self.tbl.where(sql)
                
        else:
            qry = select([self.tbl], from_obj=self.from_, whereclause=sql)
            
        # order by
        if self.order:
            qry = qry.order_by(self.order)
            
        return DataSet.procesar_resultado(self.session, qry, rp, offset, 
                                          no_count=no_count, show_ids=show_ids)
