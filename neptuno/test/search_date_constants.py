# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW, \
    CONF_USER
from neptuno.postgres.search import Search
from neptuno.util import strtodate
import sqlalchemy as sa

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'ihmadrid__20130419',
           CONF_HOST: 'localhost:5433',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    dbs = conn.session
    
    def f(s):
        return strtodate(s, fmt='%m/%d/%Y', no_exc=True)
    
    meta = sa.MetaData(bind=conn.engine)
    s = Search(dbs, 'calendarios')
    
    s.apply_qry('fecha >= {start_month - 3m}, fecha <= {end_month - 3m}')
    print s.sql
    
    ds = s(rp=10)
    for data in ds.to_data():
        print data
