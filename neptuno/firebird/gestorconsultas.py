# -*- coding: utf-8 -*-

from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.expression import and_, select
import os
from libpy.log import NeptunoLogger
from libpy.dict import Dict
from libpy.firebird.util import nombre_tabla, nombre_coleccion, cod_atributo
from libpy.firebird.const_olympo import cl_UsuariosWeb, cl_Usuarios,\
    cl_Consultas, cons_usuarios, uswe_usuarioperfil, cons_nombre,\
    cl_ParametrosDeConsulta, pdc_consulta, pdc_nombre, pdc_valorpordefecto,\
    pdc_orden, cl_Variables, vari_rutaconsultas
from libpy.firebird.exc.excepciones import ENoExisteConsulta
from libpy.firebird.const_datos_olympo import BOOL_FALSE

class GestorConsultas(object):
    
    def __init__(self, conector):
        self.conector = conector
        self.meta = MetaData(bind=self.conector.engine)
        
    def consultas_usuario(self, id_usuario_web):
        """
        Devuelve la lista de consultas asociadas al usuario (del perfil) que 
        tiene el usuario web indicado.
        
        IN
          id_usuario_web  <int>
          
        OUT
          [{'id': <int>, 'nombre': <str>}, ...]
        """
        
        tbl_uweb = Table(nombre_tabla(cl_UsuariosWeb), self.meta, autoload=True)
        tbl_usr = Table(nombre_tabla(cl_Usuarios), self.meta, autoload=True)
        col_cons = Table(nombre_coleccion(cl_Consultas), self.meta, autoload=True)
        tbl_cons = Table(nombre_tabla(cl_Consultas), self.meta, autoload=True)
        
        logger = NeptunoLogger.get_logger('gestorconsultas/consultas_usuario')
        try:
            qry = \
                tbl_cons.\
                join(col_cons,
                     and_(tbl_cons.c.cod_objeto == col_cons.c.cod_objeto,
                          col_cons.c.cod_atributo == cod_atributo(cons_usuarios),
                          )).\
                join(tbl_usr,
                     tbl_usr.c.cod_objeto == col_cons.c.cod_objetoincluido).\
                join(tbl_uweb,
                     tbl_usr.c.cod_objeto == tbl_uweb.c[uswe_usuarioperfil])
                
            sel = select([tbl_cons.c.cod_objeto,
                          tbl_cons.c[cons_nombre].label('nombre'),
                          ],
                         from_obj=qry,
                         whereclause=tbl_uweb.c.cod_objeto == id_usuario_web)
            
            lista = []
            for cons in self.conector.conexion.\
                    execute(sel.order_by(tbl_cons.c[cons_nombre])):
                lista.append(Dict(id=cons.cod_objeto, 
                                  nombre=cons.nombre))
                
            return lista
            
        except Exception, e:
            logger.error(e)
            raise
        
    def parametros(self, id_consulta):
        """
        Devuelve la lista ordenada de parámetros de la consulta indicada. 
        IN
          id_consulta  <int>
          
        OUT
          [{"nombre": <str>, "por_defecto": <str>}, ...]
        """
        
        logger = NeptunoLogger.get_logger('gestorconsultas/parametros_consulta')
        try:
            tbl_param = Table(nombre_tabla(cl_ParametrosDeConsulta), self.meta,
                            autoload=True)
            
            params = []
            for param in self.conector.conexion.\
                    execute(select([tbl_param.c[pdc_nombre],
                                    tbl_param.c[pdc_valorpordefecto],
                                    ],
                                   from_obj=tbl_param,
                                   whereclause=tbl_param.c[pdc_consulta] == id_consulta).\
                    order_by(tbl_param.c[pdc_orden])):
                
                params.append(Dict(nombre=param[pdc_nombre],
                                   por_defecto=param[pdc_valorpordefecto] or ''
                                   ))
                
            return params

        except Exception, e:
            logger.error(e)
            raise
        
    def informes(self, cod_consulta):
        """Devuelve una lista de informes para la consulta 'cod_consulta'.
        Si la consulta no existe se lanza la excepción 'ENoExisteConsulta'"""
        
        meta = MetaData(bind=conector.engine)
        tbl_variables = Table(nombre_tabla(cl_Variables), meta, autoload=True)
        tbl_consultas = Table(nombre_tabla(cl_Consultas), meta, autoload=True)
        
        # variable
        variable = self.conector.conexion.execute(tbl_variables.select()).fetchone()
        
        # ruta consultas
        ruta_consultas = variable[vari_rutaconsultas]
        
        # consulta
        consulta = self.conector.conexion.\
                execute(tbl_consultas.\
                        select(tbl_consultas.c.cod_objeto == cod_consulta)).\
                fetchone()
                
        if consulta is None:
            raise ENoExisteConsulta(cod_consulta)
        
        # nombre
        nombre_consulta = consulta[cons_nombre].replace(' ', '_')
        
        # es RAVE o Fast Report
        extension = '.FR'
        if consulta.atr_100268 == BOOL_FALSE:
            nombre_consulta += '_RAV'
            extension = '.RAV'
            
        ruta = os.path.join(ruta_consultas, 'CONS_%s' % nombre_consulta)
        
        return [os.path.splitext(n)[0].encode('utf-8')
                for n in os.listdir(ruta) \
                if os.path.splitext(n)[1].upper().startswith(extension)]
        

if __name__ == '__main__':
    
    from libpy.conexion import Conexion
    conector = Conexion()
    
    id_uw = 10
    
    gc = GestorConsultas(conector)
    r = gc.consultas_usuario(id_uw)
    
    for cons in r:
        print cons.nombre
        for param in gc.parametros(cons.id):
            print param
    
        print