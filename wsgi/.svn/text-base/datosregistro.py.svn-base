# -*- coding: utf-8 -*-

import simplejson
import cherrypy
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.util import EFaltaParametro, get_paramw, get_paramsw
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.datosregistro')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
dr = load_module(IMPLEMENTATION_TYPE, 'datosRegistro', ['record_data', 'raw_data'])
record_data = dr.record_data
raw_data = dr.raw_data

class DatosRegistro(NeptunoBase):
    
    _cp_config = {'tools.gzip.on': True}
    
    @cherrypy.expose
    def default(self, **params):
        """
        IN
          id_usuario <int>
          id_sesion  <str>
          tabla      <str>
          id         <int>
          # campos predefinidos
          
        OUT
          Un JSON de la forma:
            [{campo1}, {campo2}, ...]
                
          Cada "campoX", a su vez, tiene la forma:
          campo = {
                   "nombre":            <str>,
                   "tipo":              <str>,
                   "valor":             <str>,
                   "etiqueta":          <str>,
                   "requerido":         <bool>
                   "solo_lectura":      <bool>,
                   "tabla_relacionada": <str>,
                   "utilizar_selector": <bool>,
                   "valores":           [[{campo}, ...], ...]
                  }
        """
        
        try:
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)
            id_usuario = get_paramw(params, 'id_usuario', int)
            
            tabla = get_paramw(params, 'tabla', str)
            id_registro = get_paramw(params, 'id', int)
            
            # campos "predefinidos"
            campos_pre = get_paramsw(params, ['id_usuario', 'id_sesion', 'tabla', 'id'])
                    
            registro = record_data(id_usuario, tabla, id_registro, conector=conector, 
                                   **campos_pre)
            
            return simplejson.dumps(registro, encoding='utf8')
            
        except (NoExisteUsuario, SesionIncorrecta, EFaltaParametro), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)
        
    @cherrypy.expose
    def raw(self, **params):
        """
        IN
          id_usuario <int>
          id_sesion  <str>
          tabla      <str>
          id         <int>
          campos     [<str>, ...] (opcional)
          
        OUT
          Un JSON de la forma:
            {<nombre1>: <valor1>, <nombre2>:<valor2>, ...}
        """
        
        try:
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)
            
            tabla = get_paramw(params, 'tabla', str)
            id_registro = get_paramw(params, 'id', int)
            campos = get_paramw(params, 'campos', simplejson.loads, 
                                opcional=True)

            registro = raw_data(tabla, id_registro, campos, conn=conector)
            
            return simplejson.dumps(registro, encoding='utf8')
            
        except (NoExisteUsuario, SesionIncorrecta, EFaltaParametro), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)