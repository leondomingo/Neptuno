# -*- coding: utf-8 -*-

import cherrypy
import sys
sys.stdout = sys.stderr
from wsgi.datosregistro import DatosRegistro
from wsgi.user import User
from wsgi.acciones import AccionesNoPermitidas
from wsgi.clases import ClasesNoPermitidas
from wsgi.buscar import Buscar
from wsgi.borrar import Borrar
from wsgi.fusionarSW import Fusionar
from wsgi.variablesSW import Variables
from wsgi.enviaremail import EnviarEmail
from wsgi.guardarRegistro import GuardarRegistro

class AppVacia(object):
    
    def __init__(self, nombre):
        self.nombre = nombre        
    
    @cherrypy.expose
    def index(self):
        return 'No existe aplicación definida para "%s"' % self.nombre

class Neptuno(object):
    
    borrar_py = Borrar()
    buscar_py = Buscar()
    datosRegistro_py = DatosRegistro()
    users_py = User()
    acciones_no_permitidas_py = AccionesNoPermitidas()
    clases_no_permitidas_py = ClasesNoPermitidas()
    enviaremail_py = EnviarEmail()
    fusionarSW_py = Fusionar()
    guardarRegistro_py = GuardarRegistro()
    variablesSW_py = Variables()    
    
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return str(cherrypy.request.headers)
    
application = cherrypy.Application(Neptuno(), script_name=None, config=None)
