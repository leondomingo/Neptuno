# -*- coding: utf-8 -*-

import simplejson
import cherrypy
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.util import strtobool, EFaltaParametro, get_paramw
from libpy.const_datos_neptuno import PRIVL_NINGUNO
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from wsgi.base import NeptunoBase
mod_buscar = load_module(IMPLEMENTATION_TYPE, 'buscar', 'search')
search = mod_buscar.search
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
from libpy.excepciones.eneptuno import NoTienePrivilegios, SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from datetime import datetime
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('wsgi.buscar')

class Buscar(NeptunoBase):
    
    #_cp_config = {'tools.gzip.on': True}

    @cherrypy.expose
    @cherrypy.tools.gzip()
    def default(self, **params):
        """
        Realiza una búsqueda en la base según los criterios indicados en los 
        parámetros.
        
        IN
          id_usuario         <int>
          id_sesion          <str>
          busqueda           <str>
          tabla              <str>
          id                 <int>  (opcional),
          campos             <list> (opcional), # [[c1,v1], [c2,v2], ...]
          limite_resultados  <int>  (opcional) 
          pos                <int>
          generar_csv        <bool> (opcional)
          # para desplegables
          etiqueta           <str>  (opcional)
          valor              <str>  (opcional)
        
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
            conector = Conexion()
            usuario = self.check_session(conector, Usuarios, **params)
            
            busqueda = get_paramw(params, 'busqueda', str, opcional=True)
            tabla = get_paramw(params, 'tabla', str)
            
            logger.debug('Buscando "%s" en la tabla "%s"...' % (busqueda, tabla))
            
            # id_registro
            id_registro = get_paramw(params, 'id', int, opcional=True)
                        
            # campos
            campos = get_paramw(params, 'campos', simplejson.loads, opcional=True)
            
            # orderbyid
                
            # generar_csv
            generar_csv = get_paramw(params, 'generar_csv', strtobool, opcional=True,
                                     por_defecto=False)
            
            offset = get_paramw(params, 'pos', int, opcional=True, por_defecto=0)
            limit = get_paramw(params, 'limite_resultados', int, opcional=True,
                               por_defecto=100)
    
            # para desplegables
            etiqueta = get_paramw(params, 'etiqueta', str, opcional=True)
            valor = get_paramw(params, 'valor', str, opcional=True)
            
            if usuario.getPrivilegioTabla(tabla) == PRIVL_NINGUNO:
                raise NoTienePrivilegios(usuario.nombre_usuario, tabla)
            
            if not generar_csv:       
                resultado = search(tabla, busqueda=busqueda, 
                                   campos=campos, id_registro=id_registro,
                                   limite_resultados=limit,
                                   pos=offset,
                                   orderbyid=False, 
                                   col_etiqueta=etiqueta,
                                   col_id=valor,
                                   conector=conector)
                
                cherrypy.response.headers['Content-Type'] = 'text/plain'
                return resultado.to_json()

            else:
                # devolver el resultado en forma de CSV
                resultado = search(tabla, busqueda=busqueda, 
                                   campos=campos, id_registro=id_registro,
                                   limite_resultados=None,
                                   pos=0,
                                   conector=conector)
                
                cherrypy.response.headers['Content-Type'] = 'text/csv'
                cherrypy.response.headers['Content-Disposition'] = \
                    'Content-Disposition: attachment; filename="%s_%s.csv"' % \
                        (tabla, datetime.now().strftime('%Y%m%d%H%M%S'))

                return resultado.to_csv()

        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta, 
                NoTienePrivilegios), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)