# -*- coding: utf-8 -*-

from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql.expression import and_, func, select
from util import nombre_tabla, cod_atributo
import os.path
from libpy.firebird.const_datos_olympo import TATR_OBJETO, TATR_VALOR
from util import nombre_coleccion
from libpy.const_datos_neptuno import PRIVL_LECTURA_ESCRITURA, PRIVL_NINGUNO,\
    PRIVL_LECTURA
from libpy.firebird.const_datos_olympo import NIDEPR_LECTURA,\
    NIDEPR_LECTURA_ESCRITURA, NIDEPR_NINGUNO, EDD_ESTABLE
import shutil
from libpy.firebird.unidadescompartidasNeptuno import FormatosDeDocumentoOlympo,\
    DocumentosOlympo, RelacionObjetosDocumentosOlympo
from libpy.firebird.const_olympo import cl_RelacionObjetosDocumentos,\
    reob_documento, reob_clase, reob_codigodeobjeto,\
    atri_clasedeatributoenlazado, atri_clase, atri_tipodeatributo, atri_nombre,\
    usua_clasesdelusuario, pda_usuariodelatributo, pda_atributo,\
    pda_niveldeprivilegio, rdd_ruta, docu_titulo, fdd_extension, cl_Clases,\
    cl_Atributos, cl_Usuarios, atri_tipodevalor, cl_PrivilegiosDeAtributo,\
    cl_UsuariosWeb, uswe_usuarioperfil, cl_RepositoriosDeDocumentos,\
    cl_Documentos, cl_FormatosDeDocumento, docu_repositorio, docu_formato

