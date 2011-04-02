# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.postgres.search import search

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    #print type(conn.session)
    
    ds = search(conn.session, 'vista_busqueda_personal', rp=0)
    print ds
    print ds.count    