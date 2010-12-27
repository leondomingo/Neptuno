# -*- coding: utf-8 -*-

from mod_python import apache
from libpy.enviaremail import enviar_email
import simplejson
from libpy.util import get_param
from libpy.conexion import Conexion
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.enviaremail')
from libpy.neptunofactory import get_claseusuarios
from nucleo.config import IMPLEMENTATION_TYPE
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

def index(req):
    """
    IN
      id_usuario     <int> 
      id_sesion      <str>
      remitente      <list> => [["<email>", "nombre"]]
      destinatarios  <list> => [["<email1>", "<nombre1>"], ["<email2>", "<nombre2>"], ...]
      asunto         <str>
      mensaje        <str>
      servidor       <str>
      login          <str>
      password       <str>
    """
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion()
        Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
    
        remitente = get_param(req.form, 'remitente', simplejson.loads)

        destinatarios = get_param(req.form, 'destinatarios', simplejson.loads)
        
        asunto = get_param(req.form, 'asunto', str)
        mensaje = get_param(req.form, 'mensaje', str)
        servidor = get_param(req.form, 'servidor', str)
        login = get_param(req.form, 'login', str)
        password = get_param(req.form, 'password', str)
        
        r = enviar_email(remitente, destinatarios, asunto, mensaje, 
                         servidor, login, password)
        
        return simplejson.dumps(r)
    
    except Exception, e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN