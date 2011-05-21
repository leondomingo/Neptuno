# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.postgres.search import search

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'tandem',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    
    ds = search(conn.session, 'vista_busqueda_alumnos', rp=0, show_ids=True)
    print ds.labels
    print ds.cols
    print ds.types
    ds.to_xls('Esto es una prueba', '/home/leon/dataset.xls')
