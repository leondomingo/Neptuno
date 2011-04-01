# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import select, and_
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import IntegrityError #, NoSuchTableError,
from unidadescompartidasNeptuno import usuariosNeptuno
from libpy.roles import RolTablas, RolColumnas
from libpy.const_datos_neptuno import PRIVL_NINGUNO, PRIVL_LECTURA, PRIVL_LECTURA_ESCRITURA, \
                                    ETIQUETA, UTILIZAR_SELECTOR , COD_CLASE,\
    NOMBRE, SOLO_LECTURA, TIPO, TYPE_DATE, TYPE_TIME, TYPE_BOOLEAN, TYPE_STRING,\
    TYPE_CHAR, TYPE_TEXT, TYPE_REAL, TYPE_INTEGER, VALORES, TABLA_RELACIONADA,\
    VALOR
from libpy.excepciones.eneptuno import NoTienePrivilegios, NoTienePrivilegiosEscritura
from util import nombre_tabla, cod_clase
from sqlalchemy.databases.firebird import FBDate, FBTime, FBBoolean, FBString,\
    FBChar, FBText, FBNumeric, FBFloat, FBInteger, FBBinary, FBDateTime
from libpy.firebird.gestorolympo import GestorOlympo
from libpy.firebird.const_datos_olympo import TATR_COLECCION,\
    NIDEPR_LECTURA, NIDEPR_LECTURA_ESCRITURA, NIDEPR_NINGUNO
from libpy.firebird.util import cod_objeto
from datetime import datetime
from const_olympo import atributos_nombre
from libpy.firebird.const_olympo import cl_Atributos,\
    atributos_clase, cl_PrivilegiosDeAtributo,\
    privilegiosdeatributo_usuariodelatributo,\
    privilegiosdeatributo_niveldeprivilegio, privilegiosdeatributo_atributo,\
    atributos_tipodeatributo

try:
    from definicion_clases import DEFINICION_CLASES
except ImportError:
    DEFINICION_CLASES = None

from nucleo.const_datos import ROL_TABLAS, ROL_COLUMNAS
usuariosNeptuno.privl_tabla = RolTablas(ROL_TABLAS)
usuariosNeptuno.privl_columna = RolColumnas(ROL_COLUMNAS)

