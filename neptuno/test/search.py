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
#    tbl_alu = sa.Table('alumnos', meta, autoload=True)
#    tbl_aeg = sa.Table('alumnos_en_grupos', meta, autoload=True)
#    
#    qry = tbl_alu.\
#        join(tbl_aeg,
#             tbl_aeg.c.id_alumnos_alumno == tbl_alu.c.id)
#        
#    sel = sa.select([tbl_alu.c.nombre.label('nombre'),
#                     tbl_alu.c.apellido1.label('apellido1'),
#                     tbl_alu.c.apellido2.label('apellido2'),
#                     tbl_alu.c.e_mail.label('e_mail'),
#                     ], from_obj=qry, whereclause=tbl_alu.c.nombre.like('R%')) 
#                    
##    print type(sel)
##    print dir(sel)
##    print sel.columns
##    print dir(sel.columns['nombre_completo'])
##    print str(sel.columns['nombre_completo'].scalar)
##    print sel.columns['nombre_completo'].type
##    print sel.columns['nombre'].type
#
    ds = search(conn.session, 'vista_busqueda_alumnos', q='+nombrec, raul', rp=5)
    print ds
#                    
#    ds = search(conn.session, sel, q='+email, raul', rp=5)
#    print ds
    
    tbl_doc = sa.Table('sp_docs', meta, autoload=True)
    tbl_doct = sa.Table('sp_doctypes', meta, autoload=True)
    tbl_docf = sa.Table('sp_docformats', meta, autoload=True)
    tbl_adoc = sa.Table('sp_assigned_docs', meta, autoload=True)
    tbl_repo = sa.Table('sp_repos', meta, autoload=True)
    tbl_usr = sa.Table('sp_users', meta, autoload=True)
    
    qry = tbl_doc.\
        join(tbl_adoc, tbl_adoc.c.id == tbl_doc.c.id).\
        outerjoin(tbl_doct, tbl_doct.c.id == tbl_doc.c.id_doctype).\
        join(tbl_docf, tbl_docf.c.id == tbl_doc.c.id_docformat).\
        join(tbl_usr, tbl_usr.c.id == tbl_doc.c.id_author).\
        join(tbl_repo, tbl_repo.c.id == tbl_doc.c.id_repo)
        
    sel = sa.select([tbl_doc.c.id,
                     tbl_doc.c.title.label('title'),
                     tbl_docf.c.name.label('format'),
                     (tbl_docf.c.name + tbl_doct.c.name).label('format_type'),
                     tbl_doct.c.name.label('type'),
                     tbl_usr.c.display_name.label('author'),
                     tbl_repo.c.name.label('repo'),
                     ], from_obj=qry, #use_labels=True,
                    whereclause=sa.and_(tbl_adoc.c.id_class == 26,
                                        tbl_adoc.c.object_id == 1,
                                        ))
    
    #print type(sel.columns['format'])
    #print sel.columns['format'].collate()
    #print help(sel.columns['format'].collate)
    format_type = sel.columns['format_type'].base_columns.pop()
    #print dir(format_type)
    #print format_type.anon_label
    #format_ = sel.columns['format'].base_columns.pop()
    #print sel.columns['format_type'].base_columns.pop().type
    
    #sel = sel.where(format_.like('E%'))

    doclist = search(conn.session, sel)
    print doclist
