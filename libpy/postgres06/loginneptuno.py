#-*- coding: utf-8 -*-

from datetime import datetime, timedelta
from libpy.cryptoutils import SaltedHash, CryptoUtils
from libpy.excepciones.loginneptuno import EGenerandoSesion,\
    EContrasenaIncorrecta, EGenerandoSalt
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.conexion import Conexion
from nucleo.const_datos import SESSION_LIFE
from unidadescompartidasNeptuno import usuariosNeptuno, saltsNeptuno, sesionesNeptuno 

class loginNeptuno(object):

    def __init__(self, conector=None):
        if conector != None:
            self.conector = conector
        else:
            self.conector = Conexion()    
    
    def delelete_sesion(self, id_usuario, id_sesion):
    
        user = self.conector.conexion.query(usuariosNeptuno).\
                filter_by(id=id_usuario).\
                first()
    
        if user != None:
            sesion = self.conector.conexion.query(sesionesNeptuno).\
                        filter_by(id_usuarios_id=id_usuario, \
                                  challenge=id_sesion).first()        

            if sesion != None:
                # identificador y usuario correctos
                try:
                    self.conector.conexion.delete(sesion)
                    self.conector.conexion.commit()
                    return True
                except:
                    #self.conector.conexion.rollback
                    return False
            else:
                # El identificador de sesion no es correcto
                return False
        else:
            # No se encuentra el usuario
            raise NoExisteUsuario(str(id_usuario))        

    def check_username(self, user_name):
        """Comprueba que la sesión es correcta"""
        
        user = self.conector.conexion.query(usuariosNeptuno).\
                            filter_by(login=user_name).first()
    
        if user is None:
            return "true"
        else:
            return "false"
        
    
    def check_sesion(self, id_usuario, id_sesion):
        """
        Comprueba que la sesión es correcta
        
        IN
          id_usuario <int>
          id_sesion <str>
          
        OUT
          <bool>
          
        EXC
          NoExisteUsuario
        """
        
        user = self.conector.conexion.query(usuariosNeptuno).\
                    filter(usuariosNeptuno.id == id_usuario).first()
    
        if user != None:
            sesion = self.conector.conexion.\
                        query(sesionesNeptuno).\
                        filter_by(id_usuarios_id=id_usuario,
                                  challenge=id_sesion).first()
                
            return sesion != None       
        else:
            # No se encuentra el usuario
            raise NoExisteUsuario(str(id_usuario))
    
    def check_login(self, cls, user_login, user_password, ip):
        """
        Comprueba el login en función de nombre de usuario y contraseña
        
        IN
          user_login <str>
          user_password <str>
          ip <str>
          
        OUT
          <dict> = {"id": <int>,
                    "nombre": <str>,
                    "challenge": <str>}
          
        EXC
          EGenerandoSesion
          EContrasenyaIncorrecta
          EGenerandoSalt
          NoExisteUsuario
        """
        
        # "cls", antes "usuariosNeptuno"
        user = self.conector.conexion.query(cls).\
                    filter_by(nombre_usuario=user_login).first()
                    
        if user != None:
            salt = self.conector.conexion.query(saltsNeptuno).\
                filter_by(id_usuarios_id=user.id).first()
        
            if not salt is None:
                mi_sh = SaltedHash(user_password, salt.salt)
            
                if mi_sh.getHash() == user.contrasenya:
                    # Login OK
                    crypto_util = CryptoUtils()
                    id_sesion = crypto_util.cadena_aleatoria(32)
                
                    # Insertamos el nuevo registro
                    user_sesion = sesionesNeptuno()
                    user_sesion.id_usuarios_id = user.id
                    user_sesion.challenge = id_sesion  
                    user_sesion.ip = ip 
                    user_sesion.fecha_caducidad = datetime.now() + timedelta(minutes=SESSION_LIFE)              
                
                    try:
                        self.conector.conexion.add(user_sesion)

                        user.fecha_ultimo_login = datetime.now()
                        self.conector.conexion.add(user)                        
                        self.conector.conexion.commit()
                        
                        datos = user.datos_login()
                        datos['challenge'] = id_sesion
                        
                        return datos
                                            
                    except Exception:
                        # No se ha podido insertar el identificador de sesión
                        self.conector.conexion.rollback()
                        raise EGenerandoSesion                        
                else:
                    # La contraseña es incorrecta                     
                    raise EContrasenaIncorrecta
            else:
                # Error obteniendo salt                
                raise EGenerandoSalt                        
        else:
            # No se encuentra un usuario con dicho login
            raise NoExisteUsuario(user_login)
