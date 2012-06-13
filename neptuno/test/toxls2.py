# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW, \
    CONF_USER
from neptuno.postgres.search import search

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    
    ds_grupos = search(conn.session, '_view_grupos', q='fechaf<01/07/2012')
    #print zip(ds_grupos.labels, ds_grupos.types)
    
    with open('/home/leon/grupos.xml', 'wb') as f:
        xml = ds_grupos.to_xls('Grupos', '/home/leon/grupos.xls')
        f.write(xml)