# -*- coding: utf-8 -*-

import datetime as dt
from neptuno.dataset import DataSet
#from neptuno.util import strtodate

if __name__ == '__main__':
    
    columnas = [(u'uno', u'Uno', 'int',),
                (u'dos', u'Dos', 'float',),
                (u'fecha', u'Fecha', 'date'),
                (u'hora', u'Hora', 'time'),
                ]
    
    ds = DataSet(columnas, 
                 date_fmt='%m.%Y',
                 int_fmt='%6.6d',
                 int_fmt_=lambda i: '%6.6d' % (i*100),  
                 float_fmt='%1.1f', 
                 float_fmt_=lambda f: '%5.5f' % f)
    
    #print strtodate('2011-12-31', fmt='%Y-%m-%d')
    
    ds.append(dato=dict(uno=123, dos=2.2345, fecha=dt.date.today(),
                        hora=dt.datetime.now().time()))
    
    #print '\nto_str()'
    #print ds.to_str(width=20, fit_width=False)
    
    #print ds.to_data()
    
    ds.to_xls('Pruebas', file('/home/leon/prueba.xls', 'wb'),
              fmt=dict(date='dd/mm/yyyy', time='HH:MM:SS'))