# -*- coding: utf-8 -*-

import simplejson as sj
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE, LANGUAGE
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.util import get_param, EFaltaParametro
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.const_datos_neptuno import STATUS, MESSAGE, EXPIRATION
from libpy.excepciones.loginneptuno import ELoginIncorrecto,\
    EContrasenaIncorrecta
ln = load_module(IMPLEMENTATION_TYPE, 'loginneptuno', 'loginNeptuno')
loginNeptuno = ln.loginNeptuno
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
from mod_python import apache
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.log import NeptunoLogger

try:
    from nucleo.messages import Messages
    msg = Messages(LANGUAGE)
    
except ImportError:
    from libpy.messages import MessagesNeptuno
    msg = MessagesNeptuno(LANGUAGE)

def compruebasesion(req):
    """
    Comprueba la sesión del usuario.
    
    IN
      id         <int>
      challenge  <str>
      
    OUT
      {
       "status":  <bool>,
       "message": <str>
      }
    """
    
    logger = NeptunoLogger.get_logger('sw.users/compruebasesion')
    try:
        id_usuario = get_param(req.form, 'id', int)
        id_sesion = get_param(req.form, 'challenge', str)
            
        loginNep = loginNeptuno(Conexion())    
        loginNep.check_sesion(id_usuario, id_sesion)
        
        return sj.dumps({STATUS: True})
        
    except EFaltaParametro, e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    
    except (SesionIncorrecta, NoExisteUsuario,), e:
        logger.error(e)
        return sj.dumps({STATUS: False,
                         EXPIRATION: True})
    
    except Exception, e:
        logger.error(e)
        return sj.dumps({STATUS: False,
                         MESSAGE: msg.getErrorGeneral()})
    
def login(req):
    """    
    Servicio web de login de usuario
    
    IN
      login     <str>
      password  <str>
      
    OUT
      {
       "status":    <bool>
       "id":        <int>,
       "nombre":    <str>,
       "rol":       <str>,
       "challenge": <str>
       # otros campos (según el proyecto)
      }
    """
    
    logger = NeptunoLogger.get_logger('sw.users/login')
    try:
        user_login = get_param(req.form, 'login', str)
        user_password = get_param(req.form, 'password', str)        
        ip_cliente = req.get_remote_host(apache.REMOTE_NOLOOKUP)
        
        user = loginNeptuno(Conexion()).\
                    login(Usuarios, user_login, user_password, ip_cliente)
                    
        user[STATUS] = True
    
        return sj.dumps(user)

    except EFaltaParametro, e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN 

    except (ELoginIncorrecto, NoExisteUsuario, EContrasenaIncorrecta,), e:
        logger.error(e)
        return sj.dumps({STATUS: False,
                         MESSAGE: msg.getLoginIncorrecto()})
    
    except Exception, e:
        logger.error(e)
        return sj.dumps({STATUS: False,
                         MESSAGE: msg.getErrorGeneral()})

def cerrarsesion(req):    
    """
    Destruye la sesión de usuario.
    
    IN
      id_usuario  <int>
      id_sesion   <str>
      
    OUT
      {
       "status":  <bool>,
       "message": <str>
      }
    """
    
    logger = NeptunoLogger.get_logger('sw.users/cerrarsesion')
    try:
        id_usuario = get_param(req.form, 'id_usuario', int) 
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        logger.debug('Cerrando sesión (%d %s)' % (id_usuario, id_sesion))
            
        sesion_borrada = loginNeptuno(Conexion()).\
                            delelete_sesion(id_usuario, id_sesion)
                            
        return sj.dumps({STATUS: sesion_borrada})
    
    except EFaltaParametro, e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    
    except NoExisteUsuario, e:
        logger.error(e)
        return sj.dumps({STATUS: False,
                         MESSAGE: msg.getNoExisteUsuario()})
        
    except Exception, e:
        logger.error(e)
        return sj.dumps({STATUS: False,
                         MESSAGE: msg.getErrorGeneral()})
    
#def actualizarpassword(req):
#    """
#    Actualiza el login y/o la password del usuario registrado.
#    
#    IN
#      id_usuario <int>
#      id_sesion <str>
#      new_login <str>
#      old_password <str>
#      new_password <str>
#      
#    OUT
#      {'login': <str>}
#      
#    EXC
#      HTTP_FORBIDDEN
#        Falta algún parámetro de entrada
#        Sesión y/o usuario son incorrectos
#      
#      HTTP_NOT_ACCEPTABLE
#        Contraseña "old" no es correcta
#    """
#    
#    logger = NeptunoLogger.get_logger('sw.users/actualizarpassword')
#    try:
#        # comprobar usuario/sesión
#        id_usuario = get_param(req.form, 'id_usuario', int)
#        id_sesion = get_param(req.form, 'id_sesion', str)
#        
#        conector = Conexion()
#        user = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
#
#        # recoger parámetros
#        new_login = get_param(req.form, 'new_login', str)
#        old_password = get_param(req.form, 'old_password', str)
#        new_password = get_param(req.form, 'new_password', str) 
#        
#        if old_password != user.contrasenya:
#            raise EContrasenaIncorrecta
#        
#        user.actualizar_login(conector, new_login)        
#        user.actualizar_password(conector, new_password)
#        
#        return simplejson.dumps(dict(login=user.nombre_usuario))
#    
#    except EContrasenaIncorrecta, e:
#        logger.error(e)
#        raise apache.SERVER_RETURN, apache.HTTP_NOT_ACCEPTABLE
#    
#    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
#        logger.error(e)
#        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
