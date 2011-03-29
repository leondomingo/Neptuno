# -*- coding: utf-8 -*-

from mod_python import apache
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.util import get_param, EFaltaParametro
from libpy.log import NeptunoLogger
from libpy.const_datos_neptuno import CONF_DB, CONF_HOST
logger = NeptunoLogger.get_logger('sw.consultas')
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
import simplejson
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
mod_lanzarconsulta = load_module(IMPLEMENTATION_TYPE, 'lanzarconsulta', 'lanzar_consulta')
lanzar_consulta = mod_lanzarconsulta.lanzar_consulta

def lanzarconsulta(req):    
    """
    Lanza un informe de Olympo y devuelve el resultado.
    
    IN
      id_usuario     <int>
      id_sesion      <str>
      cod_consulta   <int>
      nombreinforme  <str>
      parametros     
        Una lista de la forma: 
        [{"nombre": <str>, "valor": <str>}, ...] (opcional)
      time_out       <int> (en segundos) (opcional)
      
    OUT
      (contenido del PDF de la consulta)
    """
    
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion()    
        user = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)

        cod_consulta = get_param(req.form, 'cod_consulta', int)
        nombreinforme = get_param(req.form, 'nombreinforme', str)
    #    tipo_fichero = get_param(req.form, 'tipo_fichero', str, opcional=True,
    #                             por_defecto='pdf')

        parametros = get_param(req.form, 'parametros', simplejson.loads, 
                               opcional=True)
        
        time_out = get_param(req.form, 'time_out', int, opcional=True)
        
        req.content_type = 'application/pdf'
        req.headers_out['Content-Disposition'] = \
            'Content-Disposition: attachment; filename="%s.pdf"' % nombreinforme    

        return lanzar_consulta(cod_usuario=user.id_usuarios_usuarioperfil,
                               servidor=conector.config[CONF_HOST],
                               base=conector.config[CONF_DB],
                               cod_consulta=cod_consulta,
                               nombreinforme=nombreinforme,
                               parametros=parametros,
                               tipo_fichero='pdf',
                               time_out=time_out)
        
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND
    
    