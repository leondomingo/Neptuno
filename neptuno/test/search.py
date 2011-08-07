# -*- coding: utf-8 -*-

import sqlalchemy as sa
import datetime as dt
from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.postgres.search import search
from neptuno.util import strtodate
from neptuno.dataset import DataSet

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser-sapns',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    #print type(conn.session)
    
    def f(s):
        return strtodate(s, fmt='%m/%d/%Y', no_exc=True)
    
    meta = sa.MetaData(bind=conn.engine)
    tbl_alu = sa.Table('alumnos', meta, autoload=True)
    tbl_aeg = sa.Table('alumnos_en_grupos', meta, autoload=True)
    
    qry = tbl_alu.\
        join(tbl_aeg,
             tbl_aeg.c.id_alumnos_alumno == tbl_alu.c.id)
        
    sel = sa.select([tbl_alu.c.nombre.label('nombre'),
                     tbl_alu.c.apellido1.label('apellido1'),
                     tbl_alu.c.apellido2.label('apellido2'),
                     tbl_alu.c.e_mail.label('e_mail'),
                     ], from_obj=qry, whereclause=tbl_alu.c.nombre.like('R%')) 
                    
#    print type(sel)
#    print dir(sel)
#    print sel.columns
#    print dir(sel.columns['nombre_completo'])
#    print str(sel.columns['nombre_completo'].scalar)
#    print sel.columns['nombre_completo'].type
#    print sel.columns['nombre'].type

    ds = search(conn.session, 'alumnos', q='+apellido1', rp=5)
    print ds
                    
    ds = search(conn.session, sel, q='+apellido1', rp=5)
    print ds