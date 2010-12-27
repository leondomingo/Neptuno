# -*- coding: utf-8 -*-

import cherrypy
import sys
sys.stdout = sys.stderr
from wsgi.neptuno import Neptuno
from wsgi.consultas import ConsultasOlympo

class NeptunoFB(Neptuno):
    
    consultas_py = ConsultasOlympo()
    
application = cherrypy.Application(NeptunoFB(), script_name=None, config=None)