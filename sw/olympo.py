# -*- coding: utf-8 -*-

import simplejson as sj
from libpy.conexion import Conexion
from libpy.log import NeptunoLogger
from libpy.util import get_param
from libpy.const_datos_neptuno import STATUS, MESSAGE, EXPIRATION
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from nucleo.messages import Messages
from nucleo.unidadescompartidas import UsuariosWeb 
from libpy.firebird.gestorconsultas import GestorConsultas

def consultasusuario(req):
    """
    Devuelve una lista de consultas del usuario ordenadas alfabéticamente.
    
    IN
      id_usuario  <int>
      id_sesion   <str>
      
    OUT
      {
       "status":     <bool>,
       "message":    <str>,
       "expiration": <bool>,
       "consultas":  [{"id": <int>, "nombre": <str>}, ...]
      }
    """
    
    logger = NeptunoLogger.get_logger('olympo/consultas')
    mess = Messages()
    try:
        conector = Conexion()
        
        # comprobar sesión
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        UsuariosWeb.comprobar_sesion(conector, id_usuario, id_sesion)
        
        gc = GestorConsultas(conector)
        
        return sj.dumps({STATUS: True, 
                         'consultas': gc.consultas_usuario(id_usuario)})
    
    except (NoExisteUsuario, SesionIncorrecta), e:
        logger.erro(e)
        return sj.dumps({STATUS: False, EXPIRATION: True})
        
    except Exception, e:
        logger.error(e)
        return sj.dumps({STATUS: False, MESSAGE: mess.getErrorGeneral()})
    
def parametrosconsulta(req):
    """
    Devuelve una lista ordenada de parámetros de la consulta.
    
    IN
      id_usuario   <int>
      id_sesion    <str>
      id_consulta  <int>
      
    OUT
      {
       "status":     <bool>,
       "message":    <str>,
       "expiration": <bool>,
       "parametros": [{"nombre": <str>, "por_defecto": <str>}, ...]
      }
    """
    
    logger = NeptunoLogger.get_logger('olympo/parametrosconsulta')
    mess = Messages()
    try:
        conector = Conexion()
        
        # comprobar sesión
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        UsuariosWeb.comprobar_sesion(conector, id_usuario, id_sesion)
        
        # recoger parámetros
        id_consulta = get_param(req.form, 'id_consulta', int)
        
        gc = GestorConsultas(conector)
        
        return sj.dumps({STATUS: True, 
                         'parametros': gc.parametros(id_consulta)})
    
    except (NoExisteUsuario, SesionIncorrecta), e:
        logger.erro(e)
        return sj.dumps({STATUS: False, EXPIRATION: True})
        
    except Exception, e:
        logger.error(e)
        return sj.dumps({STATUS: False, MESSAGE: mess.getErrorGeneral()})