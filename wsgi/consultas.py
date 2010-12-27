# -*- coding: utf-8 -*-

import cherrypy
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.neptunofactory import get_claseusuarios, load_module
from libpy.util import get_param, get_paramw, EFaltaParametro
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('wsgi.consultas')
import simplejson
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
mod_lanzarconsulta = load_module(IMPLEMENTATION_TYPE, 'lanzarconsulta', 'lanzar_consulta')
lanzar_consulta = mod_lanzarconsulta.lanzar_consulta

class ConsultasOlympo(object):

    @cherrypy.expose
    def lanzarconsulta(self, **params):    
        """
        Lanza un informe de Olympo y devuelve el resultado.
        
        IN
          id_usuario     <int>
          id_sesion      <str>
          cod_consulta   <int>
          nombreinforme  <str>
          parametros     <list> 
            Una lista de la forma: [{"nombre": <str>, "valor": <str>}, ...] (opcional)
          time_out       <int> (en segundos) (opcional)
          
        OUT
          (contenido del PDF de la consulta)
          
        EXC
          FORBIDDEN
        """
        
        try:
            id_usuario = get_paramw(params, 'id_usuario', int)
            id_sesion = get_paramw(params, 'id_sesion', str)
            
            cod_consulta = get_paramw(params, 'cod_consulta', int)
            nombreinforme = get_param(params, 'nombreinforme', str)
        #    tipo_fichero = get_paramw(params, 'tipo_fichero', str, opcional=True,
        #                              por_defecto='pdf')
        
            parametros = get_paramw(params, 'parametros', simplejson.loads, 
                                    opcional=True)
            
            time_out = get_paramw(params, 'time_out', int, opcional=True)    
            
            conector = Conexion()    
            user = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
            
            return lanzar_consulta(cod_usuario=user.id_usuarios_usuarioperfil,
                                   servidor=conector.conexion.datosconexion.BaseDatos,
                                   base=conector.conexion.datosconexion.Host,
                                   cod_consulta=cod_consulta,
                                   nombreinforme=nombreinforme,
                                   parametros=parametros,
                                   tipo_fichero='pdf',
                                   time_out=time_out)
            
        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)