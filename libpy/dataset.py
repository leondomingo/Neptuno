# -*- coding: utf-8 -*-

from decimal import Decimal
from ficherocsv import FicheroCSV
import simplejson
import datetime
from libpy.util import default_fmt_float
import re

COLUMNAS = 'columnas'
NUM_RESULTADOS = 'numero_resultados'
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

def quitar_especiales(texto):
    return re.sub(r'[^a-zA-Z0-9\-_\s]', '_', texto)

class DataSetRowIterator(object):
    
    def __init__(self, row):
        self.row = row
        self.i = 0
        self.l = len(self.row.columnas)
        
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
    
    columnas = []
    
    def __init__(self, **kw):
        self.attr = kw
        
    def __str__(self):
        resultado = []
        for k, v in self.attr.iteritems():
            resultado.append('%s=%s' % (k, v))
            
        return ', '.join(resultado)
        
    def __getattr__(self, name):
        if self.attr.has_key(name):
            return self.attr[name]
        else:
            raise Exception('<DataSet>: miembro "%s" no existe' % name)
        
    def __iter__(self):                
        return DataSetRowIterator(self)

    def __getitem__(self, key):
        if isinstance(key, int):
            k = self.columnas[key]
            if isinstance(k, unicode):
                k = k.encode('utf-8')
                
            return self.attr[k]
        
        elif self.attr.has_key(key):
            return self.attr[key]
        
    def __setitem__(self, key, value):
        if isinstance(key, int):
            k = self.columnas[key]
            if isinstance(k, unicode):
                k = k.encode('utf-8')
                            
            self.attr[k] = value
        
        else:
            if self.attr.has_key(key):
                self.attr[key] = value
                
            else:
                self.attr[key] = value

