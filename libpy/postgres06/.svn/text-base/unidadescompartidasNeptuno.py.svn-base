# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.expression import and_
from libpy.cryptoutils import SaltedHash
from libpy.excepciones.usuarios import NombreDeUsuarioYaExiste 
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario, NoExisteRol
from datetime import datetime, timedelta
from nucleo.const_datos import ROLES, SESSION_LIFE
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('libpy.postgres.unidadescompartidasNeptuno')

# creamos la clase "base" de la que derivan todas las bases que vayan a estar enlazadas con una tabla
Base = declarative_base()
        
class saltsNeptuno(Base):

    __tablename__ = 'salts'
    id = Column(Integer, primary_key=True)
    id_usuarios_id = Column(Integer, ForeignKey('usuarios.id'))    
    salt = Column(String)

class sesionesNeptuno(Base):

    __tablename__ = 'sesiones'
    id = Column(Integer, primary_key=True)
    id_usuarios_id = Column(Integer, ForeignKey('usuarios.id'))
    
    challenge = Column(String)
    fecha_creacion = Column(TIMESTAMP)
    fecha_caducidad = Column(TIMESTAMP)
    ip = Column(String)
    
class usuariosNeptuno(Base):
    
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String)
    contrasenya = Column(String)
    rol = Column(String)
    
    salt = relation(saltsNeptuno,
                    backref='usuario',
                    uselist=False,
                    primaryjoin=id==saltsNeptuno.id_usuarios_id)
    
    fecha_creacion = Column(TIMESTAMP)
    fecha_actualizacion = Column(TIMESTAMP, onupdate=datetime.now())
    fecha_ultimo_login = Column(TIMESTAMP)

    privl_tabla = None
    privl_columna = None
    privl_accion = None
    privl_clases = None
    
    def getPrivilegioTabla(self, tabla):
        return self.privl_tabla.getPrivilegio(self.rol, tabla)
    
    def getPrivilegioColumna(self, tabla, columna):
        return self.privl_columna.getPrivilegio(self.rol, tabla, columna)
    
    def getListaAccionesProhibidas(self, tabla):
        return self.privl_accion.getListaAcciones(self.rol, tabla)
    
    def getListaClasesProhibidas(self):
        return self.privl_clases.getListaClases(self.rol)
    
    @staticmethod
    def nuevo_usuario(conector, login, passwd, rol):
        """
        Crea un nuevo usuario con 'login', 'passwd' y 'rol', y devuelve un objeto 
        de 'usuarios' en caso de éxito, o una excepción en caso de que el nombre 
        de usuario ya esté en uso.
        
        IN
          conector <conexionNeptuno>
          login <str>
          passwd <str>
          rol <str>
        
        OUT
          <usuariosNeptuno>
        
        EXC
          NombreDeUsuarioYaExiste
          NoExisteRol
          ImportError
        """
        
        sh = SaltedHash(passwd)
        
        if not conector.conexion.query(usuariosNeptuno).filter_by(nombre_usuario=login).first() is None:
            raise NombreDeUsuarioYaExiste(login)
        
        if not rol.upper() in ROLES:
            raise NoExisteRol(rol.upper()) 
                
        nuevo_usuario = usuariosNeptuno()
        nuevo_usuario.nombre_usuario = login
        nuevo_usuario.contrasenya = sh.getHash()
        nuevo_usuario.rol = rol.upper()
       
        conector.conexion.add(nuevo_usuario)
        conector.conexion.commit()
        
        s = saltsNeptuno()
        s.salt = sh.getSalt()
        s.id_usuarios_id = nuevo_usuario.id
        
        conector.conexion.add(s)
        conector.conexion.commit()
        
        return nuevo_usuario
        
    def actualizar_password(self, conector, nueva_password):
        """
        Actualiza la contraseña del usuario con 'nueva_password'.
        
        IN
          conector <conexionNeptuno>
          nueva_password <str>
        """
        sh = SaltedHash(nueva_password)
        
        self.contrasenya = sh.getHash()
        
        if self.salt is None:
            # Si no existe, creamos un registro
            self.salt = saltsNeptuno()
        
        self.salt.salt = sh.getSalt()

        conector.conexion.add(self.salt)
        conector.conexion.add(self)
        conector.conexion.commit()
        
    @classmethod
    def comprobar_usuario(cls, conector, id_usuario):
        """
        Comprueba que existe el usuario (id_usuario) y devuelve el objeto en caso de éxito. 
        En otro caso lanza la excepción "NoExisteUsuario".
        
        IN
          conector <conexionNeptuno>
          id_usuario <int>
          
        OUT
          <usuariosNeptuno>
           
        EXC
          <NoExisteUsuario>
        """
        
        usuario = conector.conexion.query(cls).get(id_usuario)
        if usuario is None:
            raise NoExisteUsuario(id_usuario)
        
        return usuario        
        
    @classmethod
    def comprobar_sesion(cls, conector, id_usuario, id_sesion):
        """
        Comprueba el usuario y la sesión, y devuelve el usuario que corresponde 
        al id_usuario en caso de éxito, o una excepción en caso de fallo.
        
        IN
          conector   <ConexionNeptuno>
          id_usuario <int>
          id_sesion  <str>
          
        OUT
          <usuariosNeptuno>
            
        EXC
          NoExisteUsuario
          SesionIncorrecta
        """
        
        logger.debug('comprobar_sesion: Comprobando sesión (%d %s)' % \
                        (id_usuario, id_sesion))
        
        usuario = conector.conexion.query(cls).get(id_usuario)
        if usuario is None:
            raise NoExisteUsuario()
        
        # Buscar sesión
        sesion = conector.conexion.query(sesionesNeptuno).\
                    filter(and_(sesionesNeptuno.id_usuarios_id == id_usuario,
                                sesionesNeptuno.challenge == id_sesion,
                                sesionesNeptuno.fecha_caducidad >= current_timestamp())).\
                    first()
                    
        if sesion is None:
            logger.error('Sesión incorrecta')
            raise SesionIncorrecta()
        
        # alargar la caducidad
        sesion.fecha_caducidad = datetime.now() + timedelta(minutes=SESSION_LIFE)
        conector.conexion.add(sesion)
        conector.conexion.commit()
        
        return usuario 
    
    @staticmethod
    def getUsuario(conector, login):
        """
        Devuelve el usuario con nombre de usuario 'login' en caso de que exista o
        salta la excepción NoExisteUsuario.
        
        IN
          conector <conexionNeptuno>
          login <str>
            
        OUT
           <usuariosNeptuno>
            
        EXC
          NoExisteUsuario
        """
        
        usuario = conector.conexion.query(usuariosNeptuno).filter_by(nombre_usuario=login).first()        
        if usuario is None:
            raise NoExisteUsuario(login)
        
        return usuario
    
    def datos_login(self):
        """
        Devuelve los datos de login "básicos". Este método puede ser reescrito
        en cada proyecto.
        
        IN
        OUT
          {
           'id': <int>,
           'nombre': <str>,
           'rol': <str>
          }
        """
        
        return dict(id=self.id,
                    nombre=self.nombre_usuario,
                    rol=self.rol)
        
        