class Neptuno(object):
    """
    Permite 'mapear' una clase y ejecutar operaciones estándar de creación, 
    edición y borrado sobre la misma, utilizando los 'id' de los registros o 
    cadenas en forma de json.
    
    query_registro. Devuelve los datos de un registro de la tabla.
    update_registro. Crea / Actualiza un registro de la tabla.
    delete_registro. Elimina un registro de la tabla.
    """

    def __init__(self, conector, tabla, id_usuario):
        """
        Inicializa un objeto 'Neptuno'.
        
        IN
          conector = <conexionNeptuno>
          tabla = cadena con el nombre de la tabla <str>
          id_usuario <int>
                  
          Por ejemplo,
          tbl_personal = Neptuno(conector, 'personal', 1)
        """
        
        self.conector = conector
        self.gestor = GestorOlympo(conector)
        self.meta = MetaData(bind=conector.engine)
        self.solo_lectura = False
        
        # Comprobar que existe el usuario
        self.usuario = usuariosNeptuno.comprobar_usuario(conector, id_usuario)
        
        self.cod_clase = DEFINICION_CLASES[tabla][COD_CLASE]
            
        # Comprobar si tiene privilegios sobre esa tabla        
        privilegio = self.gestor.privilegio_clase(self.usuario.id_usuarios_usuarioperfil, self.cod_clase)
        if privilegio == PRIVL_NINGUNO:
            raise NoTienePrivilegios(self.usuario.nombredeusuario, 'tabla')
        
        # no hay privilegio de lectura sobre una tabla en Olympo
        # Read-only
        self.solo_lectura = privilegio == PRIVL_LECTURA
                
        self.la_tabla = Table(nombre_tabla(self.cod_clase), self.meta,
                              cod_objeto(self.cod_clase), autoload=True)
        
        # obtener los atributos 'usuario', 'fecha de creación' y 'fecha de actualización'
        self.atr_usuario = self.gestor.atributo_usuario(self.cod_clase).lower()
        self.atr_f_creacion = self.gestor.atributo_fechadecreacion(self.cod_clase).lower()
        self.atr_f_actualizacion = self.gestor.atributo_fechadeactualizacion(self.cod_clase).lower()
        
        self.atributos_estandar = ['cod_objeto', self.atr_usuario, self.atr_f_creacion, self.atr_f_actualizacion]
        
        tbl_atributos = Table(nombre_tabla(cl_Atributos), self.meta, autoload=True)
        tbl_privil = Table(nombre_tabla(cl_PrivilegiosDeAtributo), self.meta, autoload=True)
                
        self.campos = []
        self.etiquetas = []
        self.atributos_coleccion = []
        self.privilegios = []
        for atributo in \
                tbl_atributos.\
                    outerjoin(tbl_privil,
                              and_(tbl_privil.c[privilegiosdeatributo_atributo] == tbl_atributos.c.cod_objeto,
                                   tbl_privil.c[privilegiosdeatributo_usuariodelatributo] == self.usuario.id_usuarios_usuarioperfil)).\
                    select(tbl_atributos.c[atributos_clase] == self.cod_clase, use_labels=True).\
                    execute():
            
            nombre_columna = 'atr_%d' % atributo[tbl_atributos.c.cod_objeto]
            if not nombre_columna in self.atributos_estandar:
                self.etiquetas.append(atributo[tbl_atributos.c[atributos_nombre]])
                self.campos.append(nombre_columna)
                
                if atributo[tbl_atributos.c[atributos_tipodeatributo]] == TATR_COLECCION:
                    self.atributos_coleccion.append(nombre_columna)
                    
                # privilegio de cada atributo
                priv = atributo[tbl_privil.c[privilegiosdeatributo_niveldeprivilegio]]
                
                if priv == NIDEPR_NINGUNO or priv is None:
                    priv = PRIVL_NINGUNO
                
                elif priv == NIDEPR_LECTURA:
                    priv = PRIVL_LECTURA
                
                elif priv == NIDEPR_LECTURA_ESCRITURA:
                    priv = PRIVL_LECTURA_ESCRITURA
                                
                self.privilegios.append(priv)

    def query_registro(self, id=-1, seguir_foraneas=True):
        """
        Devuelve una cadena en forma de 'json' con los datos del registro cuyo 'id' es el que le pasamos como párametro.
        id = Identificador del registro (int). Por defecto es igual a -1.
        
        IN
          id = identificador del registro
          seguir_foraneas = NO UTILIZAR. ES DE USO INTERNO
          
        OUT
          Un array de columnas (objetos json) de la siguiente forma:
            [{'nombre': '___', 'etiqueta': '_____', 'valor': '____', 'tipo': '_____', 'tabla_relacionada': '_____',
              'valores' : [....], 'utilizar_selector': True/False}, ....]
              
            'nombre': Nombre del atributo. Por ejemplo, 'codigo_postal'
            'etiqueta': Nombre legible del atributo. Por ejemplo, 'Código postal'
            'valor': Valor de la columna. Si es nulo esta clave no estará
            'tipo': Tipo de la columna ('integer', 'string', 'text', 'real', 'boolean', 'date', 'time', 'char')
            'tabla_relacionada': Nombre de la tabla relacionada. Sólo para las claves foráneas.
            'valores': Array de valores cuando no se utiliza selector. Sólo para claves foráneas
            'utilizar_selector': True/False. Determina si se utilizará el selector para buscar valores en la tabla relacionada. Sólo claves foráneas.

        Ejemplo:
        
        tbl_personal = jsonatenea(conector, 'personal')
        tbl_personal.query_registro(id=100)
        
        Devuelve los datos del registro con id = 100 de la tabla 'personal'
        """       
        
