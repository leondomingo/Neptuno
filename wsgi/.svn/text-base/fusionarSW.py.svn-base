# -*- coding: utf-8 -*-

import cherrypy
import simplejson
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.util import get_paramw, EFaltaParametro
from wsgi.base import NeptunoBase
fs = load_module(IMPLEMENTATION_TYPE, 'fusionar', 'merge')
merge = fs.merge
from libpy.excepciones.eneptuno import ENoExisteRegistro, SesionIncorrecta
from libpy.excepciones.eneptuno import NoTienePrivilegiosEscritura
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('wsgi.fusionarSW')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

class Fusionar(NeptunoBase):

    @cherrypy.expose
    def default(self, **params):
        """
        Nombre:
            fusionarSW.py
        
        Descripción:
            Fusiona dos registros de una tabla 'nombre_tabla', borrando uno de ellos al final del proceso.
    
        IN
          nombre_tabla: Nombre de la tabla a la que pertenecen los registros (alumnos, clientes, etc)
          id_destino: Identificador del registro "destino" donde se copiarán todos los datos.
          id_origen: Identificador del registro "origen" desde donde se copiarán todos los datos.            
          id_usuario: Id de usuario
          id_sesion: Id de sesión.
            
        OUT
          Un json de la forma :
          {
           'id_destino': <int>,
           'id_origen': <int>,
           'num_campos': <int>
          }
            
        EXC
          FORBIDDEN
        """
        
        try:
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)

            # recoger parámetros
            nombre_tabla = get_paramw(params, 'nombre_tabla', str)
            id_destino = get_paramw(params, 'id_destino', int)
            id_origen = get_paramw(params, 'id_origen', int)
            
            mezcla = merge(nombre_tabla, id_destino, otros_ids=[id_origen],
                           conector=conector)
            
            return simplejson.dumps(mezcla)
            
        except (EFaltaParametro, SesionIncorrecta, NoExisteUsuario, 
                ENoExisteRegistro, NoTienePrivilegiosEscritura), e:
            # FORBIDDEN
            logger.error(e)
            raise cherrypy.HTTPError(403)
