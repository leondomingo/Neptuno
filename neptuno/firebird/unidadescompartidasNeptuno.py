# -*- coding: utf-8 -*-

# Firebird

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, TIMESTAMP #, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.functions import current_timestamp
from libpy.log import NeptunoLogger
from libpy.excepciones.usuarios import NombreDeUsuarioYaExiste 
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario, NoExisteRol
from nucleo.const_datos import ROLES
from libpy.firebird.util import nombre_tabla, cod_objeto,\
    fecha_de_creacion, fecha_de_actualizacion, atributo_objeto, ValorLogico
from libpy.firebird.const_olympo import cl_Sesiones,\
    sesiones_fechadecreacion, sesiones_fechadeactualizacion, sesiones_usuario,\
    sesiones_direccionip, sesiones_usuarioweb, cl_UsuariosWeb,\
    usuariosweb_fechadecreacion, usuariosweb_fechadeactualizacion,\
    usuariosweb_usuarioperfil, usuariosweb_contrasena,\
    usuariosweb_nombredeusuario, usuariosweb_ultimologin, usuariosweb_usuario,\
    sesiones_challenge, usuariosweb_rol, cl_Clases, clases_fechadecreacion,\
    clases_fechadeactualizacion, clases_usuario, cl_Usuarios,\
    usuarios_fechadecreacion, usuarios_fechadeactualizacion, usuarios_usuario,\
    usuarios_nombre, usuarios_gestiondocumental, usuarios_administrador,\
    cl_Documentos, documentos_fechadecreacion,\
    documentos_fechadeactualizacion, documentos_usuario, cl_Atributos,\
    atributos_fechadecreacion, atributos_fechadeactualizacion, atributos_usuario,\
    atributos_nombre, atributos_clase, atributos_atributoenlazado,\
    atributos_clasedeatributoenlazado, atributos_tipodeatributo,\
    atributos_tipodevalor, atributos_estructural,\
    atributos_requerido, atributos_unico, documentos_titulo,\
    documentos_repositorio, documentos_formato, documentos_autor,\
    documentos_tipo, documentos_version, documentos_estado, documentos_privado,\
    cl_FormatosDeDocumento, formatosdedocumento_fechadecreacion,\
    formatosdedocumento_fechadeactualizacion, formatosdedocumento_usuario,\
    formatosdedocumento_nombre, formatosdedocumento_extension,\
    formatosdedocumento_descripcion, cl_RelacionObjetosDocumentos,\
    relacionobjetosdocumentos_fechadecreacion,\
    relacionobjetosdocumentos_fechadeactualizacion,\
    relacionobjetosdocumentos_usuario, relacionobjetosdocumentos_clase,\
    relacionobjetosdocumentos_codigodeobjeto,\
    relacionobjetosdocumentos_documento, clases_nombre, cl_Consultas,\
    consultas_fechaversion, consultas_usuario, consultas_nombre, consultas_clase,\
    consultas_identificador, consultas_fichero, consultas_utilizarfastreport,\
    consultas_fechadecreacion, cl_ParametrosDeConsulta,\
    parametrosdeconsulta_fechadecreacion,\
    parametrosdeconsulta_fechadeactualizacion, parametrosdeconsulta_usuario,\
    parametrosdeconsulta_consulta, usuarios_login, cl_IdiomasOlympo,\
    idiomasolympo_fechadecreacion, idiomasolympo_fechadeactualizacion,\
    idiomasolympo_usuario, idiomasolympo_nombre, idiomasolympo_activo,\
    idiomasolympo_codigo, sesiones_fechadecaducidad, usuariosweb_nombre,\
    cl_TiposDeDocumento, tiposdedocumento_fechadecreacion,\
    tiposdedocumento_fechadeactualizacion, tiposdedocumento_usuario,\
    tiposdedocumento_nombre, tiposdedocumento_descripcion
from libpy.const_datos_neptuno import PRIVL_LECTURA_ESCRITURA
from nucleo.const_datos import SESSION_LIFE

Base = declarative_base()
        
#class saltsNeptuno(Base):
#    __tablename__ = 'salts'
#    
#    cod_clase = 0 #cl_Salts
#    
#    def __init__(self): pass
#    
#    id = Column(Integer, primary_key=True)
#    id_usuarios_id = Column(Integer, ForeignKey('usuarios.id'))    
#    salt = Column(String)

