# -*- coding: utf-8 -*-

import cStringIO
import csv
from decimal import Decimal
import datetime
from neptuno.util import default_fmt_float, datetostr, timetostr

class FicheroCSV(object):
    
    date_fmt = '%d/%m/%Y'
    time_fmt = '%H:%M'
    true_const = 't'
    false_const = 'f'    
    
    def __init__(self):
        # crear fichero CSV en memoria
        self.fichero_csv = cStringIO.StringIO()
    
        # crear writer CSV
        self.w_csv = csv.writer(self.fichero_csv, delimiter=';', 
                                quoting=csv.QUOTE_ALL)
        
        self.float_fmt = default_fmt_float
        
    def add(self, row):
        """
        Añade una fila al fichero CSV.
        
        IN
          row <list>
        """
        
        float_fmt = self.float_fmt
        
        row_resultado = []
        for i in row:
            
            if isinstance(i, float) or isinstance(i, Decimal):
                row_resultado.append(float_fmt(i))
                
            elif isinstance(i, bool):
                row_resultado.append((self.true_const if i else self.false_const))                 

            elif isinstance(i, int):
                row_resultado.append('%d' % i)

            elif isinstance(i, datetime.datetime):
                datetime_fmt = '%s %s' % (self.date_fmt, self.time_fmt)
                row_resultado.append(i.strftime(datetime_fmt))

            elif isinstance(i, datetime.date):                
                row_resultado.append(datetostr(i, fmt=self.date_fmt))
                
            elif isinstance(i, datetime.time):
                row_resultado.append(timetostr(i, fmt=self.time_fmt))
                
            elif isinstance(i, unicode):
                row_resultado.append(i.encode('utf-8'))

            else:
                row_resultado.append(str(i or '')) #.decode('utf-8'))
                
        self.w_csv.writerow(row_resultado)
    
    def read(self, encoding=None):
        """
        Devuelve el contenido del fichero CSV en forma de cadena codificado
        según el parámetro 'encoding' (por defecto 'iso-8859-1')
        
        IN
          encoding <str> => 'iso-8859-1'
          
        OUT
          <str>
        """
        
        if not encoding:
            encoding = 'iso-8859-1'
        
        self.fichero_csv.seek(0)
        resultado = self.fichero_csv.read().decode('utf-8').encode(encoding)
        #resultado = self.fichero_csv.read()
        
        return resultado
    
    def __del__(self):
        self.fichero_csv.close()