# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW, \
    CONF_USER
from neptuno.postgres.search import search, Search
from neptuno.util import strtodate
import sqlalchemy as sa

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    dbs = conn.session
    
    def f(s):
        return strtodate(s, fmt='%m/%d/%Y', no_exc=True)
    
    meta = sa.MetaData(bind=conn.engine)
    s = Search(dbs, '_view_alumnos')
    
    s.apply_qry('prueba')
    
    ds = s(rp=5)
    print ds
    
    ds = search(conn.session, 'sp_attributes', q='name=descript', 
                collection=('sp_attributes', 'id_class', 7))
    print ds
    
    s2 = Search(dbs, 'sp_attributes')
    ds2 = s2(collection=('sp_attributes', 'id_class', 7))
    print ds2
    
    s3 = Search(dbs, '_view_alumnos')
    s3.apply_qry('+nombre')
    ds3 = s3(collection=('alumnos', 'id_cliente_actual', 480))
    print ds3