#-*- coding: utf-8 -*-

from mod_python import apache
from libpy.conexion import Conexion
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.util import get_param, strtobool, EFaltaParametro
from libpy.const_datos_neptuno import PRIVL_NINGUNO
from nucleo.config import IMPLEMENTATION_TYPE
mod_buscar = load_module(IMPLEMENTATION_TYPE, 'buscar', 'search')
search = mod_buscar.search
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
from libpy.excepciones.eneptuno import NoTienePrivilegios, SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
import simplejson
from datetime import datetime
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.buscar')

def index(req):
    """
    Realiza una búsqueda en la base según los criterios indicados en los 
    parámetros.
    
    IN
      id_usuario        <int>
      id_sesion         <str>
      busqueda          <str>
      tabla             <str>
      id_registro       <int>  (opcional),
      campos            <list> (opcional), # [[c1,v1], [c2,v2], ...]
      limite_resultados <int>  (opcional) 
      pos               <int>
      generar_csv       <bool> (opcional)
      # para desplegables
      etiqueta          <str>  (opcional)
      valor             <str>  (opcional)
    
    OUT
      # generar_csv = False
      {
       "numero_resultados": <int>,
       "limite_resultados": <int>,
       "columnas":          [<str>, <str>, ...],
       "datos":             [
                             [d11, d12, ...],
                             [d21, d22, ...],
                             ...                     
                            ]
      }
      
      # generar_csv = True
      (CSV)
    """

    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion()   
        usuario = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)

        busqueda = get_param(req.form, 'busqueda', str, opcional=True)    
        tabla = get_param(req.form, 'tabla', str)
        
        # id_registro
        id_registro = get_param(req.form, 'id', int, opcional=True)
                    
        # campos
        campos = get_param(req.form, 'campos', simplejson.loads, 
                           opcional=True)
        
        # orderbyid
        orderbyid = get_param(req.form, 'orderbyid', strtobool, 
                              opcional=True, por_defecto=False)
            
        # generar_csv
        generar_csv = get_param(req.form, 'generar_csv', strtobool, 
                                opcional=True)
        
        offset = get_param(req.form, 'pos', int, por_defecto=0, opcional=True)
               
        limit = get_param(req.form, 'limite_resultados', int,
                          por_defecto=100, opcional=True)    
    
        # para desplegables
        etiqueta = get_param(req.form, 'etiqueta', str, opcional=True)
        valor = get_param(req.form, 'valor', str, opcional=True)
        
        
        if usuario.getPrivilegioTabla(tabla) == PRIVL_NINGUNO:
            raise NoTienePrivilegios(usuario.nombre_usuario, tabla)
        
        if not generar_csv:       
            resultado = search(tabla, busqueda=busqueda, 
                               campos=campos, id_registro=id_registro,
                               limite_resultados=limit,
                               pos=offset,
                               orderbyid=orderbyid, 
                               col_etiqueta=etiqueta,
                               col_id=valor,
                               conector=conector)
            
            return resultado.to_json()
            
        else:
            # devolver el resultado en forma de CSV
            resultado = search(tabla, busqueda=busqueda, 
                               campos=campos, id_registro=id_registro,
                               limite_resultados=None,
                               pos=0,
                               conector=conector)
            
            req.content_type = 'text/csv'
            req.headers_out['Content-Disposition'] = \
                'Content-Disposition: attachment; filename="%s_%s.csv"' % \
                    (tabla, datetime.now().strftime('%Y%m%d%H%M%S'))
                    
            return resultado.to_csv()
                    
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta, 
            NoTienePrivilegios), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    