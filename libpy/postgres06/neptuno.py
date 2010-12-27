# -*- coding: utf-8 -*-

import inspect
from sqlalchemy.sql.expression import select
from sqlalchemy import MetaData, Table
from sqlalchemy.types import VARCHAR, TEXT, CHAR, INTEGER, BIGINT, \
    NUMERIC, FLOAT, BOOLEAN, DATE, TIME, BINARY
from sqlalchemy.exc import NoSuchTableError, IntegrityError
from libpy.roles import RolColumnas, RolTablas
from libpy.const_datos_neptuno import PRIVL_NINGUNO, PRIVL_LECTURA, PRIVL_LECTURA_ESCRITURA, \
    CAMPOS, ETIQUETA, UTILIZAR_SELECTOR , NOMBRE, SOLO_LECTURA, REQUERIDO,\
    TIPO, VALOR, TABLA_RELACIONADA, VALORES, TYPE_DATE, TYPE_TIME, TYPE_CHAR,\
    TYPE_TEXT, TYPE_INTEGER, TYPE_REAL, TYPE_BOOLEAN, TYPE_STRING, TITULO,\
    CAMPOS_REFERENCIA
from libpy.excepciones.eneptuno import NoTienePrivilegios, NoTienePrivilegiosEscritura 
from datetime import date, time
from decimal import Decimal
from nucleo.unidadescompartidas import Usuarios

from nucleo.const_datos import ROL_COLUMNAS, ROL_TABLAS
Usuarios.privl_tabla = RolTablas(ROL_TABLAS)
Usuarios.privl_columna = RolColumnas(ROL_COLUMNAS)

try:
    from nucleo.definicion_clases import DEFINICION_CLASES
except ImportError:
    DEFINICION_CLASES = None