class sesionesNeptuno(Base):
    
    __tablename__ = nombre_tabla(cl_Sesiones)
    cod_clase = cl_Sesiones
    
    id = cod_objeto(cl_Sesiones)
    fechadecreacion = fecha_de_creacion(sesiones_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(sesiones_fechadeactualizacion)
    id_usuarios_usuario = Column(sesiones_usuario, Integer)
    direccionip = Column(sesiones_direccionip, String)
    id_usuariosweb_usuarioweb = Column(sesiones_usuarioweb, Integer)
    challenge = Column(sesiones_challenge, String)
    fecha_caducidad = Column(sesiones_fechadecaducidad, TIMESTAMP)
    
class usuariosNeptuno(Base):
    
    __tablename__ = nombre_tabla(cl_UsuariosWeb)
    cod_clase = cl_UsuariosWeb
    
    id = cod_objeto(cl_UsuariosWeb)
    fechadecreacion = fecha_de_creacion(usuariosweb_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(usuariosweb_fechadeactualizacion)
    id_usuarios_usuario = Column(usuariosweb_usuario, Integer)
    id_usuarios_usuarioperfil = Column(usuariosweb_usuarioperfil, Integer)
    nombre_usuario = Column(usuariosweb_nombredeusuario, String)
    contrasenya = Column(usuariosweb_contrasena, String)
    nombre = Column(usuariosweb_nombre, String)
    rol = Column(usuariosweb_rol, String)
    ultimologin = Column(usuariosweb_ultimologin, TIMESTAMP) #, default=datetime.now())
    
    privl_tabla = None
    privl_columna = None
    privl_accion = None
    privl_clases = None
    
    def __init__(self): pass
    
    def getPrivilegioTabla(self, tabla):
        return PRIVL_LECTURA_ESCRITURA
#        return self.privl_tabla.getPrivilegio(self.rol, tabla)
    
    def getPrivilegioColumna(self, tabla, columna):
        return PRIVL_LECTURA_ESCRITURA
#        return self.privl_columna.getPrivilegio(self.rol, tabla, columna)
    
    def getListaAccionesProhibidas(self, tabla):
        return self.privl_accion.getListaAcciones(self.rol, tabla)
    
    def getListaClasesProhibidas(self):
        return self.privl_clases.getListaClases(self.rol)
    
    @classmethod
    def nuevo_usuario(cls, conector, login, passwd, rol, id_usuarioperfil):
        """
        Crea un nuevo usuario con 'login', 'passwd' y 'rol', y devuelve un objeto 
        de 'usuarios' en caso de éxito, o una excepción en caso de que el nombre 
        de usuario ya esté en uso.
        
        IN
          conector
          login
          passwd
          rol
        
        EXC
          NombreDeUsuarioYaExiste
          NoExisteRol
          ImportError
        """
        
#        sh = SaltedHash(passwd)
        
        if not conector.conexion.query(cls).\
                    filter(usuariosNeptuno.nombre_usuario == login).first:
            raise NombreDeUsuarioYaExiste(login)
        
        if not rol.upper() in ROLES:
            raise NoExisteRol(rol.upper()) 
                
        nuevo_usuario = usuariosNeptuno()
        nuevo_usuario.nombre_usuario = login
        nuevo_usuario.contrasena = passwd
        nuevo_usuario.rol = rol
        nuevo_usuario.id_usuarios_usuarioperfil = id_usuarioperfil
        
        conector.conexion.add(nuevo_usuario)
        conector.conexion.commit()
        
#        s = saltsNeptuno()
#        s.salt = sh.getSalt()
#        s.id_usuarios_id = nuevo_usuario.id
        
#        conector.conexion.add(s)
#        conector.conexion.commit()

        return nuevo_usuario
    
    def actualizar_login(self, conector, nuevo_login):
        
        self.nombre_usuario = nuevo_login
        conector.conexion.add(self)
        conector.conexion.commit()
        
    def actualizar_password(self, conector, nueva_password):
        """Actualiza la contraseña del usuario con 'nueva_password'"""
        
        self.contrasenya = nueva_password
        conector.conexion.add(self)
        conector.conexion.commit()
        
#        sh = SaltedHash(nueva_password)
#        
#        self.contrasenya = sh.getHash()
#        
#        if self.salt is None:
#            # Si no existe, creamos un registro
#            self.salt = saltsNeptuno()
#        
#        self.salt.salt = sh.getSalt()
#
#        conector.conexion.add(self.salt)
#        conector.conexion.add(self)
#        conector.conexion.commit()
        
    @classmethod
    def comprobar_usuario(cls, conector, id_usuario):
        """Comprueba que existe el usuario (id_usuario) y devuelve el objeto en 
        caso de éxito. En otro caso lanza la excepción "NoExisteUsuario"."""
        
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
          conector    <Conexion>
          id_usuario  <int>
          id_sesion   <str>
            
        OUT
          <usuariosNeptuno>
            
        EXC
          NoExisteUsuario
          SesionIncorrecta
        """
        
        logger = NeptunoLogger.get_logger('usuariosNeptuno.comprobar_sesion')
        try:
            logger.debug('Comprobando sesión...%d %s' % (id_usuario, id_sesion))
            
            usuario = conector.conexion.query(cls).get(id_usuario)        
            if usuario is None:
                raise NoExisteUsuario(id_usuario)
            
            # Comprobar sesión
            sesion = \
                conector.conexion.query(sesionesNeptuno).\
                        filter(and_(sesionesNeptuno.id_usuariosweb_usuarioweb == id_usuario,
                                    sesionesNeptuno.challenge == id_sesion,
                                    sesionesNeptuno.fecha_caducidad >= current_timestamp()
                                    )).\
                        first()
                        
            if sesion is None:
                raise SesionIncorrecta()
            
            sesion.fecha_caducidad = datetime.now() + timedelta(minutes=SESSION_LIFE)
            conector.conexion.add(sesion)
            conector.conexion.commit()
            
            return usuario
        
        except Exception, e:
            logger.error(e)
            raise
    
    @classmethod
    def getUsuario(cls, conector, login):
        """
        Devuelve el usuario con nombre de usuario 'login' en caso de que exista o
        salta la excepción NoExisteUsuario.
        
        IN
          conector
          login
            
        OUT
          (objeto de <usuariosAtenea>)
            
        EXC
          NoExisteUsuario
        """
        
        usuario = conector.conexion.query(cls).\
                    filter(usuariosNeptuno.nombre_usuario == login).first()        
                    
        if usuario is None:
            raise NoExisteUsuario(login)
        
        return usuario
    
    def datos_login(self, **kw):
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
    
class ClasesOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Clases)    
    cod_clase = cl_Clases
    
    id = cod_objeto(cl_Clases)
    
    fechaDeCreacion = fecha_de_creacion(clases_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(clases_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(clases_usuario, cl_Usuarios)
    
    nombre = Column(clases_nombre, String)
    #descripcion = Column(clases_descripcion, String)

class AtributosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Atributos)    
    cod_clase = cl_Atributos
    
    def __init__(self): pass
    
    id = cod_objeto(cl_Atributos)
    
    fechaDeCreacion = fecha_de_creacion(atributos_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(atributos_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(atributos_usuario, cl_Usuarios)
    
    nombre = Column(atributos_nombre, String)
    id_clases_clase = atributo_objeto(atributos_clase, cl_Clases)
        
    id_atri_atributoenlazado = atributo_objeto(atributos_atributoenlazado, cl_Atributos)
    id_clas_clasedeatributoenlazado = atributo_objeto(atributos_clasedeatributoenlazado, cl_Atributos)
    
    id_tda_tipodeatributo = Column(atributos_tipodeatributo, Integer) # tipos de atributos
    id_tdv_tipodevalor = Column(atributos_tipodevalor, Integer) # tipos de valores
    
    id_valo_estructural = Column(atributos_estructural, Integer)
    estructural = ValorLogico('id_valo_estructural')
    
    id_valo_requerido = Column(atributos_requerido, Integer)
    requerido = ValorLogico('id_valo_requerido')
    
    id_valo_unico = Column(atributos_unico, Integer)
    unico = ValorLogico('id_valo_unico')
    
ClasesOlympo.atributos = \
    relation(AtributosOlympo,
             backref='clase',
             primaryjoin=ClasesOlympo.id == AtributosOlympo.id_clases_clase)   

class UsuariosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Usuarios)    
    cod_clase = cl_Usuarios
    
    id = cod_objeto(cl_Usuarios)
    fechaDeCreacion = fecha_de_creacion(usuarios_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(usuarios_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(usuarios_usuario, cl_Usuarios)
    
    nombre = Column(usuarios_nombre, String)
    login = Column(usuarios_login, String)
    
    id_valo_administrador = Column(usuarios_administrador, Integer)
    administrador = ValorLogico('id_valo_administrador')
    
    id_valo_gestionDocumental = Column(usuarios_gestiondocumental, Integer)
    gestionDocumental = ValorLogico('id_valo_gestionDocumental')    

class DocumentosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Documentos)    
    cod_clase = cl_Documentos
    
    id = cod_objeto(cl_Documentos)
    fechaDeCreacion = fecha_de_creacion(documentos_fechadecreacion)
    fechaDeActualizacin = fecha_de_actualizacion(documentos_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(documentos_usuario, cl_Usuarios)
    
    titulo = Column(documentos_titulo, String)
    repositorio = Column(documentos_repositorio, String)
    formato = atributo_objeto(documentos_formato, cl_FormatosDeDocumento)
    autor = Column(documentos_autor, String) 
    tipo = atributo_objeto(documentos_tipo, cl_TiposDeDocumento)
    version = Column(documentos_version, String)
    estado = Column(documentos_estado, Integer) # estados de documentos
    
    id_valo_privado = Column(documentos_privado, Integer) # valores lógicos
    privado = ValorLogico('id_valo_privado')
    
class TiposDeDocumento(Base):
    
    __tablename__ = nombre_tabla(cl_TiposDeDocumento)
    cod_clase = cl_TiposDeDocumento
    
    id = cod_objeto(cl_TiposDeDocumento)
    fechadecreacion = fecha_de_creacion(tiposdedocumento_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(tiposdedocumento_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(tiposdedocumento_usuario, cl_Usuarios)
    
    nombre = Column(tiposdedocumento_nombre, String)
    descripcion = Column(tiposdedocumento_descripcion, String)    
    
class FormatosDeDocumentoOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_FormatosDeDocumento)
    cod_clase = cl_FormatosDeDocumento
    
    id = cod_objeto(cl_FormatosDeDocumento)
    fechaDeCreacion = fecha_de_creacion(formatosdedocumento_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(formatosdedocumento_fechadeactualizacion)
    id_usuario_usuario = atributo_objeto(formatosdedocumento_usuario, cl_Usuarios)
    
    nombre = Column(formatosdedocumento_nombre, String)
    extension = Column(formatosdedocumento_extension, String)
    descripcion = Column(formatosdedocumento_descripcion, String)
    
class RelacionObjetosDocumentosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_RelacionObjetosDocumentos)
    cod_clase = cl_RelacionObjetosDocumentos
    
    id = cod_objeto(cl_RelacionObjetosDocumentos)
    fechaDeCreacion = fecha_de_creacion(relacionobjetosdocumentos_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(relacionobjetosdocumentos_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(relacionobjetosdocumentos_usuario, cl_Usuarios)
    
    id_clases_clase = atributo_objeto(relacionobjetosdocumentos_clase, cl_Clases)
    codigoDeObjeto = Column(relacionobjetosdocumentos_codigodeobjeto, Integer)
    id_documentos_documento = atributo_objeto(relacionobjetosdocumentos_documento, cl_Documentos) 
    
class ConsultasOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Consultas)
    cod_clase = cl_Consultas
    
    id = cod_objeto(cl_Consultas)
    fechaDeCreacion = fecha_de_creacion(consultas_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(consultas_fechaversion)
    id_usuarios_usuario = atributo_objeto(consultas_usuario, cl_Usuarios)
    
    nombre = Column(consultas_nombre, String)
    clase = atributo_objeto(consultas_clase, cl_Clases)
    fichero = Column(consultas_fichero, String)
    identificador = Column(consultas_identificador, String)
    id_valo_utilizarFastReport = Column(consultas_utilizarfastreport, Integer)
    utilizarFastReport = ValorLogico('id_valo_utilizarFastReport')
    
class ParametrosDeConsultaOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_ParametrosDeConsulta)
    cod_clase = cl_ParametrosDeConsulta
    
    id = cod_objeto(cl_ParametrosDeConsulta)
    fechaDeCreacion = fecha_de_creacion(parametrosdeconsulta_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(parametrosdeconsulta_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(parametrosdeconsulta_usuario, cl_Usuarios)
    
    id_consultas_consulta = atributo_objeto(parametrosdeconsulta_consulta, cl_Consultas)
    
ConsultasOlympo.parametros = \
    relation(ParametrosDeConsultaOlympo,
             backref='consulta',
             primaryjoin=ConsultasOlympo.id == ParametrosDeConsultaOlympo.id_consultas_consulta)
    
class IdiomasOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_IdiomasOlympo)
    cod_clase = cl_IdiomasOlympo
    
    id = cod_objeto(cl_IdiomasOlympo)
    fechadecreacion = fecha_de_creacion(idiomasolympo_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(idiomasolympo_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(idiomasolympo_usuario, cl_Usuarios)
    
    nombre = Column(idiomasolympo_nombre, String)
    codigo = Column(idiomasolympo_codigo, Integer)
    
    id_valo_activo = Column(idiomasolympo_activo, Integer)
    activo = ValorLogico('id_valo_activo')
    
    