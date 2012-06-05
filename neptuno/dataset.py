# -*- coding: utf-8 -*-

from decimal import Decimal
from jinja2 import Environment, PackageLoader
from neptuno.ficherocsv import FicheroCSV
from neptuno.util import default_fmt_float
from neptuno.xlsreport import XLSReport
from sqlalchemy.types import INTEGER, NUMERIC, DATE, TIME, BOOLEAN, BIGINT, \
    DATETIME
import datetime
import re
import sys

COLUMNAS = 'columnas'
COUNT = 'count'
LIMITE_RESULTADOS = 'limite_resultados'
DATOS = 'datos'
TOTALES = 'totales'

def tocsv(e):
    def _tocsv(func):
        def __tocsv(*args, **kwargs):
            return func(*args, **kwargs).to_csv(encoding=e)
        
        return __tocsv
    
    return _tocsv

def tostring(func):
    def __tostring(*args, **kwargs):
        return func(*args, **kwargs).tostring()
    
    return __tostring

def tojson(func):
    def __tojson(*args, **kwargs):
        return func(*args, **kwargs).to_json()
    
    return __tojson

def remove_specials(texto):
    return re.sub(r'[^a-zA-Z0-9_]', '_', texto)

class DataSetRowIterator(object):
    
    def __init__(self, row):
        self.row = row
        self.i = 0
        self.l = len(self.row.cols)
        
    def __iter__(self):
        return self
    
    def next(self):
        if self.i < self.l:
            item = self.row[self.i]
            self.i += 1
            
            return item
        else:
            raise StopIteration
    
    def __next__(self):
        return self.next()

class DataSetRow(object):
    
    cols = []
    
    def __init__(self, **kw):
        self.attr = kw
        
    def __str__(self):
        result = []
        for k, v in self.attr.iteritems():
            result.append('%s=%s' % (k, v))
            
        return ', '.join(result)
        
    def __getattr__(self, name):
        if self.attr.has_key(name):
            return self.attr[name]
        else:
            raise Exception('<DataSet>: member "%s" does not exist' % name)
        
    def __iter__(self):                
        return DataSetRowIterator(self)

    def __getitem__(self, key):
        if isinstance(key, int):
            k = self.cols[key]
            if sys.version_info < (2, 6, 6):
                if isinstance(k, unicode):
                    k = k.encode('utf-8')
            
            if self.attr.has_key(k):
                return self.attr[k]
            
            else:
                return None
        
        elif self.attr.has_key(key):
            return self.attr[key]
        
    def __setitem__(self, key, value):
        if isinstance(key, int):
            k = self.cols[key]
            if sys.version_info < (2, 6, 6):
                if isinstance(k, unicode):
                    k = k.encode('utf-8')
                            
            self.attr[k] = value
        
        else:
            if sys.version_info < (2, 6, 6):
                if isinstance(key, unicode):
                    key = key.encode('utf-8')
                    
            self.attr[key] = value
                
