#-*- coding: utf-8 -*-

import hashlib
import random
from sqlalchemy.sql.expression import and_, func
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime, timedelta
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.log import NeptunoLogger
from nucleo.const_datos import SESSION_LIFE
from unidadescompartidasNeptuno import UsuariosNeptuno,\
    SesionesNeptuno
from libpy.excepciones.loginneptuno import ELoginIncorrecto

class loginNeptuno(object):

    def __init__(self, conector):
        self.conector = conector    
    
    def delelete_sesion(self, id_usuario, id_sesion):
    
        user = self.conector.conexion.query(UsuariosNeptuno).\
            filter(UsuariosNeptuno.id == id_usuario).first()
    
        if user != None:
            sesion = \
                self.conector.conexion.query(SesionesNeptuno).\
                    filter(and_(SesionesNeptuno.id_usuarios_usuario==id_usuario,
                                SesionesNeptuno.challenge == id_sesion)).\
                    first()        

            if sesion != None:
                self.conector.conexion.delete(sesion)
                self.conector.conexion.commit()
            else:
                # El identificador de sesion no es correcto
                return False
        else:
            # No se encuentra el usuario
            raise NoExisteUsuario(str(id_usuario))        

    def check_sesion(self, id_usuario, id_sesion):
        """
        Comprueba que la sesión es correcta
        
        IN
          id_usuario  <int>
          id_sesion   <str>
          
        OUT
          ???
          
        EXC
          NoExisteUsuario
          SesionIncorrecta
        """
        
        user = self.conector.conexion.query(UsuariosNeptuno).\
                    filter(UsuariosNeptuno.id == id_usuario).first()
    
        if user != None:
            sesion = \
                self.conector.conexion.query(SesionesNeptuno).\
                    filter(and_(SesionesNeptuno.id_usuarios_usuario == id_usuario,
                                SesionesNeptuno.challenge == id_sesion,
                                SesionesNeptuno.fecha_caducidad >= current_timestamp())).\
                    first()
                
            if not sesion:
                raise SesionIncorrecta()       
        else:
            # No se encuentra el usuario
            raise NoExisteUsuario(str(id_usuario))
    
    def login(self, cls, user_login, user_password, ip):
        """
        Comprueba el login en función del nombre de usuario (user_login) y la 
        contraseña (user_password).
        
        IN
          user_login     <str>
          user_password  <str>
          ip             <str>
          
        OUT
          {
           "id": <int>,
           "nombre": <str>,
           "challenge": <str>
          }
          
        EXC
          ELoginIncorrecto
        """
        
        logger = NeptunoLogger.get_logger('loginNeptuno.login')
        logger.debug('Usuario "%s" haciendo login' % user_login)

        # buscar usuario
        usuario = \
            self.conector.conexion.\
            query(cls).\
            filter(and_(func.upper(cls.nombre_usuario) == user_login.upper(),
                        "md5(cast(usuarios.id as text)||:psswd) = usuarios.contrasenya")).\
            params(psswd=user_password).\
            first()
            
        if not usuario:
            e = ELoginIncorrecto(user_login)
            logger.error(e)
            raise e
        
        # crear sesión
        sesion = SesionesNeptuno()
        sesion.id_usuarios_usuario = usuario.id
        sesion.ip = ip
        sesion.fecha_caducidad = datetime.now() + timedelta(minutes=SESSION_LIFE)
        
        # generar cadena aleatoria de 32 caracteres
        h = hashlib.md5()
        random.seed()
        h.update('%6.6d' % random.randint(0, 999999))    
        sesion.challenge = h.hexdigest()
    
        self.conector.conexion.add(sesion)
        self.conector.conexion.commit()
        
        datos = usuario.datos_login(conector=self.conector)
        datos['challenge'] = sesion.challenge
        
        return datos