#        def comparar(x, y):
#            if DEFINICION_CLASES != None:
#                
#                if x[_NOMBRE] in self.campos:
#                    orden_x = self.campos.index(x[_NOMBRE])
#                else:
#                    orden_x = 0
#                    
#                if y[_NOMBRE] in self.campos:
#                    orden_y = self.campos.index(y[_NOMBRE])
#                else:
#                    orden_y = 0
#                                
#                if orden_x > orden_y:
#                    return 1
#                elif orden_x == orden_y:
#                    return 0
#                else:
#                    return -1
#            else:
#                return 0

        registro = self.conector.conexion.\
                    execute(self.la_tabla.\
                            select(self.la_tabla.c.cod_objeto == id)).fetchone() 
        
        resultado = []
        
        for c in self.la_tabla.columns:
            
            try:
                i = self.campos.index(c.name)
                privilegio = self.privilegios[i]
            except ValueError: 
                privilegio = PRIVL_LECTURA_ESCRITURA
                
            if privilegio != PRIVL_NINGUNO and not isinstance(c.type, FBBinary):
                
                columna = {}                
                columna[NOMBRE] = c.name
                
                # Comprobar privilegios sobre la columna
                if privilegio == PRIVL_LECTURA:
                    columna[SOLO_LECTURA] = True                  
                
                if c.name in self.campos:
                    columna[ETIQUETA] = self.etiquetas[i]
                else:
                    # renombrar "COD_OBJETO" por "id"
                    if columna[NOMBRE].upper() == 'COD_OBJETO':
                        columna[NOMBRE] = 'id'
                        columna[ETIQUETA] = 'id'
                        
                    elif columna[NOMBRE] in self.atributos_estandar:
                        # los atributos "usuario", "fecha de creación" y "fecha de actualización" son obviados 
                        continue

                # tipos
                if isinstance(c.type, FBDate):
                    columna[TIPO] = TYPE_DATE
                    
                elif isinstance(c.type, FBTime):
                    columna[TIPO] = TYPE_TIME
                    
                elif isinstance(c.type, FBDateTime):
                    columna[TIPO] = 'datetime'
                    
                elif isinstance(c.type, FBBoolean):
                    columna[TIPO] = TYPE_BOOLEAN
                    
                elif isinstance(c.type, FBString):
                    columna[TIPO] = TYPE_STRING
                    
                elif isinstance(c.type, FBChar):
                    columna[TIPO] = TYPE_CHAR
                    
                elif isinstance(c.type, FBText):
                    columna[TIPO] = TYPE_TEXT
                    
                elif isinstance(c.type, FBInteger):
                    columna[TIPO] = TYPE_INTEGER
                    
                elif isinstance(c.type, FBNumeric) or isinstance(c.type, FBFloat):
                    columna[TIPO] = TYPE_REAL
                    
                else:
                    columna[TIPO] = str(c.type)

                # Registro no nulo y columnas no nulas
                if (not registro is None) and (not registro[c.name] is None):
                    if columna[TIPO] == 'date':
                        # Formatear las fechas a 'dd/mm/yyyy'
                        columna[VALOR] = registro[c.name].strftime('%d/%m/%Y')
                        
                    elif columna[TIPO] == 'time':
                        # Formatear las horas a 'hh:mm:ss'
                        columna[VALOR] = registro[c.name].strftime('%H:%M:%S')
                        
                    elif columna[TIPO] == 'datetime':
                        columna[VALOR] = registro[c.name].strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        # Resto de tipos
                        
                        # campos de tipo cadena en Unicode
                        if isinstance(registro[c.name], unicode):
                            columna[VALOR] = registro[c.name].encode('utf-8')
                        
                        # campos MEMO (BLOB)
                        elif columna[TIPO] == 'text':                            
                            columna[VALOR] = registro[c.name].decode('iso-8859-1').encode('utf-8')
                            
                        # resto de campos
                        else:
                            columna[VALOR] = str(registro[c.name]).encode('utf-8')
                                            
                try:
                    # atributos de tipo "colección"
                    if c.name in self.atributos_coleccion and seguir_foraneas:
                        tbl_enlazada = self.gestor.clase_enlazada(c.name)
                        columna[TABLA_RELACIONADA] = tbl_enlazada.name
                        
                        cod_clase_enlazada = cod_clase(columna[TABLA_RELACIONADA])
                        if DEFINICION_CLASES is None or DEFINICION_CLASES[cod_clase_enlazada][UTILIZAR_SELECTOR]:
                            columna[UTILIZAR_SELECTOR] = 'true'
                        else:
                            # para tablas pequeñas no utilizamos selector, sólo un desplegable
                            tbl_relacionada = Neptuno(self.conector, cod_clase_enlazada, self.usuario.id)
                            
                            resultado_tabla_relacionada = []
                            for fila in tbl_enlazada.select().execute():
                                fila_resultado = tbl_relacionada.query_registro(fila.cod_objeto, seguir_foraneas=False)
                                resultado_tabla_relacionada.append(fila_resultado)
                                
                            columna[VALORES] = resultado_tabla_relacionada

                except NoTienePrivilegios:                    
                    # No tiene privilegios sobre la tabla relacionada, no puede acceder al campo que hace referencia a ella                    
                    continue

                resultado.append(columna)
        
        return resultado #sorted(resultado, comparar)

    def update_registro(self, json_registro):
        """
        Actualiza un registro de la tabla asignada al objeto 'jsonatenea'
        json_registro = diccionario (json) que contiene los datos para crear / actualizar. Si en esos datos
        no hay id (o es -1) se creará un registro. En otro caso, se actualizará el registro cuyo id es el que está contenido en
        el json de entrada.
        
        Devuelve el 'id' del registro creado o actualizado, o -1 en caso de error.
        
        ejemplo de actualización:
        tbl_personal = Neptuno(conector, 'personal')        
        json_registro = {"id": 1000, "nombre": "Paco", "apellido1": "Fernández"}
        tbl_personal.update_registro(json_registro)
        
        De este modo actualizamos el registro con 'id' = 1000 con el 'nombre' = 'Paco' y el 'apellido1' = 'Fernández'
        
        ejemplo de inserción:        
        tbl_personal = Neptuno(conector, 'personal')        
        json_registro = {"nombre":"Paco", "apellido1": "Fernández"}
        tbl_personal.update_registro(json_registro)
        
        Se creará un nuevo registro con 'nombre' = 'Paco' y 'apellido1' = 'Fernández'
        """
        
        if self.solo_lectura:
            raise NoTienePrivilegiosEscritura(self.usuario.nombre_usuario, self.la_tabla.name)
        
        try:
            registro = json_registro 
            
            # Quitar del registro los campos que no tengan privilegios de lectura/escritura
            update = {}
            for campo, valor in registro.iteritems():
                if self.usuario.getPrivilegioColumna(self.la_tabla.name, campo) == PRIVL_LECTURA_ESCRITURA:
                    update[campo] = valor
            
            # rellenar 'usuario' y 'fecha de actualización'        
            update[self.atr_usuario] = self.usuario.id_usuarios_usuarioperfil
            update[self.atr_f_actualizacion] = datetime.now()                    

            if update.has_key('id') and update['id'] != -1:
                # Actualizar'
                self.la_tabla.update(whereclause=self.la_tabla.c.cod_objeto == int(update['id']), 
                                     values=update).execute()
                                                         
                return int(update['id'])
            else:
                # Insertar
                if update.has_key('id'):
                    del update['id']
                
                # rellenar 'fecha de creación'
                update[self.atr_f_creacion] = datetime.now()                                                
                nuevo_registro = self.la_tabla.insert(values=update).execute()
                return nuevo_registro.last_inserted_ids()[0]
            
        except IntegrityError:
            raise

        else:
            return -1
        
    def delete_registro(self, id):
        """
        Borra un registro de la tabla cuyo identificador es 'id'. Devuelve True en 
        caso de borrar con éxito el registro, o False en caso contrario.
        id = int
        """
        
        if self.solo_lectura:
            raise NoTienePrivilegiosEscritura(self.usuario.nombre_usuario, self.la_tabla.name)

        try:
            self.la_tabla.delete(whereclause=self.la_tabla.c.cod_objeto == id).execute()
            return True
        except IntegrityError:
            raise
        
    def query_tabla(self, limite=None):
        """
        Devuelve una lista de todos los registros de la tabla. Cada uno de ellos 
        tal y como lo devuelve 'query_registro'.
        
        Salida:
            Un json de la forma:
            [[{"nombre": "id", "etiqueta": "id", "tipo": "integer", "valor": "1"}, ...], ...]
        """
        
        resultado = []
        for row in self.conector.conexion.\
                    execute(select([self.la_tabla.c.cod_objeto]).limit(limite)):
            registro = self.query_registro(row.cod_objeto)
            resultado.append(registro)
            
        return resultado