class DataSet(object):
    
    date_fmt = '%d/%m/%Y'
    time_fmt = '%H:%M'
    datetime_fmt = '%d/%m/%Y %H:%M:%S'
    true_const = True
    false_const = False
    int_fmt = '%d'
    
    def float_fmt(self, value):
        return default_fmt_float(value)
    
    def __init__(self, cols, types=None, limite=None, totales=None, **fmt):
        
        self.cols = []
        self.labels = []
        self.types = []
        
        # date
        if fmt.has_key('date_fmt'):
            self.date_fmt = fmt['date_fmt']
            
        # time
        if fmt.has_key('time_fmt'):
            self.time_fmt = fmt['time_fmt']
            
        # datetime
        if fmt.has_key('datetime_fmt'):
            self.datetime_fmt = fmt['datetime_fmt']
            
        # int
        if fmt.has_key('int_fmt'):
            self.int_fmt = fmt['int_fmt']
        
        # float
        if fmt.has_key('float_fmt'):
            self.float_fmt = fmt['float_fmt']
        
        for col in cols:
            self.append_col(col)

        self.limite_resultados = limite
        self.data = []
        self.count = 0
        self.totales = totales
        
    def append_col(self, col):
        if isinstance(col, tuple):
            # (<col>, <etiqueta>, <tipo>,) 
            self.cols.append(col[0])
            self.labels.append(col[1] or col[0])
            self.types.append(col[2])
            
        else:
            self.cols.append(col)
            self.labels.append(col)
            self.types.append('')

    def init_totales(self):
        if self.totales:
            totales = dict(zip(self.totales, [None] * len(self.totales)))
            
        else:
            totales = {}
            
        return totales
    
    def acumular(self, acumulado, valor):
        return (acumulado or 0) + (valor or 0)
        
    def append(self, dato=None):
        """
        IN
          dato
            <list>
            <dict>
            <DataSetRow>
            
        OUT
          ???
        """
        
        if isinstance(dato, DataSetRow):
            self.data.append(dato)
            
        elif isinstance(dato, dict):
            # compare keys and columns
            d = {}
            for k, v in dato.iteritems():
                if k not in self.cols:
                    raise Exception('The key "%s" is not correct' % k)
                
                if sys.version < (2, 6):
                    if isinstance(k, unicode):
                        k = k.encode('utf-8')
                        
                d[k] = v
            
            self.append(DataSetRow(**d))

        elif isinstance(dato, DataSet):
            for d in dato:
                self.append(d)
            
        elif isinstance(dato, list) or hasattr(dato, '__iter__'):
            d = {}
            for col, v in zip(self.cols, dato):
                if sys.version_info < (2, 6, 6):
                    if isinstance(col, unicode):
                        col = col.encode('utf-8')
                    
                d[col] = v
                
            self.append(DataSetRow(**d))

        else:
            self.append([None] * len(self.cols))        
        
        self.data[-1].cols = self.cols        
        return self.data[-1]
    
    def __iter__(self):
        return iter(self.data)
    
    def reversed(self):
        """Devuelve un iterador para recorrer la lista del final al principio
        
        Para un DataSet de N valores
        
        item0
        item1
        ...
        itemN-1
        
        devolver
        
        [
         itemN-1,
         ...
         item1,
         item0
        ]
        """
        return reversed(self.data)
    
    def ereversed(self):
        """
        Devuelve un iterador enumerado para recorrer la lista del final al 
        principio.
        
        Para un DataSet de N valores
        
        item0
        item1
        ...
        itemN-1
        
        devolver
        
        [
         (N-1, itemN-1)
         ...
         (1, item1)
         (0, item0)
        ]
        
        """
        return zip(range(len(self)-1, -1, -1), self.reversed())
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        return self.data[index]
    
    def __str__(self):
        return self.to_str()
    
    def getlabel(self, i):
        if not isinstance(i, int):
            i = self.cols.index(i)
        
        return self.label
    
    def gettype(self, i):
        if not isinstance(i, int):
            i = self.cols.index(i)
            
        return self.types[i]
    
    def _format(self, fmt, value):

        if isinstance(fmt, (str, unicode,)):
            s = unicode(fmt % value)
            
        elif hasattr(fmt, '__call__'):
            s = unicode(fmt(value))
            
        else:
            s = unicode(value or '')
            
        return s
    
    def _formatdt(self, fmt, value):

        if isinstance(fmt, (str, unicode,)):
            s = unicode(value.strftime(fmt))
            
        elif hasattr(fmt, '__call__'):
            s = unicode(fmt(value))
            
        else:
            s = unicode(value or '')
            
        return s

    def to_str(self, width=None, fit_width=True):
        """
        Devuelve los datos del DataSet en un cadena con formato tabular.
        
        |------|------|------|------|
        | (c1) | (c2) | (c3) | (c4) |
        |---------------------------|
        |      |      |      |      |
        |      |      |      |      |
        |      |      |      |      |
        |---------------------------|
        |      |      |      |      | <- totales
        |---------------------------|
        
        IN
          width <int> (opcional)
          Indica el ancho de las columnas
          
          fit_width <bool> (por defecto=True)
          Hace las columnas tan anchas como el valor m�s ancho, que no sobrepase
          el ancho fijado por 'width'.
        """
        
        if fit_width:
            widths = [0] * len(self.cols)
            
            for i, c in enumerate(self.cols):
                for d in self.data: 
                    if len(str(d[c])) > widths[i]:
                        widths[i] = len(unicode(d[c]))
                        
                if len(self.labels[i]) > widths[i]:
                    widths[i] = len(self.labels[i])

                if width and widths[i] > width:
                    widths[i] = width
        else:
            widths = [width or 10] * len(self.cols)
            
        resultado = ''
        
        cabecera = '|'
        for i, c in enumerate(self.labels):
            cabecera += unicode(c)[:widths[i]].center(widths[i]) + '|'
            
        l = len(cabecera)-2
            
        resultado += '|'+'-'*l + '|\n'
        resultado += cabecera + '\n'
        resultado += '|'+'-'*l + '|\n'
        
        totales = self.init_totales()
        
        for dato in self.data:
            linea = '|'
            for i, c in enumerate(self.cols):
                valor = dato[c]
                if valor is None:
                    valor = u''
                    
                w = widths[i]
                
                # totalizaciones
                if self.totales:
                    if totales.has_key(c):
                        totales[c] = self.acumular(totales[c], valor)
                
                # float/Decimal
                if isinstance(dato[c], (float, Decimal,)):
                    linea += self._format(self.float_fmt, dato[c])[:w].rjust(w)
                    
                # bool
                elif isinstance(dato[c], bool):
                    linea += unicode((self.true_const if dato[c] else self.false_const)).rjust(w)                   

                # int/long
                elif isinstance(dato[c], (int, long,)):
                    linea += self._format(self.int_fmt, dato[c])[:w].rjust(w)

                # datetime
                elif isinstance(dato[c], datetime.datetime):
                    #linea += unicode(dato[c].strftime('%s %s' % (self.date_fmt, self.time_fmt)))[:w].rjust(w)
                    linea += unicode(self._formatdt(self.datetime_fmt, dato[c]))[:w].rjust(w)

                # date
                elif isinstance(dato[c], datetime.date):
                    linea += unicode(self._formatdt(self.date_fmt, dato[c]))[:w].rjust(w)

                # time
                elif isinstance(dato[c], datetime.time):
                    #linea += unicode(dato[c].strftime(self.time_fmt))[:w].rjust(w)
                    linea += unicode(self._formatdt(self.time_fmt, dato[c]))[:w].rjust(w)

                else:
                    linea += unicode(valor).replace('\n', '')[:w].ljust(w)
                     
                linea += '|'
            
            resultado += linea + '\n'
            
        resultado += '|'+'-'*l + '|\n'
        
        # línea de totales
        if self.totales:
            linea = '|'
            for i, c in enumerate(self.cols):
                w = widths[i]                
                if c in self.totales:                    
                    linea += self.float_fmt(totales[c])[:w].rjust(w)                    
                else:
                    linea += ''.rjust(w)
                    
                linea += '|'
                    
            resultado += linea + '\n'                    
            resultado += '|'+'-'*l + '|\n'
            
        return resultado
        
    def to_data(self, encoding=None):
        """
        """
        
        data = []
        
        for row in self.data:
            dato = []
            for item in row:
                
                # date
                if isinstance(item, datetime.date):
                    dato.append(self._formatdt(self.date_fmt, item))
                    
                # time
                elif isinstance(item, datetime.time):
                    dato.append(self._formatdt(self.time_fmt, item))
                
                # datetime
                elif isinstance(item, datetime.datetime):
                    dato.append(self._formatdt(self.datetime_fmt, item))
                    
                # float, Decimal
                elif isinstance(item, (float, Decimal,)):
                    dato.append(self._format(self.float_fmt, item))
                    
                # bool
                elif isinstance(item, bool):
                    dato.append(self.true_const if item else self.false_const)
                    
                # int, long
                elif isinstance(item, int):
                    dato.append(self._format(self.int_fmt, item))
                
                # unicode
                elif isinstance(item, unicode):
                    dato.append(item)
                    
                # ???
                else:
                    dato.append(str(item or '').decode('utf-8'))
                    
            data.append(dato)
            
        return data
        
    def to_csv(self, encoding=None, mostrar_ids=False):
        """
        Devuelve en una cadena con formato CSV el contenido del DataSet.
        
        IN
          encoding <str> (opcional)
          
        OUT
          <str> (csv)
        """
        
        fichero_csv = FicheroCSV()
        fichero_csv.date_fmt = self.date_fmt
        fichero_csv.time_fmt = self.time_fmt
        fichero_csv.true_const = self.true_const
        fichero_csv.false_const = self.false_const
        fichero_csv.float_fmt = self.float_fmt
        
        columnas = []
        labels = []
        for item, c in enumerate(self.cols):
            
            label = self.labels[item]
