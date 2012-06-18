# -*- coding: utf-8 -*-

from lxml import etree
from neptuno.util import strtodate, strtotime
from xlwt import Workbook, Formula
from xlwt.Style import easyxf, XFStyle
import re
import xlrd

__all__ = ['XLSReport']

class XLSReport(object):
    
    class Util(object):
        
        def __init__(self):
            self.n = 0
            self.marks = {}
            
        def init_count(self):
            self.n = 0
            self.marks = {}
            
        def current_line(self):
            return self.n
        
        def line_feed(self, n=1):
            self.n += n
            return self.n
        
        def add_bookmark(self, name):
            self.marks[name] = self.n
            return self.n
            
        def bookmark(self, name):
            return self.marks[name]

    def __init__(self, template):
        self.tmpl = template

    def calcular_estilo(self, estilo):
        
        style = []
        
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
                    font.append('color %s' % color)
                    
                # bold
                if fuente.attrib.get('bold', None):
                    font.append('bold %s' % fuente.attrib['bold'])
                
                # italic
                if fuente.attrib.get('italic', None):
                    font.append('italic %s' % fuente.attrib['italic'])
                    
                # underline
                if fuente.attrib.get('underline', None):
                    font.append('underline %s' % fuente.attrib['underline'])
                
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
            patron_relleno = ''
            if estilo.attrib.get('pattern', None):
                patron_relleno = estilo.attrib['pattern']
                pattern.append('pattern %s' % patron_relleno)
            
            if estilo.attrib.get('bgcolor', None):
                if not patron_relleno:
                    pattern.append('pattern solid')
                    
                pattern.append('fore-color %s' % estilo.attrib['bgcolor'])
                
            if pattern:
                style.append('pattern: %s' % (','.join(pattern)))
                
            border = []
            if estilo.find('border') != None:
                borde = estilo.find('border')
                
                # color
                color_borde = ''
                if borde.attrib.get('color', None):
                    color_borde = borde.attrib['color']
                
                # line
                linea_borde = 'thin'
                if borde.attrib.get('line', None):
                    linea_borde = borde.attrib['line']
                
                # top
                top_color = ''
                top_line = ''
                if borde.find('top') != None:
                    tp = borde.find('top')
                    if tp.attrib.get('color', None):
                        top_color = tp.attrib['color']
                        
                    elif color_borde:
                        top_color = color_borde
                        
                    if tp.attrib.get('line', None):
                        top_line = tp.attrib['line']
                    
                    elif linea_borde:
                        top_line = linea_borde
                        
                if top_color:
                    border.append('top_color %s' % top_color)
                    
                if top_line:
                    border.append('top %s' % top_line)
                
                # bottom
                bottom_color = ''
                bottom_line = ''
                if borde.find('bottom') != None:
                    bt = borde.find('bottom')
                    if bt.attrib.get('color', None):
                        bottom_color = bt.attrib['color']
                        
                    elif color_borde:
                        bottom_color = color_borde
                        
                    if bt.attrib.get('line', None):
                        bottom_line = bt.attrib['line']
                    
                    elif linea_borde:
                        bottom_line = linea_borde

                if bottom_color:
                    border.append('bottom_color %s' % bottom_color)
                    
                if bottom_line:
                    border.append('bottom %s' % bottom_line)
                
                # left
                left_color = ''
                left_line = ''
                if borde.find('left') != None:
                    lf = borde.find('left')
                    if lf.attrib.get('color', None):
                        left_color = lf.attrib['color']
                        
                    elif color_borde:
                        left_color = color_borde
                        
                    if lf.attrib.get('line', None):
                        left_line = lf.attrib['line']
                    
                    elif linea_borde:
                        left_line = linea_borde

                if left_color:
                    border.append('left_color %s' % left_color)
                    
                if left_line:
                    border.append('left %s' % left_line)

                # right
                right_color = ''
                right_line = ''
                if borde.find('right') != None:
                    rt = borde.find('right')
                    if rt.attrib.get('color', None):
                        right_color = rt.attrib['color']
                        
                    elif color_borde:
                        right_color = color_borde
                        
                    if rt.attrib.get('line', None):
                        right_line = rt.attrib['line']
                    
                    elif linea_borde:
                        right_line = linea_borde

                if right_color:
                    border.append('right_color %s' % right_color)
                    
                if right_line:
                    border.append('right %s' % right_line)

                if border:
                    style.append('border: %s' % (','.join(border)))
                    
        return style
    
    def create(self, params, filename=None):
        """
        IN
          params    <dict>
          filename  <str> (opcional)
          
        OUT
          El XML del informe
          <str>
        """
        
        util = self.Util()
        self.tmpl.globals['util'] = util
        self.tmpl.globals['xlrd'] = xlrd

        informe_xml = self.tmpl.render(**params).encode('utf-8')
        
        root = etree.fromstring(informe_xml)
        
        wb = Workbook()
        
        estilos = {}
        
        xfs0 = XFStyle()
        
        n_sheet = 0
        for sheet in root.iter('sheet'):
            
            n_sheet += 1
            cols_width = None
            
            # title
            title = sheet.attrib.get('title', 'Sheet-%d' % n_sheet)
            
            # auto-width
            sheet_width = sheet.attrib.get('width')
            cols_width = {}
                
            ws = wb.add_sheet(title, True)
            
            util.init_count()
            for item in sheet:
                
                # style
                if item.tag == 'style':
                    estilos[item.attrib['name']] = easyxf(';'.join(self.calcular_estilo(item)))
                    
                # image
                if item.tag == 'image':
                    bm_path = item.find('path').text
                    col = int(item.attrib.get('col', 0))
                    scale_x = float(item.attrib.get('scale_x', '1'))
                    scale_y = float(item.attrib.get('scale_y', '1'))
                    ws.insert_bitmap(bm_path, util.current_line(), col, scale_x=scale_x, scale_y=scale_y) 
                
                # cell
                if item.tag == 'cell':
                    
                    col = int(item.attrib['col'])
                    
                    num_format = None
                    
                    # width
                    width = item.attrib.get('width', sheet_width)
                        
                    if width is not None:
                        if not cols_width.get(col):
                            cols_width[col] = dict(auto=width == 'auto', 
                                                   width=int(width) if width != 'auto' else 0)
                        
                    # value
                    value = item.find('value')
                    dato = value.text
                    # type: aplicar una conversión (str, int, float, ...)
                    type_ = item.attrib.get('type')
                    if type_:
                        tipo = type_.split(';')
                        
                        # date
                        if tipo[0] == 'date':
                            try:
                                dato = strtodate(dato, fmt='%Y-%m-%d')
                            except:
                                dato = None
    
                        # time
                        elif tipo[0] == 'time':
                            try:
                                dato = strtotime(dato)
                            except:
                                dato = None
                        
                        # formula
                        elif tipo[0] == 'formula':
                            dato = Formula(dato)
                        
                        # resto de tipos
                        else:
                            if dato != '':
                                try:
                                    f = lambda t,v: t(v)
                                    dato = f(eval(tipo[0]), dato)
                                except:
                                    dato = None
                        
                        # date;dd/mm/yyyy
                        # date;dd/mmm/yyyy
                        # date;NN D MMMM YYYY
                        # time;hh:mm
                        # float;#,##0.00
                        # float;+#,##0.00
                        # float;#,##0.00;[RED]-#,##0.00
                        if len(tipo) > 1:
                            num_format = ';'.join(tipo[1:])
                            
                        #print dato, tipo, num_format
    
                    # style: aplicar un estilo
                    estilo = item.find('style')
                    xfs = xfs0
                    if estilo != None:
                        if not estilos.has_key(estilo.attrib['name']):
                            xfs = easyxf(';'.join(self.calcular_estilo(estilo))) 
        
                            estilos[estilo.attrib['name']] = xfs
                            
                        else:
                            xfs = estilos[estilo.attrib['name']]
                        
                    xfs.num_format_str = 'General'    
                    if num_format:
                        if not xfs:
                            xfs = XFStyle()

                        xfs.num_format_str = num_format
                        
                    # merge
                    if item.attrib.has_key('merge') and item.attrib['merge']:
                        try:
                            _merge = re.search(r'(\d+)\s+(\d+)', item.attrib['merge'], re.U)
                            if _merge:
                                hg = int(_merge.group(1))
                                wd = int(_merge.group(2))
                            
                                _current_line = util.current_line()
                                ws.write_merge(_current_line, _current_line + hg - 1,
                                               col, col + wd -1, 
                                               dato, xfs)
                            else:
                                raise Exception(u'merge: Invalid format')
                        
                        except Exception:
                            ws.write(util.current_line(), col, dato, xfs)
                            
                    else:
                        ws.write(util.current_line(), col, dato, xfs)
                        
                    # width
                    colw = cols_width.get(col, None)
                    if colw is not None:
                        
                        if colw['auto']:
                            try:
                                width_ = len(str(dato))
                            except:
                                width_ = len(unicode(dato))
                                
                            if width_ > colw['width']:
                                cols_width[col]['width'] = width_
                                
                elif item.tag == 'line_feed':
                    n = int(item.attrib.get('n', 1))
                    util.line_feed(n)
                    
                elif item.tag == 'bookmark':
                    util.add_bookmark(item.attrib['name'])
            
            # width
            if cols_width is not None:
                for col, colw in cols_width.iteritems():
                    
                    if colw['width'] < 10:
                        colw['width'] = colw['width'] + 2
                        
                    ws.col(col).width = colw['width']*256
                
        if filename:
            wb.save(filename)
            
        return informe_xml