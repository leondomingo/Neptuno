# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.dataset import DataSet
import datetime as dt

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser-sapns',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    
    columnas = [('uno', u'Uno', '',),
                ('dos', u'Dos', '',),
                ('tres', u'Unicode: á è ï ŧ', '',),
                ]
    
    ds = DataSet(columnas)
    ds.time_fmt = '%H:%M:%S'
    
    ds.append(dato=dict(uno=1, dos='2', tres=u'León Domingo Ortín'))
    ds.append(dato=dict(uno=u'Más unicode: á é', dos=True, tres=123L))
    ds.append(dato=dict(uno=dt.date.today(), dos=dt.time(10, 30, 25), tres=dt.datetime.now()))
    ds.append(dato=dict(tres=3.3))
    
    print '\nto_str()'
    print ds.to_str(width=20, fit_width=False)
    
    print '\nlabels'
    print ds.labels
    
    print '\nto_data()'
    print ds.to_data()
    
    print '\nCSV'
    print ds.to_csv()