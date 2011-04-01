# -*- coding: utf-8 -*-

from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql.expression import select
from libpy.conexion import Conexion

class ENoExisteRegistro(Exception):
    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return 'No existe el regsitro %d' % self.id

def merge(nombre_tabla, id_destino, otros_ids):
    """
    Fusiona uno o más registros (otros_ids) en otro (id_destino), siendo todos ellos
    de la tabla 'nombre_tabla'.
    
    IN
      id_usuario: Identificador del usuario que se conecta
      nombre_tabla: Nombre de la tabla a la que pertenecen los registros
      id_destino: Identificador del registro donde se guardará la información
      otros_ids: Lista de ids desde donde se obtendrá la información
    
    OUT
      un json de la forma:
      {
       'id_destino': 123,
       'id_origen': 123,
       'num_campos': 123
      }
    
    EXC
      ENoExisteRegistro: Cuando no existe alguno de los registros (origen o destino)
    """
    
    conector = Conexion()

    meta = MetaData(bind=conector.engine, reflect=True)
    tabla = Table(nombre_tabla, meta, autoload=True)                
                        
    # comprobar que existe el registro "destino"
    alumno = conector.conexion.execute(select([tabla], tabla.c.id == id_destino)).fetchone()
    if alumno is None:
        raise ENoExisteRegistro(id_destino)
    
    # comprobar que existen los "otros" registros
    for id_otro in otros_ids:
        
        otro = conector.conexion.execute(select([tabla], tabla.c.id == id_otro)).fetchone()
        if otro is None:
            raise ENoExisteRegistro(id_otro)
            
    # fusionar
    resultado = {}
    resultado['id_destino'] = id_destino
    resultado['num_campos'] = 0         
    for id_otro in otros_ids:
        resultado['id_origen'] = id_otro
        
        # obtener datos de los dos alumnos
        alumno = conector.conexion.execute(select([tabla], tabla.c.id == id_destino)).fetchone()
        otro = conector.conexion.execute(select([tabla], tabla.c.id == id_otro)).fetchone()
        
        # claves foráneas que hacen referencia a esta tabla
        for t in meta.sorted_tables:
            for fk in t.foreign_keys:
                if fk.references(tabla):
                    # actualizar los registros que apuntan a "origen" -> "destino"
                    qry_update = t.update(fk.parent == id_otro, values={fk.parent: id_destino})
                    conector.conexion.execute(qry_update)                        
        
        conector.conexion.commit()
        
        # cambiar datos de la tabla
        datos = {}
        for k in alumno.keys():
            if k != 'id' and k != 'busqueda':
                if alumno[k] is None and otro[k] != None:
                    datos[k] = otro[k]
                    resultado['num_campos'] += 1
                    
            if datos != {}:
                # actualizar "destino"
                qry_update = tabla.update(tabla.c.id == id_destino, values=datos)
                conector.conexion.execute(qry_update)

        # borrar "otro"
        qry_delete = tabla.delete(tabla.c.id == id_otro)
        conector.conexion.execute(qry_delete)
        conector.conexion.commit()                    
    
    return resultado
