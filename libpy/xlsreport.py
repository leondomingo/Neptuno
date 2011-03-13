# -*- coding: utf-8 -*-

import re
from lxml import etree
from xlwt import Workbook, Formula
from xlwt.Style import easyxf
from genshi.template.loader import TemplateLoader
from libpy.util import strtodate, strtotime
from nucleo.config import VARIABLES

def xlsreport(template, params, filename):
    """
    IN
      template  <str>
      params   <dict>
      filename  <str>
      
    OUT
      <str>
    """

    class Util(object):
        
        def __init__(self):
            self.n = 0
            self.marks = {}
            
        def init_count(self):
            self.n = 0
            
        def current_line(self):
            return self.n
        
        def line_feed(self):
            self.n += 1
            return self.n
        
        def add_bookmark(self, name):
            self.marks[name] = self.n
            return self.n
            
        def bookmark(self, name):
            return self.marks[name]
            
    tl = TemplateLoader([VARIABLES['ruta_templates']])
    tmpl = tl.load(template)
    informe = tmpl.generate(**params)
    informe_xml = informe.render('xml')
    
    root = etree.fromstring(informe_xml)
    
    wb = Workbook()
    
    n_sheet = 0
    for sheet in root.iter('sheet'):
        
        n_sheet += 1
        
        # title
        title = 'Sheet-%d' % n_sheet
        if sheet.attrib.has_key('title') and sheet.attrib['title']:
            title = sheet.attrib['title']
            
        ws = wb.add_sheet(title, True)
        
        util = Util()
        for item in sheet:
            # cell
            if item.tag == 'cell':
                col = int(item.attrib['col'])
                
                style = []
                num_format = None
                
                value = item.find('value')
                dato = value.text
                # type: aplicar una conversión (str, int, float, ...)
                if item.attrib.has_key('type') and item.attrib['type']:
                    tipo = item.attrib['type'].split(';')
                    
                    # date
                    if tipo[0] == 'date':
                        dato = strtodate(dato)

                    # time
                    elif tipo[0] == 'time':
                        dato = strtotime(dato, fmt='%H:%M:%S')
                    
                    # formula
                    elif tipo[0] == 'formula':
                        def parsear_formula(texto):
                            def evaluar(m):
                                # esto sólo está aquí para que se pueda
                                # referenciar "util" en la expresión de la fórmula
                                util.current_line()
                                expr = m.group(1).replace('{', '').replace('}', '')
                                return str(eval(expr))
                            
                            # {{<fórmula>}}
                            return re.sub(r'({{[^\{\}]+}})', evaluar, texto)
                            
                        dato = Formula(parsear_formula(dato))
                    
                    # resto de tipos
                    else:
                        f = lambda t,v: t(v)
                        dato = f(eval(tipo[0]), dato)
                    
                    # date;dd/mm/yyyy
                    # date;dd/mmm/yyyy
                    # date;NN D MMMM YYYY
                    # time;hh:mm
                    # float;#,##0.00
                    # float;+#,##0.00
                    # float;#,##0.00;[RED]-#,##0.00
                    if len(tipo) > 1:
                        num_format = ';'.join(tipo[1:])

                # style: aplicar un estilo
                estilo = item.find('style')
                if estilo != None:
                    # font
                    fuente = estilo.find('font')
                    if fuente != None:
                        
                        font = []
                        
                        # name
                        if fuente.attrib.get('name', None):
                            font.append('name %s' % fuente.attrib['name'])
                            
                        # size (height)
                        if fuente.attrib.get('size', None):
                            font.append('height %d' % (int(fuente.attrib['size'])*25))
                            
                        # color
                        if fuente.attrib.get('color', None):
                            color = fuente.attrib['color']
                            font.append('color_index %s' % color)
                            
                        # bold
                        if fuente.attrib.get('bold', None):
                            font.append('bold on')
                        
                        # italic
                        if fuente.attrib.get('italic', None):
                            font.append('italic on')
                        
                        # añadir "font"
                        if font:
                            #print font
                            style.append('font: %s' % (','.join(font)))
                            
                    # align
                    if estilo.find('align') != None:
                        
                        al = estilo.find('align')
                        align = []
                        
                        # halign (horiz align)
                        if al.attrib.get('hor', None):
                            align.append('horiz %s' % al.attrib['hor'])
                            
                        # valign (vert align)
                        if al.attrib.get('ver', None):
                            align.append('vert %s' % al.attrib['ver'])
                            
                        if align:
                            style.append('align: %s' % (','.join(align)))
                            
                    pattern = []
                    
                    # bgcolor
                    if estilo.attrib.get('bgcolor', None):
                        pattern.append('solid')
                        pattern.append('fore-color %s' % estilo.attrib['bgcolor'])
                        
                    if pattern:
                        style.append('pattern: %s' % (','.join(pattern)))
                        
                #print style
                ws.write(util.current_line(), col, dato, 
                         easyxf(';'.join(style), num_format_str=num_format))
            
            elif item.tag == 'line_feed':
                util.line_feed()
                
            elif item.tag == 'bookmark':
                util.add_bookmark(item.attrib['name'])
            
    wb.save(filename)
    
    return informe_xml