#            if isinstance(label, unicode):
#                label = label.encode('utf-8')
                
            if not c.startswith('id') or mostrar_ids:
                columnas.append(remove_specials(self.cols[item]))
                labels.append(label)
        
        fichero_csv.add(labels)
        
        totales = self.init_totales()
        
        for dato in self.data:
            
            # totalizar
            if self.totales:
                for idx, c in enumerate(columnas):
                    if totales.has_key(c):
                        totales[c] = self.acumular(totales[c], dato[idx])
                        
            fila = []
            for col in columnas:
                fila.append(dato[col])                 
            
            fichero_csv.add(fila)
            
        # añadir línea con el total
        if self.totales:
            fila_totales = []
            for c in columnas:
                if totales.has_key(c):
                    fila_totales.append(self.float_fmt(totales[c]))
                    
                else:
                    fila_totales.append(None)
                    
            fichero_csv.add(fila_totales)
        
        return fichero_csv.read(encoding)
    
    def to_xls(self, title, filename, fmt=None):
        pl = PackageLoader('neptuno', 'templates')
        env = Environment(loader=pl)
        template = env.get_template('dstoxls.xml')
        
        xr = XLSReport(template)
        
        date_fmt = self.date_fmt.replace('%d', 'dd').\
            replace('%m', 'mm').\
            replace('%Y', 'yyyy')
            
        time_fmt = self.time_fmt.\
            replace('%H', 'HH').\
            replace('%M', 'MM').\
            replace('%S', 'SS')
        
        _fmt = dict(date=date_fmt, time=time_fmt)
        _fmt.update(fmt or {})
            
        params = dict(title=title, ds=self, fmt=_fmt)
        return xr.create(params, filename=filename)
    
    def order(self, claves):
        """
        IN
          claves <list> [(<col>, <signo>), ...]
            * <col>    Nombre de la columna
            * <signo>  +1 para ordenación ascendente
                       -1 para ordenación descendente
          
        OUT
          ???
        """

        def ordenar(ordenar_por):
            def _ordenar(function):
                def __ordenar(*args):
                    for o, signo in ordenar_por:
                        new_args = (args[0][o], args[1][o])
                        r = function(*new_args)
                        
                        if r != 0:
                            break
                    return r * signo
                
                return __ordenar
                        
            return _ordenar
        
        @ordenar(claves)
        def compara(x, y):
            if x < y:
                return -1
            
            elif x == y:
                return 0
            
            else:
                return 1
            
        self.data.sort(cmp=compara)
    
    @staticmethod
    def procesar_resultado(session, query, limit=None, pos=None, no_count=False, show_ids=False):
        """
        IN
          session  <sqlalchemy.orm.session.Session>
          query    <>
          limit    <int>
          pos      <int>
          no_count  <bool> = False
          show_ids  <bool> = False
          
        OUT
          <DataSet>
        """
        
        cols = []
        col_names = []
        for c in query.columns:
            if show_ids or not (c.name.startswith('id_') or c.name.startswith('_')):
                type_ = ''
                if isinstance(c.type, INTEGER) or isinstance(c.type, BIGINT):
                    type_ = 'int'
                    
                elif isinstance(c.type, NUMERIC):
                    type_ = 'float'
                    
                elif isinstance(c.type, DATE):
                    type_ = 'date'
                    
                elif isinstance(c.type, TIME):
                    type_ = 'time'
                    
                elif isinstance(c.type, DATETIME):
                    type_ = 'datetime'
                    
                elif isinstance(c.type, BOOLEAN):
                    type_ = 'bool'
                    
                #print c.type, type
                
                # avoid col name repeat
                name = remove_specials(c.name).lower()
                i = 1
                while name in col_names:
                    name = u'%s_%d' % (name, i)
                    i += 1
                    
                col_names.append(name)
                    
                cols.append((name, # name
                             c.name, # label
                             type_,))
                
        ds = DataSet(cols)
        if not no_count:
            ds.count = session.execute(query).rowcount
            
        else:
            ds.count = 0
        
        if limit == 0:
            limit = None
        
        for fila in session.execute(query.limit(limit).offset(pos)):
            row = []
            for c in query.columns:
                data = fila[c]
                if show_ids or not (c.name.startswith('id_') or c.name.startswith('_')):
                    if isinstance(data, str):
                        data = data.decode('utf-8')
                        
                    if isinstance(data, unicode):
                        data = data.replace(u'\u000B', ' ')
                    
                    row.append(data)

            ds.append(row)
            
            if no_count:
                ds.count += 1
                        
        return ds
    
    @staticmethod
    def query(dbs, query, cols, limit=None, pos=None, show_ids=False):
        """
        IN
          session  <sqlalchemy.orm.session.Session>
          query    <sqlalchemy.orm.query.Query>
          limit    <int>
          pos      <int>
          
        OUT
          <DataSet>
        """
        
        ds = DataSet(cols, limite=limit)
        ds.count = dbs.execute(query).rowcount
        
        if limit == 0:
            limit = None
        
        for row in dbs.execute(query.limit(limit).offset(pos)):
            ds.append(row.values())

        return ds