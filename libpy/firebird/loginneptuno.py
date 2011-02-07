# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import and_, func
from datetime import datetime, timedelta
from libpy.cryptoutils import CryptoUtils
from libpy.excepciones.loginneptuno import EGenerandoSesion, \
    EContrasenaIncorrecta, ELoginIncorrecto
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.conexion import Conexion
from libpy.log import NeptunoLogger
from nucleo.const_datos import SESSION_LIFE
from unidadescompartidasNeptuno import usuariosNeptuno, sesionesNeptuno 

class loginNeptuno(object):

    def __init__(self, conector=None):
        if conector != None:
            self.conector = conector
        else:
            self.conector = Conexion()    
    
    def delelete_sesion(self, id_usuario, id_sesion):
        """Borra la sesión 'id_sesion' del usuario 'id_usuario'
        
        IN
          id_usuario  <int>
          id_sesion   <str>
          
        OUT
          <bool>
          
        EXC
          NoExisteUsuario
        """
    
        user = self.conector.conexion.query(usuariosNeptuno).\
                filter_by(id=id_usuario).first()
    
        if user != None:
            sesion = \
                self.conector.conexion.query(sesionesNeptuno).\
                    filter(and_(sesionesNeptuno.id_usuariosweb_usuarioweb == id_usuario,
                                sesionesNeptuno.challenge == id_sesion)).first()

            if sesion != None:
                # identificador y usuario correctos
                try:
                    self.conector.conexion.delete(sesion)
                    self.conector.conexion.commit()
                    return True
                except:
                    self.conector.conexion.rollback
                    return False
            else:
                # El identificador de sesion no es correcto
                return False
        else:
            # No se encuentra el usuario
            raise NoExisteUsuario(str(id_usuario))        

    def check_sesion(self, id_usuario, id_sesion):
        """
        Comprueba que la sesión es correcta.
        
        IN
          id_usuario  <int>
          id_sesion   <str>
          
        OUT
          <bool>
          
        EXC
          NoExisteUsuario        
        """
        
        user = \
            self.conector.conexion.query(usuariosNeptuno).\
                filter(usuariosNeptuno.id == id_usuario).\
                first()
    
        if user != None:
            sesion = \
                self.conector.conexion.query(sesionesNeptuno).\
                    filter(and_(sesionesNeptuno.id_usuariosweb_usuarioweb == id_usuario,
                                sesionesNeptuno.challenge == id_sesion)).first()
                                                    
            return sesion != None
        else:
            # No se encuentra el usuario
            raise NoExisteUsuario(str(id_usuario))
    
    def login(self, cls, user_login, user_password, ip):
        """
        Comprueba el login en función de nombre de usuario y contraseña.
        
        IN
          user_login     <str>
          user_password  <str>
          ip             <str>
          
        OUT
          {
           "id":        <int>,
           "nombre":    <str>,
           "rol":       <str>,
           "challenge": <str>
          }
        """
        
        logger = NeptunoLogger.get_logger('(FB) loginNeptuno.login')
        try:
            user = \
                self.conector.conexion.query(cls).\
                filter(func.upper(usuariosNeptuno.nombre_usuario) == func.upper(user_login)).\
                first()
        
            if user is None:
                raise NoExisteUsuario(user_login)
                            
            if user.contrasenya != user_password:
                raise EContrasenaIncorrecta
                    
            crypto_utils = CryptoUtils()
            id_sesion = crypto_utils.cadena_aleatoria(32)
        
            # sesión
            sesion_usuario = sesionesNeptuno()
            sesion_usuario.id_usuarios_usuario = user.id_usuarios_usuarioperfil
            sesion_usuario.id_usuariosweb_usuarioweb = user.id
            sesion_usuario.challenge = id_sesion  
            sesion_usuario.direccionip = ip
            sesion_usuario.fecha_caducidad = datetime.now() + timedelta(minutes=SESSION_LIFE)
        
            self.conector.conexion.add(sesion_usuario)
            
            # actualizar 'Último login'
            user.ultimologin = datetime.now()
            
            self.conector.conexion.add(user)                        
            self.conector.conexion.flush()
            
            datos_login = user.datos_login(conector=self.conector)
            datos_login['challenge'] = id_sesion
            
            logger.debug('Login correcto de usuario "%s"' % user_login)
            
            # guardar definitivamente
            self.conector.conexion.commit()
            
            return datos_login
            
        except Exception, e:
            logger.error(e)
            raise
        