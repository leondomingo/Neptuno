# -*- coding: utf-8 -*-
from sqlalchemy.schema import MetaData, Table
from sqlalchemy import func
from libpy.firebird.util import nombre_tabla
from libpy.firebird.const_olympo import cl_Clases, cl_Atributos,\
    clases_nombre, atributos_clase, atributos_nombre
from sqlalchemy.sql.expression import and_
from libpy.firebird.gestorolympo import GestorOlympo
from libpy.conexion import Conexion
import re

class SQLParser(object):
    
    def __init__(self, conector):
        """__init__(self, conector <conexionNeptuno>)""" 
        
        self.conector = conector      
        self.meta = MetaData(bind=self.conector.engine)
        
        self.gestor = GestorOlympo(conector)
        
        self.tbl_clases = Table(nombre_tabla(cl_Clases), self.meta, autoload=True)
        self.tbl_atrib = Table(nombre_tabla(cl_Atributos), self.meta, autoload=True)
        
        self.alias = []
        self.clases = []
        
    def extraer_alias(self, query):
        
        # --# --- = ---------------
        # --# aeg = alumnos en grupos
        
        m = re.search(r'--#\s*[A-Za-z0-9_]+\s*=\s*[\w _]+\n', query, re.UNICODE)
        while m != None:
            
            m_alias = re.search(r'--#\s*[A-Za-z0-9_]+\s*=', m.group(0), re.UNICODE)
            m_clase = re.search(r'=\s*[\w _]+\n', m.group(0), re.UNICODE)
            
            self.alias.append(m_alias.group(0)[3:-1].strip())
            self.clases.append(m_clase.group(0)[1:].strip().lower())
            
            query = query[:m.start()] + query[m.end():]
            
            m = re.search(r'--#\s*[A-Za-z0-9_]+\s*=\s*[\w _]+\n', query[m.start()], re.UNICODE)
            
        return query
                
    def traducir_columnas(self, query):
        
        # {------[----].-----}
        # {------[----]_xx.------}
        # {Atributos[Clase].Nombre}
        # {Clases[Usuario]_2.Nombre}
        
        prefijo = ''
        
        m = re.search(r'\{\w[^\t\r\n\f\v\{]*\[\w[^\t\r\n\f\v\}]*\](\B|_[0-9]+)\.\w[^\t\r\n\f\v\}]*\}',
                      query, re.UNICODE)
        while m != None:
            
            m_clase = re.search(r'\{\w[^\t\r\n\f\v\{]*\[', m.group(0), re.UNICODE)
            clase = m_clase.group(0)[1:-1]
            clase = self.tiene_alias(clase).decode('utf-8').upper()
            
            m_atr1 = re.search(r'\[\w[^\t\r\n\f\v\}]*\](\B|_[0-9]+)', m.group(0), re.UNICODE)
            
            numero = None
            if m_atr1.group(0)[-1] == ']':
                atributo1 = m_atr1.group(0)[1:-1].decode('utf-8').upper()           
            else:
                i = m_atr1.group(0).rfind(']') 
                atributo1 = m_atr1.group(0)[1:i].decode('utf-8').upper()
                
                numero = m_atr1.group(0)[i+1:]                
            
            m_atr2 = re.search(r'\.\w[^\t\r\n\f\v\{\}]*\}', m.group(0), re.UNICODE)
            atributo2 = m_atr2.group(0)[1:-1].decode('utf-8').upper()
            
            # buscar correspondencia
            cod_atributo = self.conector.conexion.\
                execute(self.tbl_atrib.\
                        join(self.tbl_clases,
                             and_(self.tbl_clases.c.cod_objeto == self.tbl_atrib.c[atributos_clase],
                                  func.upper(self.tbl_clases.c[clases_nombre]) == clase,
                                  func.upper(self.tbl_atrib.c[atributos_nombre]) == atributo1)).\
                        select(use_labels=True)).\
                        fetchone()
                        
            if cod_atributo != None:
                
                cod_atributo = cod_atributo[self.tbl_atrib.c.cod_objeto]
                            
                cod_clase_enlazada = self.gestor.cod_clase_enlazada(cod_atributo)
                
                if atributo2 != u'COD_OBJETO':
                
                    cod_atributo_enlazado = self.conector.conexion.\
                            execute(self.tbl_atrib.\
                                    select(and_(self.tbl_atrib.c[atributos_clase] == cod_clase_enlazada,
                                                func.upper(self.tbl_atrib.c[atributos_nombre]) == atributo2))).\
                            fetchone()
                            
                    if cod_atributo_enlazado != None:
                        
                        cod_atributo_enlazado = cod_atributo_enlazado.cod_objeto                                       
                        
                        # sustituir            
                        query = query[:m.start()] + \
                            ('REL_%d%s.ATR_%d' % (cod_atributo,
                                                  (numero if numero != None else ''), 
                                                  cod_atributo_enlazado)) + \
                            query[m.end():]
                        
                    else:
                        prefijo = prefijo + query[:m.end()]
                        query = query[m.end():]
                
                else:
                    query = query[:m.start()] + \
                        ('REL_%d.COD_OBJETO' % cod_atributo) + \
                        query[m.end():]
                        
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]
            
            m = re.search(r'\{\w[^\t\r\n\f\v\{]*\[\w[^\t\r\n\f\v\}]*\](\B|_[0-9]+)\.\w[^\t\r\n\f\v\}]*\}',
                          query, re.UNICODE)
        
        query = prefijo + query        
    
        # {----------.---------}
        # {Vistas personalizadas.Nombre}
        prefijo = ''
        m = re.search(r'\{\w[^\t\r\n\f\v\{\[\]]*\.\w[^\t\r\n\f\v\}]*\}', query, re.UNICODE)
        while m != None:
            
            m_clase = re.search(r'\{\w[^\t\r\n\f\v\{\[\]]*\.', m.group(0), re.UNICODE)
            clase = m_clase.group(0)[1:-1].decode('utf-8')
            clase = self.tiene_alias(clase).decode('utf-8').upper()
            
            m_atr = re.search(r'\.\w[^\t\r\n\f\v\}]*\}', m.group(0), re.UNICODE)
            atributo = m_atr.group(0)[1:-1].decode('utf-8').upper()
            
            cod_clase = self.conector.conexion.\
                    execute(self.tbl_clases.\
                            select(func.upper(self.tbl_clases.c[clases_nombre]) == clase)).\
                    fetchone()
                    
            if cod_clase != None:            
                cod_clase = cod_clase.cod_objeto
                
                if atributo != u'COD_OBJETO':
                    
                    cod_atributo = self.conector.conexion.\
                            execute(self.tbl_atrib.\
                                    select(and_(self.tbl_atrib.c[atributos_clase] == cod_clase,
                                                func.upper(self.tbl_atrib.c[atributos_nombre]) == atributo))).\
                            fetchone()
                            
                    if cod_atributo != None:
                        cod_atributo = cod_atributo.cod_objeto
                        
                        query = query[:m.start()] + ('OBJ_%d.ATR_%d' % (cod_clase, cod_atributo)) + query[m.end():]
                        
                    else:
                        prefijo = prefijo + query[:m.end()]
                        query = query[m.end():]
                
                else:
                    query = query[:m.start()] + ('OBJ_%d.COD_OBJETO' % cod_clase) + query[m.end():]
                    
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]                    

            m = re.search(r'\{\w[^\t\r\n\f\v\{\[\]]*\.\w[^\t\r\n\f\v\}]*\}', query, re.UNICODE)
        
        query = prefijo + query                
        return query
    
    def traducir_columnas_sin_clase(self, query):
        
        # .{----------.---------}
        # .{Vistas personalizadas.Nombre}
        prefijo = ''
        m = re.search(r'\.\{\w[^\t\r\n\f\v\{\[\]]*\.\w[^\t\r\n\f\v\}]*\}', query, re.UNICODE)
        while m != None:
            
            m_clase = re.search(r'\.\{\w[^\t\r\n\f\v\{\[\]]*\.', m.group(0), re.UNICODE)
            clase = m_clase.group(0)[2:-1]
            clase = self.tiene_alias(clase).decode('utf-8').upper()
            
            m_atr = re.search(r'\.\w[^\t\r\n\f\v\}]*\}', m.group(0), re.UNICODE)
            atributo = m_atr.group(0)[1:-1].decode('utf-8').upper()
            
            cod_clase = self.conector.conexion.\
                    execute(self.tbl_clases.\
                            select(func.upper(self.tbl_clases.c[clases_nombre]) == clase)).\
                    fetchone()
                    
            if cod_clase != None:            
                cod_clase = cod_clase.cod_objeto
                
                cod_atributo = self.conector.conexion.\
                        execute(self.tbl_atrib.\
                                select(and_(self.tbl_atrib.c[atributos_clase] == cod_clase,
                                            func.upper(self.tbl_atrib.c[atributos_nombre]) == atributo))).\
                        fetchone()
                        
                if cod_atributo != None:
                    cod_atributo = cod_atributo.cod_objeto
                    
                    query = query[:m.start()] + ('ATR_%d' % cod_atributo) + query[m.end():]
                    
                else:
                    prefijo = prefijo + query[:m.end()]
                    query = query[m.end():]
                    
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]                    

            m = re.search(r'\.\{\w[^\t\r\n\f\v\{\[\]]*\.\w[^\t\r\n\f\v\}]*\}', query, re.UNICODE)
        
        query = prefijo + query                
        return query
        
    def traducir_clases(self, query):
        
        # {-----------}
        # {Vistas personalizadas}
        prefijo = ''
        m = re.search(r'\{\w[^\t\r\n\f\v\{\[\.]*\}', query, re.UNICODE)
        while m != None:
            
            clase = m.group(0)[1:-1]            
            clase = self.tiene_alias(clase).decode('utf-8').upper()            
            
            cod_clase = self.conector.conexion.\
                execute(self.tbl_clases.\
                        select(func.upper(self.tbl_clases.c[clases_nombre]) == clase)).\
                fetchone()
                
            if cod_clase != None:            
                cod_clase = cod_clase.cod_objeto
                
                query = query[:m.start()] + ('OBJ_%d' % cod_clase) + query[m.end():]
                
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]
            
            m = re.search(r'\{\w[^\t\r\n\f\v\{\[\.]*\}', query, re.UNICODE)
            
        query = prefijo + query
        return query
    
    def traducir_colecciones(self, query):
        
        # *{-----------}
        # *{Vistas personalizadas}
        prefijo = ''
        m = re.search(r'\*\{\w[^\t\r\n\f\v\{\[\.]*\}', query, re.UNICODE)
        while m != None:
            
            clase = m.group(0)[2:-1]            
            clase = self.tiene_alias(clase).decode('utf-8').upper()           
            
            cod_clase = self.conector.conexion.\
                execute(self.tbl_clases.\
                        select(func.upper(self.tbl_clases.c[clases_nombre]) == clase)).\
                fetchone()
                
            if cod_clase != None:            
                cod_clase = cod_clase.cod_objeto
                
                query = query[:m.start()] + ('COL_%d' % cod_clase) + query[m.end():]
                
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]
            
            m = re.search(r'\*\{\w[^\t\r\n\f\v\{\[\.]*\}', query, re.UNICODE)
            
        query = prefijo + query
        return query

    def traducir_generadores(self, query):
        
        # +{-----------}
        # +{Vistas personalizadas}
        prefijo = ''
        m = re.search(r'\+\{\w[^\t\r\n\f\v\{\[\.]*\}', query, re.UNICODE)
        while m != None:
            
            clase = m.group(0)[2:-1]            
            clase = self.tiene_alias(clase).decode('utf-8').upper()            
            
            cod_clase = self.conector.conexion.\
                execute(self.tbl_clases.\
                        select(func.upper(self.tbl_clases.c[clases_nombre]) == clase)).\
                fetchone()
                
            if cod_clase != None:            
                cod_clase = cod_clase.cod_objeto
                
                query = query[:m.start()] + ('GEN_%d' % cod_clase) + query[m.end():]
            
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]
            
            m = re.search(r'\+\{\w[^\t\r\n\f\v\{\[\.]*\}', query, re.UNICODE)
            
        query = prefijo + query
        return query

    
    def tiene_alias(self, clase):
        if clase.lower() in self.alias:
            return self.clases[self.alias.index(clase.lower())]
        else:
            return clase        
    
    def traducir_alias(self, query):

        # {------------[----------]_---}
        # {Atributos[Clase]}
        # {Clases[Usuario]_1
        prefijo = ''
        m = re.search(r'\{\w[^\t\r\n\f\v\{]*\[\w[^\t\r\n\f\v\}]*\]\}(\B|_[0-9]+)', query, re.UNICODE)
        while m != None:
            
            m_clase = re.search(r'\{\w[^\t\r\n\f\v\{]*\[', m.group(0))
            clase = m_clase.group(0)[1:-1].decode('utf-8').upper()
            
            m_atributo = re.search(r'\[\w[^\t\r\n\f\v\}]*\]', m.group(0))
            atributo = m_atributo.group(0)[1:-1].decode('utf-8').upper()
            
            # buscar "cod_atributo"
            cod_atributo = self.conector.conexion.\
                execute(self.tbl_atrib.\
                        join(self.tbl_clases,
                             and_(self.tbl_clases.c.cod_objeto == self.tbl_atrib.c[atributos_clase],
                                  func.upper(self.tbl_clases.c[clases_nombre]) == clase,
                                  func.upper(self.tbl_atrib.c[atributos_nombre]) == atributo)).\
                        select(use_labels=True)).\
                        fetchone()
                        
            if cod_atributo != None:
                
                cod_atributo = cod_atributo[self.tbl_atrib.c.cod_objeto]
            
                m_numero = re.search(r'\}(\B|_[0-9]+)', m.group(0))
                 
                query = \
                    query[:m.start()] + \
                    ('REL_%d%s' % (cod_atributo, (m_numero.group(0)[1:] if m_numero != None else ''))) + \
                    query[m.end():]
                    
            else:
                prefijo = prefijo + query[:m.end()]
                query = query[m.end():]
                
            query = prefijo + query
            m = re.search(r'\{\w[^\t\r\n\f\v\{]*\[\w[^\t\r\n\f\v\}]*\]\}(\B|_[0-9]+)', query)    
            
        return query
    
    def traducir(self, query):
        
        query = self.extraer_alias(query)
        query = self.traducir_columnas_sin_clase(query)
        query = self.traducir_columnas(query)
        query = self.traducir_colecciones(query)
        query = self.traducir_generadores(query)
        query = self.traducir_clases(query)
        query = self.traducir_alias(query)        
        
        return query
    
