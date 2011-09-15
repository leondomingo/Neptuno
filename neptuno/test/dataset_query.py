# -*- coding: utf-8 -*-

from neptuno.conexion import Conexion
from neptuno.const_datos_neptuno import CONF_DB, CONF_HOST, CONF_PASSW,\
    CONF_USER
from neptuno.dataset import DataSet
from neptuno.util import default_fmt_float

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query
DeclarativeBase = declarative_base()

class Cursos(DeclarativeBase):
    
    __tablename__ = 'cursos'
    
    id = sa.Column(sa.Integer, primary_key=True)
    nombre = sa.Column(sa.Unicode(100))
    
class Grupos(DeclarativeBase):
    
    __tablename__ = 'grupos'
    
    id = sa.Column(sa.Integer, primary_key=True)
    nombre = sa.Column(sa.Unicode(100))
    fecha_inicio = sa.Column(sa.Date)
    horas_de_clase = sa.Column(sa.Numeric(7, 2))
    
    id_curso = sa.Column(sa.Integer, sa.ForeignKey('cursos.id'))

if __name__ == '__main__':
    
    cfg = {CONF_DB: 'lanser_sapns',
           CONF_HOST: 'localhost',
           CONF_USER: 'postgres',
           CONF_PASSW: '5390post'}
    
    conn = Conexion(config=cfg)
    dbs = conn.session
    
    q = Query([Grupos.id, Grupos.nombre, Grupos.fecha_inicio, 
               Grupos.horas_de_clase, 
               Cursos.nombre]).\
            join(Cursos)
            
    cols = [('grupos_id', 'id', ''),
            ('grupos_nombre', 'Nombre', ''),
            ('grupos_fecha_inicio', 'Fecha', 'date'),
            ('grupos_horas_de_clase', 'Horas de clase', ''),
            ('cursos_nombre', 'Curso', ''),
            ]
            
    ds = DataSet.query(dbs, q, cols=cols, limit=2) #, limit, pos, show_ids)
    for row in ds.to_data():
        print row
        
    print ds.count
    
    ds = DataSet.query(dbs, dbs.query(Grupos).order_by(Grupos.id), 
                       cols=[('id', 'id', ''),
                             ('nombre', 'Nombre', '')],
                       limit=10)
    #print ds
    print ds[0]
    print ds[1]
    print ds.count
    
    def pagination(rp, pag_n, total):
        
        # total number of pages
        pos = (pag_n-1)*(rp or 0)
        total_pag = 1
        if rp > 0:
            total_pag = total/rp
            
            if total % rp != 0:
                total_pag += 1
            
            if total_pag == 0:
                total_pag = 1
        
        # rows in this page
        this_page = total - pos
        if rp and this_page > rp:
            this_page = rp
            
        return (this_page, total_pag,)
    
    print pagination(ds.limite_resultados, 2, ds.count)