# -*- coding: utf-8 -*-

import simplejson
import cherrypy
from nucleo.config import IMPLEMENTATION_TYPE 
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.util import get_paramw, EFaltaParametro
from libpy.excepciones.eneptuno import SesionIncorrecta
ln = load_module(IMPLEMENTATION_TYPE, 'loginneptuno', 'loginNeptuno')
loginNeptuno = ln.loginNeptuno
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
from libpy.excepciones.loginneptuno import EGenerandoSesion, EGenerandoSalt,\
    EContrasenaIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.conexion import Conexion
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('wsgi.checkuser')

class User(object):
    
    @cherrypy.expose
    def index(self):
        return 'CheckUser'
    
    @cherrypy.expose
    def compruebasesion(self, **params):    
        """Servicio web de login de usuario"""
 
        try:
            id_usuario = get_paramw(params, 'id', int)
            id_sesion = get_paramw(params, 'challenge', str)
            
            loginNep = loginNeptuno(Conexion())    
            sesion_correcta = loginNep.check_sesion(id_usuario, id_sesion)
            
            return simplejson.dumps(sesion_correcta)
        
        except (EFaltaParametro, NoExisteUsuario), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)        

    @cherrypy.expose
    def login(self, **params):
        """    
        Servicio web de login de usuario
        
        IN
          login    <str>
          password <str>
          
        OUT
          {"id": <int>,
           "nombre": <str>,
           "rol": <str>,
           "challenge": <str>
           # otros campos (según el proyecto)
          }
        """
        
        try:
            login = get_paramw(params, 'login', str)
            password = get_paramw(params, 'password', str)
            ip_cliente = cherrypy.request.headers.get('Remote-Addr', '127.0.0.1')

            loginNep = loginNeptuno(Conexion())    

            user = loginNep.check_login(Usuarios, login, password, ip_cliente)
        
            return simplejson.dumps(user)
            
        except (EFaltaParametro, EGenerandoSesion, EGenerandoSalt, 
                EContrasenaIncorrecta, NoExisteUsuario), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)
    
    @cherrypy.expose
    def cerrarsesion(self, **params):    
        """
        Destruye la sesión del usuario
        IN
          id_usuario <int>
          id_sesion <str>
          
        OUT
          {"resultado": <bool>}
        """
        
        try:
            id_usuario = get_paramw(params, 'id_usuario', int)
            id_sesion = get_paramw(params, 'id_sesion', str)
        
            loginNep = loginNeptuno(Conexion())
            
            sesion_borrada = loginNep.delelete_sesion(id_usuario, id_sesion)
            return simplejson.dumps(dict(resultado=sesion_borrada))
        
        except NoExisteUsuario, e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)
    
    @cherrypy.expose
    def actualizarpassword(self, **params):
        """
        Actualiza el login y/o la password del usuario registrado.
        
        IN
          id_usuario <int>
          id_sesion <str>
          new_login <str>
          old_password <str>
          new_password <str>
          
        OUT
          {'login': <str>}
          
        EXC
          HTTP_FORBIDDEN
        """
        
        try:
            id_usuario = get_paramw(params, 'id_usuario', int)
            id_sesion = get_paramw(params, 'id_sesion', str)
            new_login = get_paramw(params, 'new_login', str)
            old_password = get_paramw(params, 'old_password', str)
            new_password = get_paramw(params, 'new_password', str) 
            
            conector = Conexion()    

            user = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
            if old_password != user.contrasenya:
                raise EContrasenaIncorrecta
            
            user.actualizar_login(conector, new_login)        
            user.actualizar_password(conector, new_password)
            
            return simplejson.dumps(dict(login=user.nombre_usuario))

        except (EContrasenaIncorrecta, EFaltaParametro, NoExisteUsuario, 
                SesionIncorrecta), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)