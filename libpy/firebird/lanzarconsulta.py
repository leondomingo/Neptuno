# -*- coding: utf-8 -*-

import re
import sys
from lxml import etree
from base64 import encodestring
import tempfile
import os
import subprocess as sp
import threading
import signal
try:
    import win32api
except ImportError:
    pass 
from libpy.log import NeptunoLogger
from libpy.firebird.const_datos_olympo import TDF_PDF
from nucleo.config import VARIABLES

from libpy.const_datos_neptuno import VAR_LANZADOR, VAR_TIMEOUT_CONSULTAS

class KillLanzador(object):
    def __init__(self, process, time_out):
        self.process = process
        self.t = threading.Timer(time_out, self.kill)
        
    def kill(self):
        if sys.platform == 'win32':
            win32api.TerminateProcess(int(self.process._handle), -1)
            
        else:
            # linux
            os.kill(self.process.pid, signal.SIGKILL)
        
    def start(self):        
        self.t.start()
        
def lanzar_consulta(cod_usuario, servidor, base, cod_consulta, nombreinforme, \
                    parametros=None, tipo_fichero=None, time_out=None,
                    log=None):
    """
    Lanza una consulta de Olympo mediante el lanzador (LanzarConsultaFR.exe)
    que debe estar indicado entre las variables (const__bbdd.py/variables) como
    'lanzador'.
    
    IN
      cod_usuario    <int> (<usuarios web>)
      servidor       <str>
      base           <str>
      cod_consulta   <int> (<ConsultasOlympo>)
      nombreinforme  <unicode>
      parametros ([{'nombre': <str>, 'valor': <str>}, ...])
      tipo_fichero   <str> = ('pdf'|'excel') (opcional, None)
      time_out       <int> (opcional)
          Time-out concreto para esta consulta. Tiene preferencia sobre el time-out
          definido en "VARIABLES" (config.py)
    
    OUT
      (contenido del informe resultante en PDF)
      
    EXC
      Exception
        No existe la variable "lanzador"
    """
    
    logger = NeptunoLogger.get_logger('lanzar_consulta')

    root = etree.Element('root')
    
    # servidor
    etree.SubElement(root, 'servidor').text = servidor 
    
    # base
    etree.SubElement(root, 'base').text = base
    
    # cod_usuario
    etree.SubElement(root, 'cod_usuario').text = str(cod_usuario)    
    
    # cod_consulta
    n_consulta = etree.SubElement(root, 'cod_consulta')
    n_consulta.text = str(cod_consulta)
    
    # nombreinforme
    n_nombreinforme = etree.SubElement(root, 'nombreinforme')
    n_nombreinforme.text = nombreinforme
    
    # parámetros
    if parametros != None:
        for parametro in parametros:
            n_parametro = etree.SubElement(root, 'parametro')
            etree.SubElement(n_parametro, 'nombre').text = parametro['nombre']
            etree.SubElement(n_parametro, 'valor').text = encodestring(str(parametro['valor']))
            
#    return etree.tostring(root, pretty_print=True)
            
    # TODO: controlar "tipo_fichero"
    if tipo_fichero is None or tipo_fichero == TDF_PDF:
        pass
        
    # rutaFicheroPdf
    fd_pdf, nombre_pdf = tempfile.mkstemp(suffix='.pdf', prefix='cons_')
    os.close(fd_pdf)
    try:    
        etree.SubElement(root, 'rutaficheropdf').text = nombre_pdf
        
        # fichero XML
        fd_xml, nombre_xml = tempfile.mkstemp(suffix='.xml', prefix='lanzarconsulta_')
        os.close(fd_xml)
        try:
            fichero_xml = file(nombre_xml, 'wb')
            try:
                fichero_xml.write(etree.tostring(root, xml_declaration=True, 
                                                 encoding='ISO-8859-1', \
                                                 pretty_print=True))
            finally:
                fichero_xml.close()
                
            # llamar a la aplicación que genera el PDF
            nombre_aplicacion = VARIABLES.get(VAR_LANZADOR)
            
            logger.debug('Lanzando informe (%s)' % nombre_aplicacion)
            
            if nombre_aplicacion == '':
                e = Exception('No está definida la variable "%s"' % VAR_LANZADOR)
                logger.error(e)
                raise e
            
            else:
                m_wine = re.search(r'^(.+wine)\s+(.+)', nombre_aplicacion)
                if m_wine:
                    cmd = [m_wine.group(1), m_wine.group(2), nombre_xml, 
                           (log or '')]
                    
                    # incluir variables de entorno necesarias para ejecutar Wine
                    os.environ['DISPLAY'] = ':0'
                    os.environ['WINEDEBUG'] = '-all'
                
                else:
                    cmd = [nombre_aplicacion, nombre_xml, (log or '')]
                    
            logger.debug('Comando para lanzar consulta: "%s"' % cmd)

            # ejecutar proceso
            p = sp.Popen(cmd)
            
            # "time out" al lanzar una consulta
            if time_out is None:
                time_out = VARIABLES.get(VAR_TIMEOUT_CONSULTAS)
            
                if time_out == '':
                    time_out = 30
                
            killer = KillLanzador(p, time_out)
            try:
                killer.start()
                
                # ejecutar lanzador
                logger.debug('Ejecutando lanzador de consulta (%d)' % os.getuid())
                out_data, err_data = p.communicate(0)
                
                logger.debug(out_data)
                logger.debug(err_data)
                
                # leer el resultado que se ha escrito en "nombre_pdf"
                fichero_pdf = file(nombre_pdf, 'rb')
                try:
                    return fichero_pdf.read()                 
                finally:
                    fichero_pdf.close()
                
            finally:
                killer.t.cancel()
                
        finally:
            if os.access(nombre_xml, os.F_OK or os.R_OK):
                os.remove(nombre_xml)
                
    finally:
        if os.access(nombre_pdf, os.F_OK or os.R_OK):
            os.remove(nombre_pdf)