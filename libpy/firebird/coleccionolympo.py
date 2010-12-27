# -*- coding: utf-8 -*-

from util import cod_atributo, nombre_coleccion
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.expression import and_

class ColeccionOlympo(object):
    
    def __init__(self, conector, cod_origen, clase_origen, atributo_origen, 
                 clase_enlazada, atributo_enlazado):
        
        self.conector = conector
        self.cod_origen = cod_origen
        self.clase_origen = clase_origen
        self.atributo_origen = cod_atributo(atributo_origen)
        self.clase_enlazada = clase_enlazada
        self.atributo_enlazado = cod_atributo(atributo_enlazado)
        
        meta = MetaData(bind=self.conector.engine)
        self.tbl_coleccion = Table(nombre_coleccion(clase_origen.cod_clase), meta, 
                                   autoload=True)
        
        self.tbl_coleccion_enl = Table(nombre_coleccion(clase_enlazada.cod_clase), 
                                       meta, autoload=True)   
    
    def add(self, id_destino, commit=False):
        """Añade 'id_destino' a la colección. 'id_destino' puede ser un entero o 
        una lista de enteros"""        
        
        # un único id
        if isinstance(id_destino, int):
            # actualizar la tabla de colección
            qry_ins = self.tbl_coleccion.\
                insert(values={self.tbl_coleccion.c.cod_objeto: self.cod_origen,
                               self.tbl_coleccion.c.cod_atributo: self.atributo_origen,
                               self.tbl_coleccion.c.cod_objetoincluido: id_destino})
                        
            self.conector.conexion.execute(qry_ins)
            
            # actualizar la tabla de colección "enlazada"
            qry_ins2 = \
                self.tbl_coleccion_enl.\
                insert(values={self.tbl_coleccion_enl.c.cod_objeto: id_destino,
                               self.tbl_coleccion_enl.c.cod_atributo: self.atributo_enlazado,
                               self.tbl_coleccion_enl.c.cod_objetoincluido: self.cod_origen})
                        
            self.conector.conexion.execute(qry_ins2)
            
        # una lista de ids
        elif isinstance(id_destino, list):
            
            for i in id_destino:
                self.add(i)
        
        if commit:
            self.conector.conexion.commit()
            
    def find(self, id_destino):
        """Devuelve el objeto de la clase enlazada con id 'id_destino' dentro de 
        la colección, o None en caso contrario"""
        
        return self.conector.conexion.query(self.clase_enlazada).\
                join((self.tbl_coleccion, \
                      and_(self.tbl_coleccion.c.cod_objetoincluido == id_destino,
                           self.tbl_coleccion.c.cod_objeto == self.cod_origen,
                           self.tbl_coleccion.c.cod_atributo == self.atributo_origen))).\
                first()

    
    def remove(self, id_destino, commit=False):
        """Saca de la colección el id 'id_destino'. 'id_destino' puede ser un 
        entero o una lista de enteros"""
        
        # un único id
        if isinstance(id_destino, int):
            qry_borrado = \
                self.tbl_coleccion.\
                delete(and_(self.tbl_coleccion.c.cod_objetoincluido == id_destino,
                            self.tbl_coleccion.c.cod_objeto == self.cod_origen,
                            self.tbl_coleccion.c.cod_atributo == self.atributo_origen))
            
            qry_borrado2 = \
                self.tbl_coleccion_enl.\
                delete(and_(self.tbl_coleccion_enl.c.cod_objetoincluido == self.cod_origen,
                            self.tbl_coleccion_enl.c.cod_objeto == id_destino,
                            self.tbl_coleccion_enl.c.cod_atributo == self.atributo_enlazado))            
            
            
        # una lista de ids
        elif isinstance(id_destino, list):
            qry_borrado = \
                self.tbl_coleccion.\
                delete(and_(self.tbl_coleccion.c.cod_objetoincluido.in_(id_destino),
                            self.tbl_coleccion.c.cod_objeto == self.cod_origen,
                            self.tbl_coleccion.c.cod_atributo == self.atributo_origen))
            
            qry_borrado2 = \
                self.tbl_coleccion_enl.\
                delete(and_(self.tbl_coleccion_enl.c.cod_objetoincluido == self.cod_origen,
                            self.tbl_coleccion_enl.c.cod_objeto.in_(id_destino),
                            self.tbl_coleccion_enl.c.cod_atributo == self.atributo_enlazado))            
            
        else:
            raise TypeError('id_destino debe ser <int> o <list>')
                        
        self.conector.conexion.execute(qry_borrado)
        self.conector.conexion.execute(qry_borrado2)
        
        if commit:
            self.conector.conexion.commit()
            
    def removeall(self, commit=False):
        """Vacía la colección"""
        
        # borrar en la tabla de colección
        qry_borrado = \
            self.tbl_coleccion.\
            delete(and_(self.tbl_coleccion.c.cod_objeto == self.cod_origen,
                        self.tbl_coleccion.c.cod_atributo == self.atributo_origen))  
        
        self.conector.conexion.execute(qry_borrado)
        
        # borrar en la tabla de colección "enlazada"
        qry_borrado2 = \
            self.tbl_coleccion_enl.\
            delete(and_(self.tbl_coleccion_enl.c.cod_objetoincluido == self.cod_origen,
                        self.tbl_coleccion_enl.c.cod_atributo == self.atributo_enlazado))  
        
        self.conector.conexion.execute(qry_borrado2)       
        
        if commit:
            self.conector.conexion.commit()
    
    def all(self):
        """Devuelve la lista de objetos de la clase "enlazada" que están en la colección"""
         
        return self.conector.conexion.query(self.clase_enlazada).\
                    join((self.tbl_coleccion, 
                          and_(self.tbl_coleccion.c.cod_objetoincluido == self.clase_enlazada.id,
                               self.tbl_coleccion.c.cod_objeto == self.cod_origen,
                               self.tbl_coleccion.c.cod_atributo == self.atributo_origen))).\
                    order_by(self.clase_enlazada.id).\
                    all()
