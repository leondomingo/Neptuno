# -*- coding: utf-8 -*-

from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.util import get_param, EFaltaParametro
from libpy.excepciones.eneptuno import SesionIncorrecta
ln = load_module(IMPLEMENTATION_TYPE, 'loginneptuno', 'loginNeptuno')
loginNeptuno = ln.loginNeptuno
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
from mod_python import apache
from libpy.excepciones.loginneptuno import EGenerandoSesion, EGenerandoSalt,\
    EContrasenaIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
import simplejson
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.checkuser')

def compruebasesion(req):    
    """
    Comprueba la sesión del usuario.
    
    IN
      id         <int>
      challenge  <str>
      
    OUT
      <bool>
    """

    try:
        id_usuario = get_param(req.form, 'id', int)
        id_sesion = get_param(req.form, 'challenge', str)
            
        loginNep = loginNeptuno(Conexion())    
        return loginNep.check_sesion(id_usuario, id_sesion)
        
    except (EFaltaParametro, NoExisteUsuario), e:
        logger.debug('compruebasesion')
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    
def checksession(req):
    """
    Comprueba la sesión del usuario.
    
    IN
      id_usuario  <int>
      id_sesion   <str>
      
    OUT
      {
       "status": <bool>
      }
    """
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        r = loginNeptuno(Conexion()).check_sesion(id_usuario, id_sesion)
        
        return simplejson.dumps(dict(status=r)) 
        
    except (EFaltaParametro), e:
        logger.debug('checksession')
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN

def login(req):
    """    
    Servicio web de login de usuario
    
    IN
      login    <str>
      password <str>
      
    OUT
      {
       "id":        <int>,
       "nombre":    <str>,
       "rol":       <str>,
       "challenge": <str>
       # otros campos (según el proyecto)
      }
    """
    
    try:
        user_login = get_param(req.form, 'login', str)
        user_password = get_param(req.form, 'password', str)        
        ip_cliente = req.get_remote_host(apache.REMOTE_NOLOOKUP)
        
        user = loginNeptuno(Conexion()).\
                    login(Usuarios, user_login, user_password, ip_cliente)
    
        return simplejson.dumps(user)
        
    except (EFaltaParametro, EGenerandoSesion, EGenerandoSalt, 
            EContrasenaIncorrecta, NoExisteUsuario), e:
        logger.debug('login')
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN

def cerrarsesion(req):    
    """
    Destruye la sesión del usuario
    IN
      id_usuario <int>
      id_sesion <str>
      
    OUT
      {"resultado": <bool>}
    """

    try:
        id_usuario = get_param(req.form, 'id_usuario', int) 
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        logger.debug('Cerrando sesión (%d %s)' % (id_usuario, id_sesion))
            
        sesion_borrada = loginNeptuno(Conexion()).\
                            delelete_sesion(id_usuario, id_sesion)
        return simplejson.dumps(dict(resultado=sesion_borrada))
    
    except (EFaltaParametro, NoExisteUsuario), e:
        logger.debug('cerrarsesión')
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    
def actualizarpassword(req):
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
        Falta algún parámetro de entrada
        Sesión y/o usuario son incorrectos
      
      HTTP_NOT_ACCEPTABLE
        Contraseña "old" no es correcta
    """
    
    try:
        # comprobar usuario/sesión
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        conector = Conexion()
        user = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)

        # recoger parámetros
        new_login = get_param(req.form, 'new_login', str)
        old_password = get_param(req.form, 'old_password', str)
        new_password = get_param(req.form, 'new_password', str) 
        
        if old_password != user.contrasenya:
            raise EContrasenaIncorrecta
        
        user.actualizar_login(conector, new_login)        
        user.actualizar_password(conector, new_password)
        
        return simplejson.dumps(dict(login=user.nombre_usuario))
    
    except EContrasenaIncorrecta, e:
        logger.debug('actualizarpassword')
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_NOT_ACCEPTABLE
    
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
        logger.debug('actualizarpassword')
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
