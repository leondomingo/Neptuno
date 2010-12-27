# -*- coding: utf-8 -*-

import cherrypy
import simplejson
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.util import EFaltaParametro, get_paramw
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.guardarRegistro')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
gr = load_module(IMPLEMENTATION_TYPE, 'guardarRegistro', 'save')
save = gr.save

class GuardarRegistro(NeptunoBase):

    @cherrypy.expose
    def default(self, **params):
        """
        Guardar datos de una tabla.
        
        IN
          id_usuario <int>
          id_sesion  <str>
          tabla      <str>
          datos      {<campo1>: <valor1>, <campo2>: <valor2>, ...}
          
        OUT
          <int>
        """
        
        try:
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)
            
            id_usuario = get_paramw(params, 'id_usuario', int)
    
            # recoger parámetros
            tabla = get_paramw(params, 'tabla', str)    
            datos = get_paramw(params, 'datos', simplejson.loads)
    
            # guardar registro
            id_registro = save(tabla, id_usuario, datos, conector=conector)
            return str(id_registro)
            
        except (NoExisteUsuario, SesionIncorrecta, EFaltaParametro), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)