if __name__ == '__main__':
    
    from libpy.const_datos_neptuno import IMPLTYPE_FIREBIRD
    
    conector = Conexion(config=dict(host='localhost',
                                    db='ICB',
                                    user='SYSDBA',
                                    password='masterkey'),
                        impl_type=IMPLTYPE_FIREBIRD)
    
    query = \
        '--#  aeg     =    alumnos EN gRuPOS\n' + \
        ' SELECT \n' + \
        '   ORIGEN.COD_OBJETO, \n' + \
        '   {Clases.Nombre}, \n' + \
        '   .{Clases.Nombre}, \n' + \
        '   {aeg.Fecha de INICIO}, \n' + \
        '   {Atributos[Clase]_1.Nombre}, \n' + \
        '   {Atributos.COd_obJeto}, \n' + \
        '   {Atributos.Nombre} \n' + \
        '   {Atributos.Fecha de Creación} \n' + \
        '   {Atributos.Tipo de valor} \n' + \
        '   {Relación Objetos-Documentos.cod_objeto} \n' + \
        '   {Relación Objetos-Documentos.Usuario} \n' + \
        '   {Relación Objetos-Documentos.Usuario} \n' + \
        '   .{Relación Objetos-Documentos.Usuario} \n' + \
        '   {Relación Objetos-Documentos.Código de objeto} \n' + \
        '   {Relación Objetos-Documentos[Usuario].Fecha de creación} \n' + \
        ' FROM {Atributos} ORIGEN \n' + \
        ' +{Atributos} \n' + \
        ' *{Atributos} \n' + \
        ' FROM {Relación Objetos-Documentos} \n' + \
        ' INNER JOIN {Usuarios} {Atributos[Usuario]} ON {Atributos[Usuario].COD_OBJETO} = {Atributos.Usuario} \n\n' + \
        ' Insert into {Atributos} (COD_OBJETO, .{Atributos.Fecha de creación}, .{Atributos.Nombre}, .{Atributos.Usuario})\n' + \
        ' Values(Next value for +{Atributos}, \'Nuevo atrbuto\', 1)\n'
        
    copia = query    
    
    parser = SQLParser(conector)
    query = parser.traducir(query)
    
    print '\n', copia
    print '\n', query