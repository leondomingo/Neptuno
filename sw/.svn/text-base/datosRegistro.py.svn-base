# -*- coding: utf-8 -*-

from mod_python import apache
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.util import get_param, get_params, EFaltaParametro, strtobool
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.datosRegistro')
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
import simplejson
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
dr = load_module(IMPLEMENTATION_TYPE, 'datosRegistro', 'record_data')
record_data = dr.record_data
raw_data = dr.raw_data

def index(req):
    """
    IN
      id_usuario  <int>
      id_sesion   <str>
      tabla       <str>
      id          <int>
      sin_orden   <bool>
      # campos predefinidos
      
    OUT
      Un JSON de la forma:
        [{campo1}, {campo2}, ...]
            
      Cada "campoX", a su vez, tiene la forma:
      campo = {
               "nombre":            <str>,
               "tipo":              <str>,
               "valor":             <str>,
               "etiqueta":          <str>,
               "requerido":         <bool>
               "solo_lectura":      <bool>,
               "tabla_relacionada": <str>,
               "utilizar_selector": <bool>,
               "valores":           [[{campo}, ...], ...]
              }
      
      sin_orden = True
      
      {
       <nombre>: {
         "tipo":              <str>,
         "valor":             <str>,
         "etiqueta":          <str>,
         "requerido":         <bool>
         "solo_lectura":      <bool>,
         "tabla_relacionada": <str>,
         "utilizar_selector": <bool>,
         "valores":           [[{campo}, ...], ...]
       },
       ...
      }
    """
    
    try:
        # comprobar usuario/sesión
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str) 

        conector = Conexion()
        Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
        
        # recoger parámetros
        tabla = get_param(req.form, 'tabla', str)
        id_registro = get_param(req.form, 'id', int)
        sin_orden = get_param(req.form, 'sin_orden', strtobool, opcional=True,
                              por_defecto=False)
        
        # campos "predefinidos"
        campos_pre = get_params(req.form, ['id_usuario', 'id_sesion', 
                                           'tabla', 'id', 'sin_orden'])
                
        registro = record_data(id_usuario, tabla, id_registro, sin_orden, 
                               conector, **campos_pre)
        
        return simplejson.dumps(registro, encoding='utf8')
        
    except (NoExisteUsuario, SesionIncorrecta, EFaltaParametro), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    
def raw(req):
    """
    IN
      id_usuario  <int>
      id_sesion   <str>
      tabla       <str>
      id          <int>
      campos      [<str>, ...] (opcional)
      
    OUT
      Un JSON de la forma:
        {<nombre1>: <valor1>, <nombre2>:<valor2>, ...}
    """
    
    try:
        # comprobar usuario/sesión
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str) 

        conector = Conexion()
        Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)

        # recoger parámetros        
        tabla = get_param(req.form, 'tabla', str)
        id = get_param(req.form, 'id', int)
        
        campos = get_param(req.form, 'campos', simplejson.loads,
                           opcional=True)
        
        registro = raw_data(tabla, id, campos, conn=conector)
        
        return simplejson.dumps(registro, encoding='utf8')
        
    except (NoExisteUsuario, SesionIncorrecta, EFaltaParametro), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN