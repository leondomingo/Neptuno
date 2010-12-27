# -*- coding: utf-8 -*-

# Firebird

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, TIMESTAMP #, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.functions import current_timestamp
from libpy.excepciones.usuarios import NombreDeUsuarioYaExiste 
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario, NoExisteRol
from nucleo.const_datos import ROLES
from libpy.firebird.util import nombre_tabla, cod_objeto,\
    fecha_de_creacion, fecha_de_actualizacion, atributo_objeto, ValorLogico
from libpy.firebird.const_olympo import cl_Sesiones, cl_UsuariosWeb,\
    atri_tipodeatributo, atri_tipodevalor, sesi_fechadecreacion, \
    sesi_fechadeactualizacion, sesi_usuario, sesi_direccionip, sesi_usuarioweb, \
    sesi_challenge, sesi_fechadecaducidad, uswe_fechadecreacion, \
    uswe_fechadeactualizacion, uswe_usuario, uswe_usuarioperfil, \
    uswe_nombredeusuario, uswe_contrasena, uswe_nombre, uswe_rol, uswe_ultimologin, \
    clas_fechadecreacion, clas_fechadeactualizacion, clas_usuario, clas_nombre, \
    atri_fechadecreacion, atri_fechadeactualizacion, atri_usuario, atri_nombre, \
    atri_clase, atri_atributoenlazado, atri_clasedeatributoenlazado, atri_estructural,\
    atri_requerido, atri_unico, usua_fechadecreacion, usua_fechadeactualizacion,\
    usua_usuario, usua_nombre, usua_login, usua_administrador,\
    usua_gestiondocumental, docu_fechadecreacion, docu_fechadeactualizacion,\
    docu_usuario, docu_titulo, docu_formato, docu_repositorio, docu_autor,\
    docu_tipo, docu_version, docu_estado, docu_privado, tdd_fechadeactualizacion,\
    tdd_usuario, tdd_fechadecreacion, tdd_nombre, tdd_descripcion,\
    fdd_fechadecreacion, fdd_fechadeactualizacion, fdd_usuario, fdd_nombre,\
    fdd_extension, fdd_descripcion, reob_fechadecreacion,\
    reob_fechadeactualizacion, reob_usuario, reob_clase, reob_codigodeobjeto,\
    reob_documento, cons_fechadecreacion, cons_fechaversion, cons_usuario,\
    cons_nombre, cons_clase, cons_fichero, cons_identificador,\
    cons_utilizarfastreport, pdc_fechadecreacion, pdc_fechadeactualizacion,\
    pdc_usuario, pdc_consulta, idol_fechadecreacion, idol_fechadeactualizacion,\
    idol_usuario, idol_nombre, idol_codigo, idol_activo, cl_Atributos,\
    cl_Usuarios, cl_Clases, cl_Documentos, cl_FormatosDeDocumento,\
    cl_TiposDeDocumento, cl_RelacionObjetosDocumentos, cl_Consultas,\
    cl_ParametrosDeConsulta, cl_IdiomasOlympo
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
    fechadecreacion = fecha_de_creacion(sesi_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(sesi_fechadeactualizacion)
    id_usuarios_usuario = Column(sesi_usuario, Integer)
    direccionip = Column(sesi_direccionip, String)
    id_usuariosweb_usuarioweb = Column(sesi_usuarioweb, Integer)
    challenge = Column(sesi_challenge, String)
    fecha_caducidad = Column(sesi_fechadecaducidad, TIMESTAMP)
    
class usuariosNeptuno(Base):
    
    __tablename__ = nombre_tabla(cl_UsuariosWeb)
    cod_clase = cl_UsuariosWeb
    
    id = cod_objeto(cl_UsuariosWeb)
    fechadecreacion = fecha_de_creacion(uswe_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(uswe_fechadeactualizacion)
    id_usuarios_usuario = Column(uswe_usuario, Integer)
    id_usuarios_usuarioperfil = Column(uswe_usuarioperfil, Integer)
    nombre_usuario = Column(uswe_nombredeusuario, String)
    contrasenya = Column(uswe_contrasena, String)
    nombre = Column(uswe_nombre, String)
    rol = Column(uswe_rol, String)
    ultimologin = Column(uswe_ultimologin, TIMESTAMP) #, default=datetime.now())
    
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
          conector
          id_usuario
          id_sesion
            
        OUT
          <usuariosNeptuno>
            
        EXC
          NoExisteUsuario
          SesionIncorrecta
        """
        
        usuario = conector.conexion.query(cls).get(id_usuario)        
        if usuario is None:
            raise NoExisteUsuario()
        
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
    
    fechaDeCreacion = fecha_de_creacion(clas_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(clas_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(clas_usuario, cl_Usuarios)
    
    nombre = Column(clas_nombre, String)
    #descripcion = Column(clas_descripcion, String)

class AtributosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Atributos)    
    cod_clase = cl_Atributos
    
    def __init__(self): pass
    
    id = cod_objeto(cl_Atributos)
    
    fechaDeCreacion = fecha_de_creacion(atri_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(atri_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(atri_usuario, cl_Usuarios)
    
    nombre = Column(atri_nombre, String)
    id_clases_clase = atributo_objeto(atri_clase, cl_Clases)
        
    atributoEnlazado = atributo_objeto(atri_atributoenlazado, cl_Atributos)
    id_clas_clasedeatributoenlazado = atributo_objeto(atri_clasedeatributoenlazado, cl_Atributos)
    
    id_tda_tipodeatributo = Column(atri_tipodeatributo, Integer) # tipos de atributos
    id_tdv_tipodevalor = Column(atri_tipodevalor, Integer) # tipos de valores
    
    id_valo_estructural = Column(atri_estructural, Integer)
    estructural = ValorLogico('id_valo_estructural')
    
    id_valo_requerido = Column(atri_requerido, Integer)
    requerido = ValorLogico('id_valo_requerido')
    
    id_valo_unico = Column(atri_unico, Integer)
    unico = ValorLogico('id_valo_unico')
    
ClasesOlympo.atributos = \
    relation(AtributosOlympo,
             backref='clase',
             primaryjoin=ClasesOlympo.id == AtributosOlympo.id_clases_clase)   

class UsuariosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Usuarios)    
    cod_clase = cl_Usuarios
    
    id = cod_objeto(cl_Usuarios)
    fechaDeCreacion = fecha_de_creacion(usua_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(usua_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(usua_usuario, cl_Usuarios)
    
    nombre = Column(usua_nombre, String)
    login = Column(usua_login, String)
    
    id_valo_administrador = Column(usua_administrador, Integer)
    administrador = ValorLogico('id_valo_administrador')
    
    id_valo_gestionDocumental = Column(usua_gestiondocumental, Integer)
    gestionDocumental = ValorLogico('id_valo_gestionDocumental')    

class DocumentosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Documentos)    
    cod_clase = cl_Documentos
    
    id = cod_objeto(cl_Documentos)
    fechaDeCreacion = fecha_de_creacion(docu_fechadecreacion)
    fechaDeActualizacin = fecha_de_actualizacion(docu_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(docu_usuario, cl_Usuarios)
    
    titulo = Column(docu_titulo, String)
    repositorio = Column(docu_repositorio, String)
    formato = atributo_objeto(docu_formato, cl_FormatosDeDocumento)
    autor = Column(docu_autor, String) 
    tipo = atributo_objeto(docu_tipo, cl_TiposDeDocumento)
    version = Column(docu_version, String)
    estado = Column(docu_estado, Integer) # estados de documentos
    
    id_valo_privado = Column(docu_privado, Integer) # valores lógicos
    privado = ValorLogico('id_valo_privado')
    
class TiposDeDocumento(Base):
    
    __tablename__ = nombre_tabla(cl_TiposDeDocumento)
    cod_clase = cl_TiposDeDocumento
    
    id = cod_objeto(cl_TiposDeDocumento)
    fechadecreacion = fecha_de_creacion(tdd_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(tdd_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(tdd_usuario, cl_Usuarios)
    
    nombre = Column(tdd_nombre, String)
    descripcion = Column(tdd_descripcion, String)    
    
class FormatosDeDocumentoOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_FormatosDeDocumento)
    cod_clase = cl_FormatosDeDocumento
    
    id = cod_objeto(cl_FormatosDeDocumento)
    fechaDeCreacion = fecha_de_creacion(fdd_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(fdd_fechadeactualizacion)
    id_usuario_usuario = atributo_objeto(fdd_usuario, cl_Usuarios)
    
    nombre = Column(fdd_nombre, String)
    extension = Column(fdd_extension, String)
    descripcion = Column(fdd_descripcion, String)
    
class RelacionObjetosDocumentosOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_RelacionObjetosDocumentos)
    cod_clase = cl_RelacionObjetosDocumentos
    
    id = cod_objeto(cl_RelacionObjetosDocumentos)
    fechaDeCreacion = fecha_de_creacion(reob_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(reob_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(reob_usuario, cl_Usuarios)
    
    id_clases_clase = atributo_objeto(reob_clase, cl_Clases)
    codigoDeObjeto = Column(reob_codigodeobjeto, Integer)
    id_documentos_documento = atributo_objeto(reob_documento, cl_Documentos) 
    
class ConsultasOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_Consultas)
    cod_clase = cl_Consultas
    
    id = cod_objeto(cl_Consultas)
    fechaDeCreacion = fecha_de_creacion(cons_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(cons_fechaversion)
    id_usuarios_usuario = atributo_objeto(cons_usuario, cl_Usuarios)
    
    nombre = Column(cons_nombre, String)
    clase = atributo_objeto(cons_clase, cl_Clases)
    fichero = Column(cons_fichero, String)
    identificador = Column(cons_identificador, String)
    id_valo_utilizarFastReport = Column(cons_utilizarfastreport, Integer)
    utilizarFastReport = ValorLogico('id_valo_utilizarFastReport')
    
class ParametrosDeConsultaOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_ParametrosDeConsulta)
    cod_clase = cl_ParametrosDeConsulta
    
    id = cod_objeto(cl_ParametrosDeConsulta)
    fechaDeCreacion = fecha_de_creacion(pdc_fechadecreacion)
    fechaDeActualizacion = fecha_de_actualizacion(pdc_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(pdc_usuario, cl_Usuarios)
    
    id_consultas_consulta = atributo_objeto(pdc_consulta, cl_Consultas)
    
ConsultasOlympo.parametros = \
    relation(ParametrosDeConsultaOlympo,
             backref='consulta',
             primaryjoin=ConsultasOlympo.id == ParametrosDeConsultaOlympo.id_consultas_consulta)
    
class IdiomasOlympo(Base):
    
    __tablename__ = nombre_tabla(cl_IdiomasOlympo)
    cod_clase = cl_IdiomasOlympo
    
    id = cod_objeto(cl_IdiomasOlympo)
    fechadecreacion = fecha_de_creacion(idol_fechadecreacion)
    fechadeactualizacion = fecha_de_actualizacion(idol_fechadeactualizacion)
    id_usuarios_usuario = atributo_objeto(idol_usuario, cl_Usuarios)
    
    nombre = Column(idol_nombre, String)
    codigo = Column(idol_codigo, Integer)
    
    id_valo_activo = Column(idol_activo, Integer)
    activo = ValorLogico('id_valo_activo')
    
    