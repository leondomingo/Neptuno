# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW, \
    CONF_USER
from neptuno.dataset import DataSet
from sqlalchemy import MetaData, Table

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'ihmadrid__11722',
           CONF_HOST: 'localhost:5433',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    
    meta = MetaData(bind=conn.engine)
    series = Table('sp_updates', meta, autoload=True)
    
    ds = DataSet.procesar_resultado(conn.session, series.select())
    print ds.to_data()