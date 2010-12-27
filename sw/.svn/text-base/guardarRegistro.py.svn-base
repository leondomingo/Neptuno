#-*- coding: utf-8 -*-

from mod_python import apache
import simplejson
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.util import get_param, EFaltaParametro
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.guardarRegistro')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
gr = load_module(IMPLEMENTATION_TYPE, 'guardarRegistro', 'save')
save = gr.save

def index(req):
    """
    Guardar datos de una tabla.
    
    IN
      id_usuario <int>
      id_sesion  <str>
      tabla      <str>
      datos      {<campo1>: <valor1>, <campo2>: <valor2>, ...}
      
    OUT
      <int>
    """
    
    try:
        # comprobar usuario/sesión
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion()
        Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)

        # recoger parámetros
        tabla = get_param(req.form, 'tabla', str)    
        datos = get_param(req.form, 'datos', simplejson.loads)

        id_registro = save(tabla, id_usuario, datos, conector=conector)
        req.write(str(id_registro))
        
    except (NoExisteUsuario, SesionIncorrecta, EFaltaParametro), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN

