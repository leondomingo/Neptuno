# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.postgres.search import search
from neptuno.util import strtodate

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser-sapns',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    #print type(conn.session)
    
    def f(s):
        return strtodate(s, fmt='%m/%d/%Y', no_exc=True)
    
    ds = search(conn.session, 'vista_busqueda_cursos', rp=0, strtodatef=f,
                q='fechai >= 1/15/2011, +fechai')
    print ds
    print ds.count    