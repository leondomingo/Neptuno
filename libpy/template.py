# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
from libpy.log import NeptunoLogger
from nucleo.config import VARIABLES

def get_template(ruta):
    """
    Devuelve el objeto template (<jinja2.Template>) que corresponde al template
    indicado por la ruta. La ruta completa del template se calcula como:
        ruta_completa = os.path.join(VARIABLES['ruta_templates'], ruta)
        
    Así que tenemos que indicar la ruta con base a la ruta de templates definida
    en VARIABLES.
    
    IN
      ruta  <str>
      
    OUT
      <jinja2.Template>
    """
    
    logger = NeptunoLogger.get_logger('template/get_template')
    try:
        env = Environment(loader=FileSystemLoader(VARIABLES['ruta_templates']))
        return env.get_template(ruta)
        
    except Exception, e:
        logger.error(e)

    