class DataSet(object):
    
    date_fmt = '%d/%m/%Y'
    time_fmt = '%H:%M'
    datetime_fmt = '%d/%m/%Y %H:%M:%S'
    true_const = True
    false_const = False

    def __init__(self, columnas, types=None, limite=None, totales=None):
        
        self.columnas = []
        self.labels = []
        self.types = []
        
        for col in columnas:
            if isinstance(col, tuple):
                # (<col>, <etiqueta>, <tipo>,) 
                self.columnas.append(col[0])
                self.labels.append(col[1] or col[0])
                self.types.append(col[2])
            else:
                self.columnas.append(col)
                self.labels.append(col)
                self.types.append('')

        self.limite_resultados = limite
        self.datos = []
        self.numero_resultados = 0
        self.float_fmt = default_fmt_float
        self.totales = totales
        
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
            self.datos.append(dato)
            
        elif isinstance(dato, dict):
            # comparar claves y columnas
            for k in dato.keys():
                if k not in self.columnas:
                    raise Exception('La clave "%s" no es correcta' % k)
            
            self.append(DataSetRow(**dato))

        elif isinstance(dato, DataSet):
            for d in dato:
                self.append(d)
            
        elif isinstance(dato, list) or hasattr(dato, '__iter__'):
            d = {}
            for col, v in zip(self.columnas, dato):
                if isinstance(col, unicode):
                    col = col.encode('utf-8')
                    
                d[col] = v
                
            self.append(DataSetRow(**d))

        else:
            self.append([None] * len(self.columnas))        
        
        self.datos[-1].columnas = self.columnas        
        return self.datos[-1]
    
    def __iter__(self):
        return iter(self.datos)
    
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
        return reversed(self.datos)
    
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
        return len(self.datos)
    
    def __getitem__(self, index):
        return self.datos[index]
    
    def __str__(self):
        return self.tostring()
    
    def getlabel(self, i):
        if not isinstance(i, int):
            i = self.columnas.index(i)
        
        return self.label
    
    def gettype(self, i):
        if not isinstance(i, int):
            i = self.columnas.index(i)
            
        return self.types[i]
    
    def tostring(self, width=None, fit_width=True):
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
            widths = [0] * len(self.columnas)
            
            for i, c in enumerate(self.columnas):
                for d in self.datos: 
                    if len(str(d[c])) > widths[i]:
                        widths[i] = len(str(d[c]))
                        
                if len(self.labels[i]) > widths[i]:
                    widths[i] = len(self.labels[i])

                if width and widths[i] > width:
                    widths[i] = width
        else:
            widths = [width or 10] * len(self.columnas)
            
        resultado = ''
        
        cabecera = '|'
        for i, c in enumerate(self.labels):
            cabecera += str(c)[:widths[i]].center(widths[i]) + '|'
            
        l = len(cabecera)-2
            
        resultado += '|'+'-'*l + '|\n'
        resultado += cabecera + '\n'
        resultado += '|'+'-'*l + '|\n'
        
        totales = self.init_totales()
        
        for dato in self.datos:
            linea = '|'
            for i, c in enumerate(self.columnas):
                valor = dato[c]
                if valor is None:
                    valor = ''
                    
                w = widths[i]
                
                # totalizaciones
                if self.totales:
                    if totales.has_key(c):
                        totales[c] = self.acumular(totales[c], valor)
                
                if isinstance(dato[c], float) or isinstance(dato[c], Decimal):
                    linea += self.float_fmt(dato[c])[:w].rjust(w)
                    
                elif isinstance(dato[c], bool):
                    linea += (self.true_const if dato[c] else self.false_const).rjust(w)                   

                elif isinstance(dato[c], int):
                    linea += ('%d' % dato[c])[:w].rjust(w)
                    
                elif isinstance(dato[c], int) or isinstance(dato[c], long):
                    linea += str(dato[c])[:w].rjust(w)

                elif isinstance(dato[c], datetime.datetime):
                    linea += dato[c].strftime('%s %s' % (self.date_fmt, self.time_fmt))[:w].rjust(w)

                elif isinstance(dato[c], datetime.date):
                    linea += dato[c].strftime(self.date_fmt)[:w].rjust(w)

                elif isinstance(dato[c], datetime.time):
                    linea += dato[c].strftime(self.time_fmt)[:w].rjust(w)

                else:
                    linea += str(valor).decode('utf-8').replace('\n', '')[:w].ljust(w)
                     
                linea += '|'
            
            resultado += linea + '\n'
            
        resultado += '|'+'-'*l + '|\n'
        
        # línea de totales
        if self.totales:
            linea = '|'
            for i, c in enumerate(self.columnas):
                w = widths[i]                
                if c in self.totales:                    
                    linea += self.float_fmt(totales[c])[:w].rjust(w)                    
                else:
                    linea += ''.rjust(w)
                    
                linea += '|'
                    
            resultado += linea + '\n'                    
            resultado += '|'+'-'*l + '|\n'
            
        return resultado
        
    def to_json(self, encoding=None):
        """
        Devuelve los datos del DataSet en una cadena con formato JSON.
        
        IN
          encoding <str> (opcional)
          
        OUT
          <str>
          
          {
           "numero_resultados": <int>,
           "limite_resultados": <int>,
           "columnas":          [<str>, <str>, ...],
           "datos":             [
                                 [d11, d12, ...],
                                 [d21, d22, ...],
                                 ...                     
                                ],
           "totales":           [<float>, ...]
          }
        """
        
        datos = {
                 COLUMNAS: self.labels,
                 NUM_RESULTADOS: (self.numero_resultados or len(self)),
                 LIMITE_RESULTADOS: len(self),
                 DATOS: [],
                 TOTALES: None
                }
        
                    
        totales = self.init_totales()
        
        for d in self.datos:
            dato = []
            for idx, i in enumerate(d):
                
                # totalizaciones
                if self.totales:
                    if totales.has_key(self.columnas[idx]): 
                        totales[self.columnas[idx]] = self.acumular(totales[self.columnas[idx]], i)
                
                # date
                if isinstance(i, datetime.date):
                    dato.append(i.strftime(self.date_fmt))
                    
                # time
                elif isinstance(i, datetime.time):
                    dato.append(i.strftime(self.time_fmt))
                
                # datetime
                elif isinstance(i, datetime.datetime):
                    dato.append(i.strftime(self.datetime_fmt))
                    
                # float, Decimal
                elif isinstance(i, float) or isinstance(i, Decimal):
                    dato.append(self.float_fmt(i))
                    
                # bool
                elif isinstance(i, bool):
                    dato.append(self.true_const if i else self.false_const)
                    
                # int
                elif isinstance(i, int):
                    dato.append(i)
                
                elif isinstance(i, unicode):
                    dato.append(i.encode(encoding or 'utf-8'))
                    
                else:
                    dato.append(str(i or ''))
                    
            datos[DATOS].append(dato)
            
        if self.totales:
            datos[TOTALES] = []
            for c in self.columnas:
                if c in self.totales:
                    datos[TOTALES].append(self.float_fmt(totales[c]))
                    
                else:
                    datos[TOTALES].append(None)
        
        if encoding:
            return simplejson.dumps(datos, encoding=encoding)
        
        else:
            return simplejson.dumps(datos)
        
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
        for i, c in enumerate(self.columnas):
            
            label = self.labels[i]
            if isinstance(label, unicode):
                label = label.encode('utf-8')
                
            if not c.startswith('id') or mostrar_ids:
                columnas.append(quitar_especiales(self.columnas[i]))
                labels.append(label)
        
        fichero_csv.add(labels)
        
        totales = self.init_totales()
        
        for dato in self.datos:
            
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
            
        self.datos.sort(cmp=compara)
    
    @staticmethod
    def procesar_resultado(conector, query, limite_resultados=None, pos=None, 
                           orderbyid=False, columnas=None, row_func=None,
                           mostrar_ids=False):
        """
        Ejecuta la consulta 'query' y procesa los resultados.
        
        IN
          conector <conexionNeptuno>
          query
          limite_resultados <int> => None
          pos <int> => None
          numero_resultados <bool> => None
          order_byid <bool> => False
          
          columnas <list> => None
          Permite cambiar los nombres de las columnas que tiene la query por el 
          correspondiente en esta lista
          
          row_func <function> => None
          Permite generar una fila "ad hoc" como resultado. Es una función que recibe 
          una fila del dataset (row) y devuelve una lista de la forma:
            [v1, v2, ...]
          
          Por ejemplo,
            def mi_funcion(row):
                fila = []
                fila.append(row[0])
                fila.append('%s *** %s' % (row[2], row[1]))
                
                return fila
                
        OUT
          <DataSet>
        """
        
        if orderbyid:
            query = query.order_by('id')
        
        if columnas:
            cols = columnas
        else:
            cols = []
            for c in query.columns:
                if c.name != 'busqueda':
                    if not c.name.startswith('id_'):
                        cols.append((quitar_especiales(c.name),
                                     c.name.encode('utf-8'),
                                     '',))
                        
                    elif mostrar_ids:
                        cols.append((quitar_especiales(c.name),
                                     c.name.encode('utf-8'),
                                     '',))

        ds = DataSet(columnas=cols, limite=limite_resultados)
        ds.numero_resultados = conector.conexion.execute(query).rowcount
        
        for fila in conector.conexion.\
                execute(query.limit(limite_resultados).offset(pos)):
            if row_func is None:            
                # recorrer las columnas
                row = []
                for c in query.columns:
                    if c.name != 'busqueda':
                        if not c.name.startswith('id_'):
                            row.append(fila[c])
                            
                        elif mostrar_ids:
                            row.append(fila[c])
                              
                ds.append(row)
            else:
                # calcular la fila mediante la función "row_func"
                ds.append(row_func(fila))
                        
        return ds