# -*- coding: utf-8 -*-

import sqlalchemy as sa
from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.postgres.search import Search
from neptuno.util import strtodate

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'kleinson',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    dbs = conn.session
    
    def f(s):
        return strtodate(s, fmt='%d/%m/%Y', no_exc=True)
    
    s = Search(dbs, '_view_grupos', strtodatef=f)
    s.and_(sa.func.tiene_clases(s.tbl.c.id, 1288))

    ds = s()
    print ds
    #print ds.count
    
    s = Search(dbs, 'sp_attributes')
    s.apply_qry('')
    print s(collection=('sp_attributes', 'id_class', 10))