class Neptuno(object):
    """
    Permite "mapear" una tabla y ejecutar operaciones estándar de creación, 
    edición y borrado sobre la misma, utilizando los 'id' de los registros o 
    cadenas en forma de json.
    
    query_registro. Devuelve los datos de un registro de la tabla.
    update_registro. Crea / Actualiza un registro de la tabla.
    delete_registro. Elimina un registro de la tabla.
    """

    def __init__(self, conector, tabla, id_usuario):
        """
        IN
          conector   <conexionNeptuno>
          tabla      <str> Nombre de la tabla
          id_usuario <int> (<usuarios>) Identificador del usuario
        
          Por ejemplo,
          tbl_personal = Neptuno(conector, 'personal', 1)
        """
        
        self.conector = conector
        self.meta = MetaData(bind=conector.engine)
        self.solo_lectura = False
        
        # Comprobar que existe el usuario
        self.usuario = Usuarios.comprobar_usuario(conector, id_usuario)
        
        # Comprobar si tiene privilegios sobre esa tabla
                    
        # Si no existe definición explícita de privilegios es porque tiene privilegios "Lectura/Escritura"
        privilegio = self.usuario.getPrivilegioTabla(tabla) 
        if privilegio == PRIVL_NINGUNO:
            raise NoTienePrivilegios(self.usuario.nombre_usuario, tabla)

        # Read-only
        self.solo_lectura = privilegio == PRIVL_LECTURA
                
        self.la_tabla = Table(tabla, self.meta, autoload=True)
        
        # campo "ficticio":
        # Un campo "ficticio" tiene la forma:
        #
        # ((<nombre>, <tipo>, <valor inicial>, <callback>, [<solo-lectura>]), <etiqueta>, [<requerido>]),
        # ((<funcion>, <tipo>, <valor inicial>, <callback>, [<solo-lectura>]), <etiqueta>, [<requerido>])
        #
        # <funcion> es una función que recibe como parámetros:
        #   id <int>
        #   conector <conexionNeptuno>
        #
        # Por ejemplo:
        #
        # def una_funcion(id, conector):
        #     return {_VALOR: 'Esto es un campo calculado'}
        #
        # def otra_funcion(id, conector):
        #     return {_TABLA_RELACIONADA: '',
        #             _VALORES: [[{_NOMBRE: 'id',
        #                          _VALOR: 1,
        #                          _TIPO: const.TYPE_INTEGER},
        #                         {_NOMBRE: 'nombre',
        #                          _VALOR: 'Valor 1',
        #                          _TIPO: const.TYPE_STRING}],
        #                        [{_NOMBRE: 'id',
        #                          _VALOR: 2,
        #                          _TIPO: const.TYPE_INTEGER},
        #                         {_NOMBRE: 'nombre',
        #                          _VALOR: 'Valor 2',
        #                          _TIPO: const.TYPE_STRING}        
        #                        ]
        #                       ]
        #
        # y devuelve un diccionario con forma de "columna".
        #
        # <callback> es una función que toma tres parámetros:
        #   id <int>
        #   valor <str> -> el valor del campo "ficticio"
        #   conector <ConexionNeptuno>
        #
        # y no devuelve nada. Es una función que trata el valor del campo "ficticio".
        #
        # Por ejemplo
        #
        # def callback(id, valor, conector):
        #     objeto = conector.conexion.query(UnaClase).get(id)
        #
        #     if valor is None:
        #        return
        #
        #     valor = int(valor)
        #     if valor == 1:
        #         objeto.campo = 'Has elegido la opción 1'
        #
        #     elif valor == 2:
        #         objeto.campo = 'Has elegido la opción 2'
        #
        #
        self.campos_ficticios = []
        self.campos = []
        
        # lista de identificadores en la tabla
        if DEFINICION_CLASES.has_key(self.la_tabla.name):
            self.campos = [campo[0] for campo in DEFINICION_CLASES[self.la_tabla.name][CAMPOS]]
            
            self.campos_ficticios = [None] * len(self.campos)
            for i in xrange(len(self.campos)):
                campo = self.campos[i]
                
                # campo "ficticio"
                if isinstance(campo, tuple):
                    
                    self.campos_ficticios[i] = campo
                    
                    # (<nombre>, <tipo>, <valor de inicio>, <callback>, <solo-lectura>)
                    if isinstance(campo[0], str):
                        self.campos[i] = campo[0]
                    
                    # (<función>, <tipo>, <valor inicial>, <callback>, <solo-lectura>)       
                    elif hasattr(campo[0], '__call__'):
                        self.campos[i] = getattr(campo[0], '__name__')

    def query_registro(self, id_reg=-1, seguir_foraneas=True, **kwargs):
        """
        Devuelve una cadena en forma de JSON con los datos del registro cuyo 
        'id' es el que le pasamos como párametro.
        
        IN
          id_reg              <int> Identificador del registro => -1
          seguir_foraneas <bool> NO UTILIZAR. ES DE USO INTERNO
          
        OUT
          Un array de columnas (objetos json) de la siguiente forma:
            [{'nombre': <str>, 
              'etiqueta': <str>, 
              'valor': <str>, 
              'tipo': <str>,
              'tabla_relacionada': <str>,
              'valores' : [....], 
              'utilizar_selector': <bool>,
              'solo_lectura': <bool>,
              'requerido': <bool>
             }, 
             ...
            ]
              
            'nombre': Nombre del atributo. Por ejemplo, 'codigo_postal'
            
            'etiqueta': Nombre legible del atributo. Por ejemplo, 'Código postal'
            
            'valor': Valor de la columna. Si es nulo esta clave no estará
            
            'tipo': Tipo de la columna 
              'integer' 
              'string' 
              'text'
              'real' 
              'boolean' 
              'date'
              'time' 
              'char'
              
            'tabla_relacionada': Nombre de la tabla relacionada. 
             Sólo para las claves foráneas.
             
            'valores': Array de valores cuando no se utiliza selector. 
             Sólo para claves foráneas
             
            'utilizar_selector': True/False. Determina si se utilizará el selector 
             para buscar valores en la tabla relacionada. Sólo claves foráneas.
             
            'solo_lectura': True/False. Determina si el campo será editable o no
            
            'requerido': True/False. Determina si el campo será obligatorio o no

        Ejemplo:
        
        tbl_personal = jsonatenea(conector, 'personal')
        tbl_personal.query_registro(id_reg=100)
        
        Devuelve los datos del registro con id = 100 de la tabla 'personal'
        """
        
        POS_ETIQUETA = 1
        POS_REQUERIDO = 2 
        
        def comparar(x, y):
            if DEFINICION_CLASES != None:              
                if x[NOMBRE] in self.campos:
                    orden_x = self.campos.index(x[NOMBRE])
                else:
                    orden_x = 0
                
                if y[NOMBRE] in self.campos:
                    orden_y = self.campos.index(y[NOMBRE])
                else:
                    orden_y = 0
                    
                if orden_x > orden_y:
                    return 1
                elif orden_x == orden_y:
                    return 0
                else:
                    return -1
            else:
                return 0
        
        registro = self.la_tabla.select(whereclause=self.la_tabla.c.id == id_reg).\
                        execute().fetchone()

        resultado = []
        
        for c in self.la_tabla.columns:
            if (self.usuario.getPrivilegioColumna(self.la_tabla.name, c.name) != PRIVL_NINGUNO) and \
            (c.name != 'busqueda') and (type(c.type) != BINARY):
                columna = {}
                
                columna[NOMBRE] = c.name
                
                # Comprobar privilegios sobre la columna
                if self.usuario.getPrivilegioColumna(self.la_tabla.name, c.name) == PRIVL_LECTURA:
                    columna[SOLO_LECTURA] = True
                
                # etiqueta, requerido
                if DEFINICION_CLASES != None and c.name in self.campos:
                    el_campo = DEFINICION_CLASES[self.la_tabla.name][CAMPOS][self.campos.index(c.name)]
                    
                    # etiqueta
                    columna[ETIQUETA] = el_campo[POS_ETIQUETA]
                    
                    # requerido
                    if len(el_campo) >= POS_REQUERIDO + 1:
                        columna[REQUERIDO] = el_campo[POS_REQUERIDO]
                    else:
                        columna[REQUERIDO] = False
                         
                else:
                    columna[ETIQUETA] = columna[NOMBRE]
                    columna[REQUERIDO] = False                    

                if isinstance(c.type, DATE):
                    columna[TIPO] = TYPE_DATE
                elif isinstance(c.type, TIME):
                    columna[TIPO] = TYPE_TIME
                elif isinstance(c.type, BOOLEAN):
                    columna[TIPO] = TYPE_BOOLEAN
                elif isinstance(c.type, VARCHAR):
                    columna[TIPO] = TYPE_STRING
                elif isinstance(c.type, CHAR):
                    columna[TIPO] = TYPE_CHAR
                elif isinstance(c.type, TEXT):
                    columna[TIPO] = TYPE_TEXT
                elif isinstance(c.type, INTEGER) or isinstance(c.type, BIGINT):
                    columna[TIPO] = TYPE_INTEGER
                elif isinstance(c.type, NUMERIC) or isinstance(c.type, FLOAT):
                    columna[TIPO] = TYPE_REAL
                else:
                    columna[TIPO] = str(c.type)

                # Registro no nulo y columnas no nulas
                if not kwargs.has_key(c.name):
                    if (not registro is None) and (not registro[c.name] is None):
                        if columna[TIPO] == 'date':
                            # Formatear las fechas a 'dd/mm/yyyy'
                            columna[VALOR] = registro[c.name].strftime('%d/%m/%Y')
                        elif columna[TIPO] == 'time':
                            # Formatear las horas a 'hh:mm:ss'
                            columna[VALOR] = registro[c.name].strftime('%H:%M:%S')
                            
                        elif isinstance(registro[c.name], unicode):
                            columna[VALOR] = registro[c.name].encode('utf-8')
                            
                        else:
                            # Resto de tipos
                            columna[VALOR] = str(registro[c.name])
                else:
                    # valores definidos por defecto
                    # cuando queremos asignar valor a una columna por defecto
                    # por ejemplo, si queremos crear un grupo de un curso
                    # rellenamos el campo "id_cursos_cursodelgrupo" con el valor
                    # del curso a priori y lo hacemos de solo-lectura.
                    columna[VALOR] = str(kwargs[c.name])
                    columna[SOLO_LECTURA] = True
                
                try:
                    # Es una clave foránea?
                    clave_foranea = [k for k in self.la_tabla.foreign_keys if k.parent.name == c.name]
                    if clave_foranea != [] and seguir_foraneas:
                        key = clave_foranea[0]

                        columna[TABLA_RELACIONADA] = str(key.column.table)
                        
                        if DEFINICION_CLASES is None or \
                        not DEFINICION_CLASES.has_key(columna[TABLA_RELACIONADA]) or \
                        DEFINICION_CLASES[columna[TABLA_RELACIONADA]][UTILIZAR_SELECTOR]:
                        
                            columna[UTILIZAR_SELECTOR] = 'true'

                            # en inserción (registro = None) no calculamos el título
                            columna[TITULO] = ''                            
                            if registro:
                                titulo = DEFINICION_CLASES[columna[TABLA_RELACIONADA]].get(TITULO)
                                if titulo:
                                    if inspect.isclass(titulo):
                                        columna[TITULO] = \
                                            titulo.__title__(self.conector, 
                                                             registro[c.name])
                                        
                                    else:
                                        # calcular el título con la lista de campos
                                        if registro[c.name]:
                                            # tabla "relacionada"
                                            try:
                                                tabla_relacionada = \
                                                    Table('vista_busqueda_%s' % columna[TABLA_RELACIONADA],
                                                          self.meta, autoload=True)
                                                
                                            except NoSuchTableError:
                                                tabla_relacionada = \
                                                    Table(columna[TABLA_RELACIONADA], 
                                                          self.meta, autoload=True)
                                            
                                            registro_relacionado = \
                                                self.conector.conexion.\
                                                execute(tabla_relacionada.\
                                                        select(whereclause=tabla_relacionada.c.id == registro[c.name])).\
                                                fetchone()
                                                
                                            # calcular el título
                                            texto_titulo = []
                                            for campo_r in titulo:
                                                
                                                v = registro_relacionado[campo_r]
                                                if isinstance(v, unicode):
                                                    texto_titulo.append(v.encode('utf-8'))
                                                    
                                                else:
                                                    texto_titulo.append(str(v or ''))
                                                
                                            columna[TITULO] = (' '.join(titulo)).strip()
                                            
                                else:
                                    # no tiene definido el título
                                    try:
                                        tabla_relacionada = \
                                            Table('vista_busqueda_%s' % columna[TABLA_RELACIONADA],
                                                  self.meta, autoload=True)
                                        
                                    except NoSuchTableError:
                                        tabla_relacionada = \
                                            Table(columna[TABLA_RELACIONADA], 
                                                  self.meta, autoload=True)
                                    
                                    if registro[c.name]:
                                        for col_r in tabla_relacionada.columns: 
                                            if not col_r.name.startswith('id'):
                                                registro_relacionado = \
                                                    self.conector.conexion.\
                                                        execute(tabla_relacionada.\
                                                                select(tabla_relacionada.c.id == registro[c.name])).\
                                                        fetchone()
                                                        
                                                v = registro_relacionado[col_r.name]
                                                if isinstance(v, unicode):
                                                    columna[TITULO] = (v.encode('utf-8')).strip()
                                                else:
                                                    columna[TITULO] = str(v or '').strip()
                                                    
                                                break
                                            
                            # campos de referencia
                            campos_ref = DEFINICION_CLASES[columna[TABLA_RELACIONADA]].get(CAMPOS_REFERENCIA)
                            if campos_ref:
                                columna[CAMPOS_REFERENCIA] = campos_ref
                                    
                            else:
                                # coger primera columna que no empiece por 'id' de la vista
                                try:
                                    tabla_relacionada = Table('vista_busqueda_%s' % columna[TABLA_RELACIONADA],
                                                              self.meta, autoload=True)
                                    
                                except NoSuchTableError:
                                    tabla_relacionada = \
                                        Table(columna[TABLA_RELACIONADA], self.meta, autoload=True)
                                        
                                for col_r in tabla_relacionada.columns: 
                                    if not col_r.name.startswith('id'):
                                        if isinstance(col_r.name, unicode):
                                            columna[CAMPOS_REFERENCIA] = [col_r.name.encode('utf-8')]
                                        else:
                                            columna[CAMPOS_REFERENCIA] = [str(col_r.name)]
                                            
                                        break

                        else:
                            try:
                                tabla_busqueda = \
                                    Table('vista_busqueda_%s' % columna[TABLA_RELACIONADA], 
                                          self.meta, autoload=True)
                            except NoSuchTableError:
                                tabla_busqueda = \
                                    Table(columna[TABLA_RELACIONADA], self.meta, 
                                          autoload=True)                                                                    
                                
                            tbl_relacionada = \
                                Neptuno(self.conector, columna[TABLA_RELACIONADA], 
                                        self.usuario.id)
    
                            resultado_tabla_relacionada = []
                            for fila in tabla_busqueda.select().execute():                                        
                                fila_resultado = tbl_relacionada.\
                                    query_registro(id_reg=fila['id'], 
                                                   seguir_foraneas=False)
                                
                                resultado_tabla_relacionada.append(fila_resultado)
    
                            columna[VALORES] = resultado_tabla_relacionada
                
                except NoTienePrivilegios:                    
                    # No tiene privilegios sobre la tabla relacionada, no puede acceder al campo que hace referencia a ella                    
                    columna = None
                                                   
                if not columna is None:
                    resultado.append(columna)
                    
        if self.campos_ficticios:
            for i in xrange(len(self.campos_ficticios)):
                campo = self.campos_ficticios[i]
                if campo != None:
                    el_campo = DEFINICION_CLASES[self.la_tabla.name][CAMPOS][i]
                    
                    if isinstance(campo[0], str):
                        
                        columna = {}
                        columna[NOMBRE] = campo[0]
                        
                    elif hasattr(campo[0], '__call__'):
                        
                        funcion = campo[0]
                        columna = funcion(id_reg, self.conector)
                        columna[NOMBRE] = getattr(funcion, '__name__')
                    
                    # valor inicial
                    if not columna.has_key(VALOR):
                        columna[VALOR] = campo[2]
                        
                    columna[TIPO] = campo[1]
                    columna[ETIQUETA] = el_campo[POS_ETIQUETA]
                    
                    # sólo-lectura
                    if len(campo) > 4:
                        columna[SOLO_LECTURA] = campo[4]
                        
                    # requerido
                    columna[REQUERIDO] = False
                    if len(el_campo) > 2:
                        columna[REQUERIDO] = el_campo[2]
                    
                    resultado.append(columna)
                        
        return sorted(resultado, comparar)
    
    def convertir_valor(self, valor, tipo):
        
        if tipo == TYPE_BOOLEAN:
            return valor.lower() == 'true'
        
        elif tipo == TYPE_CHAR or tipo == TYPE_STRING or tipo == TYPE_TEXT:
            return valor
        
        elif tipo == TYPE_DATE:
            pass
        
        elif tipo == TYPE_INTEGER:
            return int(valor)
        
        elif tipo == TYPE_REAL:
            return float(valor)
        
        elif tipo == TYPE_TIME:
            pass

    def update_registro(self, json_registro):
        """
        Actualiza un registro de la tabla asignada al objeto "Neptuno"
        json_registro = diccionario que contiene los datos para crear / actualizar. 
        Si en esos datos no hay id o es -1 se creará un registro. En otro caso, 
        se actualizará el registro cuyo id es el que está contenido en
        el diccionario de entrada.
        
        Devuelve el 'id' del registro creado o actualizado, o -1 en caso de error.
        
        ejemplo de actualización:
        tbl_personal = Neptuno(conector, 'personal')        
        json_registro = {"id": 1000, "nombre": "Paco", "apellido1": "Fernández"}
        tbl_personal.update_registro(json_registro)
        
        De este modo actualizamos el registro con 'id' = 1000 con el 'nombre' = 
        'Paco' y el 'apellido1' = 'Fernández'
        
        ejemplo de inserción:        
        tbl_personal = Neptuno(conector, 'personal')        
        json_registro = {"nombre":"Paco", "apellido1": "Fernández"}
        tbl_personal.update_registro(json_registro)
        
        Se creará un nuevo registro con 'nombre'='Paco' y 'apellido1'='Fernández'
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
                                
            if update.has_key('id') and update['id'] != -1:
                # Actualizar'
                self.la_tabla.update(whereclause=self.la_tabla.c.id == int(update['id']), 
                                     values=update).execute()
                id_reg = int(update['id'])
            else:
                # Insertar
                if update.has_key('id'):
                    del update['id']
                
                nuevo_registro = self.la_tabla.insert(values=update).execute()
                id_reg = nuevo_registro.last_inserted_ids()[0]
                
            # campos "ficticios"
            if self.campos_ficticios:
                for campo in [cf for cf in self.campos_ficticios 
                              if cf != None and cf[3] != None]: 
                    callback = campo[3]
                    
                    nombre = campo[0]
                    if hasattr(nombre, '__call__'):
                        nombre = getattr(nombre, '__name__')
                    
                    callback(id_reg, update[nombre], self.conector)
                
            return id_reg            
            
        except IntegrityError:
            raise
        
        else:
            return -1
        
    def delete_registro(self, id_reg):
        """
        Borra un registro de la tabla cuyo identificador es 'id'. Devuelve True en 
        caso de borrar con éxito el registro, o False en caso contrario.
        IN
          id_reg  <int> -> Identificador del registro
        """
        
        if self.solo_lectura:
            raise NoTienePrivilegiosEscritura(self.usuario.nombre_usuario, self.la_tabla.name)

        try:
            self.la_tabla.\
                delete(whereclause=self.la_tabla.c.id == id_reg).\
                execute()
                
            return True
        
        except IntegrityError:
            raise
        
    def query_tabla(self):
        """
        Devuelve una lista de todos los registros de la tabla. Cada uno de ellos 
        tal y como lo devuelve 'query_registro'.
        
        OUT
          Un array de arrays de diccionarios de la forma:
          [[{"nombre": "id", "etiqueta": "id", "tipo": "integer", "valor": "1"}, ...], ...]
        """
        
        resultado = []
        for row in self.conector.conexion.execute(select([self.la_tabla.c.id])):
            registro = self.query_registro(row[self.la_tabla.c.id])
            resultado.append(registro)
            
        return resultado
    
    def raw_data(self, id_reg, campos):
        """
        IN
          campos [<str>, ...]
          
        OUT
          {<campo1>, <campo2>, ...}
        """
        
        registro = self.la_tabla.select(whereclause=self.la_tabla.c.id == id_reg).\
                        execute().fetchone()
                    
        def format_value(value):
            if isinstance(value, date):
                return value.strftime('%d/%m/%Y')
            
            elif isinstance(value, time):
                return value.strftime('%H:%M:%S')
            
            elif isinstance(value, Decimal):
                return '%2.2f' % value
            
            else:
                return value
        
        # si "campos" está vacío utilizamos todas las columnas
        if not campos:
            campos = [c.name for c in self.la_tabla.columns]
            
        data = {}
        for c in campos:
            if self.la_tabla.columns.has_key(c):
                data[c] = format_value(registro[c])

        return data