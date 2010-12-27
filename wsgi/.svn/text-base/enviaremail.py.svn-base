# -*- coding: utf-8 -*-

import cherrypy
from libpy.enviaremail import enviar_email
import simplejson
from libpy.util import EFaltaParametro, get_paramw
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.neptunofactory import get_claseusuarios
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.enviaremail')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

class EnviarEmail(NeptunoBase):

    @cherrypy.expose
    def default(self, **params):
        """
        IN
          id_usuario     <int>
          id_sesion      <str>
          remitente      <list> => [<email>, <nombre>]
          destinatarios  <list> => [[<email1>, <nombre1>], [<email2>, <nombre2>], ...]'
          asunto         <str>
          mensaje        <str>
          servidor       <str>
          login          <str>
          password       <str>
        """

        try:
            # comprobar usuario/sesión
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)
            
            # recoger parámetros
            remitente = get_paramw(params, 'remitente', simplejson.loads)
            destinatarios = get_paramw(params, 'destinatarios', simplejson.loads)            
            asunto = get_paramw(params, 'asunto', str)
            mensaje = get_paramw(params, 'mensaje', str)
            servidor = get_paramw(params, 'servidor', str)
            login = get_paramw(params, 'login', str)
            password = get_paramw(params, 'password', str)

            # enviar e-mail            
            r = enviar_email(remitente, destinatarios, asunto, mensaje, servidor, 
                             login, password)
            return simplejson.dumps(r)
            
        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)