class GestorOlympo(object):
    
    def __init__(self, conector):
        self.conector = conector
        self.meta = MetaData(bind=self.conector.engine)
        
        self.tbl_clases = Table(nombre_tabla(cl_Clases), self.meta, autoload=True)
        self.tbl_atributos = Table(nombre_tabla(cl_Atributos), self.meta, autoload=True)
        self.tbl_usuarios = Table(nombre_tabla(cl_Usuarios), self.meta, autoload=True)
        
    def get_atributo(self, atributo):
        """
        Devuelve el registro de la clase <Atributos> que corresponde al
        atributo 'atributo'.
        
        IN
          atributo <str> = 'ATR_XXXX'
          atributo <int> = XXXX          
        """
        
        if isinstance(atributo, str):
            c_atributo = cod_atributo(atributo)
            
        elif isinstance(atributo, int):
            c_atributo = atributo
            
        else:
            raise Exception('"atributo" debe ser de tipo <str> o <int>')
            
        return self.conector.conexion.\
                execute(self.tbl_atributos.\
                        select(self.tbl_atributos.c.cod_objeto == c_atributo)).fetchone()
        
    def tipo_de_atributo(self, atributo):
        """Devuelve el tipo de atributo (Valor, Objeto, Colección) para el 
        atributo 'atributo'"""
        a = self.get_atributo(atributo)
        return a[atri_tipodeatributo]
    
    def tipo_de_valor(self, atributo):
        """Devuelve el tipo de valor (Carácter, Entero, Real, etc) para el 
        atributo 'atributo'"""
        a = self.get_atributo(atributo)
        return a[atri_tipodevalor]
    
    def clase_enlazada(self, atributo):
        """
        Devuelve el objeto <Table> que representa la clase del atributo enlazado
        para el atributo 'atributo'
                
        IN
          atributo <str> = 'ATR_1234'
          atributo <int> = 1234
          
        OUT
          <sqlalchemy.schema.Table>
        """
        a = self.get_atributo(atributo)        
        return Table(nombre_tabla(a[atri_clasedeatributoenlazado]), 
                     self.meta, autoload=True)
    
    def cod_clase_enlazada(self, atributo):
        """
        Devuelve el código de la clase enlazada del atributo 'atributo'
        IN
          atributo <str> = 'ATR_1234'
          atributo <int> = 1234
        """   
        a = self.get_atributo(atributo)
        return a[atri_clasedeatributoenlazado]
    
    def atributo_usuario(self, clase):
        """
        Devuelve el nombre del atributo (ATR_XXXX) 'Usuario'
        correspondiente de la clase 'clase'"""
        atributo = \
            self.conector.conexion.\
                execute(self.tbl_atributos.\
                        select(and_(self.tbl_atributos.c[atri_clase] == clase,
                                    self.tbl_atributos.c[atri_tipodeatributo] == TATR_OBJETO,
                                    self.tbl_atributos.c[atri_clasedeatributoenlazado] == cl_Usuarios)).\
                        order_by(self.tbl_atributos.c.cod_objeto)).\
                        fetchone()
                                
        return 'atr_%d' % atributo.cod_objeto
    
    def atributo_fechadecreacion(self, clase):
        """Devuelve el nombre del atributo (ATR_XXXX) 'Fecha de creación'
        correspondiente de la clase 'clase'"""
        atributo = \
            self.conector.conexion.\
                execute(self.tbl_atributos.\
                        select(and_(self.tbl_atributos.c[atri_clase] == clase,
                                    self.tbl_atributos.c[atri_tipodeatributo] == TATR_VALOR,
                                    #self.tbl_atributos.c[atributos_tipodevalor] == TVAL_FECHAYHORA,
                                    func.upper(self.tbl_atributos.c[atri_nombre]).like('FECHA DE CREAC%'))).\
                order_by(self.tbl_atributos.c.cod_objeto)).\
                fetchone()
                                
        return 'atr_%d' % atributo.cod_objeto
    
    def atributo_fechadeactualizacion(self, clase):
        """Devuelve el nombre del atributo (ATR_XXXX) 'Fecha de actualización'
        correspondiente de la clase 'clase'"""
        atributo = \
            self.conector.conexion.\
                execute(self.tbl_atributos.\
                        select(and_(self.tbl_atributos.c[atri_clase] == clase,
                                    self.tbl_atributos.c[atri_tipodeatributo] == TATR_VALOR,
                                    #self.tbl_atributos.c[atributos_tipodevalor] == TVAL_FECHAYHORA,
                                    func.upper(self.tbl_atributos.c[atri_nombre]).like('FECHA DE ACTUALIZA%'))).\
                order_by(self.tbl_atributos.c.cod_objeto)).\
                fetchone()
                                
        return 'atr_%d' % atributo.cod_objeto
    
    def privilegio_clase(self, id_usuario, id_clase):
        """Devuelve el privilegio del usuario 'id_usuario' para la clase 'id_clase'"""        
        col_usuarios = Table(nombre_coleccion(cl_Usuarios), self.meta, autoload=True)
        
        clase = \
            self.conector.conexion.\
                execute(col_usuarios.\
                        select(and_(col_usuarios.c.cod_objeto == id_usuario,
                                    col_usuarios.c.cod_atributo == cod_atributo(usua_clasesdelusuario),
                                    col_usuarios.c.cod_objetoincluido == id_clase))).\
                fetchone()
                            
        if clase != None:
            return PRIVL_LECTURA_ESCRITURA
        else:
            return PRIVL_NINGUNO
        
    def privilegio_atributo(self, id_usuario, atributo):
        """Devuelve el privilegio del usuario 'id_usuario' para el atributo 'atributo'"""

        tbl_priv = Table(nombre_tabla(cl_PrivilegiosDeAtributo), self.meta, autoload=True)
        
        privilegio = \
            self.conector.conexion.\
                execute(tbl_priv.\
                        select(and_(tbl_priv.c[pda_usuariodelatributo] == id_usuario,
                                    tbl_priv.c[pda_atributo] == cod_atributo(atributo)))).\
                fetchone()
        
        if privilegio is None or privilegio[pda_niveldeprivilegio] == NIDEPR_NINGUNO:
            return PRIVL_NINGUNO
                        
        if privilegio[pda_niveldeprivilegio] == NIDEPR_LECTURA:
            return PRIVL_LECTURA
        
        elif privilegio[pda_niveldeprivilegio] == NIDEPR_LECTURA_ESCRITURA:
            return PRIVL_LECTURA_ESCRITURA
        
    def usuario_perfil(self, id_usuarioweb):
        """
        Devuelve el COD_OBJETO del usuario que es el perfil del usuario web
        'id_usuarioweb
        """
        
        tbl_uweb = Table(nombre_tabla(cl_UsuariosWeb), self.meta, autoload=True)
        
        uweb = \
            self.conector.conexion.\
            execute(tbl_uweb.\
                    select(tbl_uweb.c.cod_objeto == id_usuarioweb)).\
            fetchone()
        
        if uweb != None:            
            return uweb[uswe_usuarioperfil]
        
        else:
            return 0        
        
    def registrar_documento(self, id_usuario, fichero, extension, titulo, 
                            id_clase, id_objeto, id_tipo=None, autor=None, id_repositorio=None):
        """Registra un documento y devuelve el identificador del nuevo documento"""
                
        tbl_repositorios = Table(nombre_tabla(cl_RepositoriosDeDocumentos),
                                 self.meta, autoload=True)
        
        if id_repositorio != None:
            repositorio = \
                self.conector.conexion.\
                execute(tbl_repositorios.\
                        select(tbl_repositorios.c.cod_objeto == id_repositorio)).\
                fetchone()
                
        else:
            repositorio = \
                self.conector.conexion.\
                execute(tbl_repositorios.select().limit(1)).\
                fetchone()
                
        # formato de documento
        formato = \
            self.conector.conexion.query(FormatosDeDocumentoOlympo).\
                filter(func.upper(FormatosDeDocumentoOlympo.extension) == \
                       func.upper(extension.replace('.', ''))).\
                first()
                                
        if formato is None:            
            formato = FormatosDeDocumentoOlympo()
            formato.extension = extension.lower()
            formato.nombre = 'Archivos %s' % extension.lower()
            formato.id_usuario_usuario = id_usuario
            
            self.conector.conexion.add(formato)
            self.conector.conexion.commit()
                
        documento = DocumentosOlympo()
        documento.titulo = titulo
        documento.repositorio = repositorio.cod_objeto
        documento.formato = formato.id
        documento.id_usuarios_usuario = id_usuario
        documento.autor = autor or ''
        documento.tipo = id_tipo
        documento.version = '1'
        documento.estado = EDD_ESTABLE
        documento.privado = False
        
        self.conector.conexion.add(documento)
        self.conector.conexion.commit()
        
        id_documento = documento.id       
        
        reob = RelacionObjetosDocumentosOlympo()
        reob.id_clases_clase = id_clase
        reob.id_documentos_documento = id_documento
        reob.codigoDeObjeto = id_objeto
        
        self.conector.conexion.add(reob)
        self.conector.conexion.commit()        
                
        # guardar fichero en el repositorio                
        ruta = os.path.join(repositorio[rdd_ruta],
                            '%d%s' % (id_documento, extension.lower()))
        
        fichero_documento = file(ruta, 'wb')
        try:
            fichero_documento.write(fichero.read())
                    
        finally:
            fichero_documento.close()        
        
        return id_documento
        
    def exportar_documento(self, id_documento, ruta_destino):
        """
        Exporta el documento 'id_documento' a la carpeta 'ruta_destino' como
        <titulo del documento>.<extension> si 'ruta_destino' es un directorio,
        o utilizando 'ruta_destino' como ruta completa al fichero de salida (directorio + fichero)
        
        OUT
          La ruta completa del fichero exportado en caso de éxito o '' en otro caso
        """
        
        tbl_doc = Table(nombre_tabla(cl_Documentos), self.meta, autoload=True)
        tbl_repo = Table(nombre_tabla(cl_RepositoriosDeDocumentos), self.meta, autoload=True)
        tbl_fdd = Table(nombre_tabla(cl_FormatosDeDocumento), self.meta, autoload=True)
        
        qry_documento = \
            tbl_doc.\
            join(tbl_repo,
                 tbl_repo.c.cod_objeto == tbl_doc.c[docu_repositorio]).\
            join(tbl_fdd,
                 tbl_fdd.c.cod_objeto == tbl_doc.c[docu_formato])
            
        documento = \
            self.conector.conexion.\
                execute(select([tbl_repo.c[rdd_ruta].label('ruta_repo'),
                                tbl_doc.c.cod_objeto.label('cod_documento'),
                                tbl_doc.c[docu_titulo].label('titulo'),
                                tbl_fdd.c[fdd_extension].label('extension')],
                               from_obj=qry_documento,
                               whereclause=tbl_doc.c.cod_objeto == id_documento)).\
                fetchone()
                        
        ruta_documento = os.path.join(documento.ruta_repo, 
                                      '%d.%s' % (documento.cod_documento, 
                                                 documento.extension))
        
        if os.path.isdir(ruta_destino):
            ruta_documento_destino = os.path.join(ruta_destino, 
                                                  '%s.%s' % (documento.titulo, 
                                                             documento.extension))
        else:
            # ruta completa (dir + fichero)
            ruta_documento_destino = ruta_destino
        
        try:
            shutil.copy(ruta_documento, ruta_documento_destino)
            return ruta_documento_destino
        
        except:
            return ''
        
    def documentos_asociados(self, cod_clase, cod_objeto):
        """
        Devuelve una lista de documentos asociados al objeto indicado.
        
        IN
          cod_clase   <int>
          cod_objeto  <int>
          
        OUT
          [<int>, ...]
        """
        
        tbl_reob = Table(nombre_tabla(cl_RelacionObjetosDocumentos), self.meta, 
                         autoload=True)
        
        resultado = []
        for cod_documento in \
            self.conector.conexion.\
                execute(select([tbl_reob.c[reob_documento].label('cod_documento')],
                               from_obj=tbl_reob,
                               whereclause=and_(tbl_reob.c[reob_clase] == cod_clase,
                                                tbl_reob.c[reob_codigodeobjeto] == cod_objeto
                                                )
                               )).\
                fetchall():
            
            resultado.append(cod_documento[0])
            
        return resultado
        