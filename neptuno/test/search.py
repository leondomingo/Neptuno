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
    
    ds = search(conn.session, 'vista_busqueda_grupos', rp=0, strtodatef=f,
                q='iber',
#                filters=[('id_clientes_propietario', 474,),
#                         #('Fecha inicio', dt.date(2010, 1, 1),),
#                         #('id', 35,),
#                         ],
                collection=('grupos', 'id_cursos_cursodelgrupo', 22)
                #q='fechai = 15/10/2009'
                #q='fechai >= 1/15/2011, +fechai'
                )
    #print ds
    #print 'Nº de registros: %d' % ds.count
    
    meta = sa.MetaData(bind=conn.engine)
    tbl_alu = sa.Table('alumnos', meta, autoload=True)
    tbl_aeg = sa.Table('alumnos_en_grupos', meta, autoload=True)
    
    qry = tbl_alu.\
        join(tbl_aeg,
             tbl_aeg.c.id_alumnos_alumno == tbl_alu.c.id)
        
    # condiciones
    where_ = sa.and_(tbl_alu.c.nombre.like('A%'),
                     tbl_alu.c.apellido1.like('A%'),
                     tbl_alu.c.e_mail != None,
                     tbl_alu.c.apellido2 != None,
                    )
    
    order_ = (tbl_alu.c.e_mail,)
        
    sel = sa.select([(tbl_alu.c.apellido1 + ', ' + tbl_alu.c.nombre).label('nombre_completo'),
                     tbl_alu], from_obj=qry, 
                    whereclause=where_).order_by(*order_)
                    
    print dir(sel)
    print sel.columns
    print sel.columns['nombre_completo'].type
    print sel.columns['nombre'].type
                    
    ds = DataSet.procesar_resultado(conn.session, sel)
    print ds