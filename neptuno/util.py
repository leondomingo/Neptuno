# -*- coding: utf-8 -*-

import re
import simplejson
import datetime as dt
from decimal import Decimal

def get_parametros(req, parametros):
    form = req.form
    
    resultado = {}
    for p in parametros:
        valor = form.get(p, None)
        if valor != None:
            valor = valor.value
            
        resultado[p] = valor
            
    return resultado

class EFaltaParametro(Exception):
    
    def __init__(self, param):
        Exception.__init__(self)
        self.param = param
        
    def __str__(self):
        return 'Falta el parámetro "%s"' % self.param

def get_param(form, nombre, tipo, opcional=False, por_defecto=None):
    """
    Devuelve el parámetro 'nombre' de tipo 'tipo' del diccionario 'form'
    
    Ejemplos:
      # un valor entero "obligatorio"
      i = get_param(req.form, 'entero', int)
      
      # un valor entero "opcional" (valor por defecto=None)
      i = get_param(req.form, 'entero', int, opcional=True)
      
      # un valor entero "opcional" con valor por defecto
      i = get_param(req.form, 'entero', int, opcional=True, por_defecto=100)
      
      # un valor que se obtiene después de pasar por una función
      x = get_param(req.form, 'x', 
                    lambda v: simplejson.loads(str(v)))
                    
      f = get_param(req.form, 'fecha', strtodate)     
    """
    
    if not opcional:
        if not form.has_key(nombre):
            raise EFaltaParametro(nombre)
        
        else:
            try:
                return tipo(form[nombre].value)
            except:
                return por_defecto
                    
    else:
        if form.has_key(nombre):
            try:
                return tipo(form[nombre].value)
            except:
                return por_defecto
        
        else:
            return por_defecto

def get_paramw(params, nombre, tipo, opcional=False, por_defecto=None):
    """
    Devuelve el parámetro 'nombre' de tipo 'tipo' del diccionario 'params'
    
    Ejemplos:
      # un valor entero "obligatorio"
      i = get_paramw(params, 'entero', int)
      
      # un valor entero "opcional" (valor por defecto=None)
      i = get_paramw(params, 'entero', int, opcional=True)
      
      # un valor entero "opcional" con valor por defecto
      i = get_paramw(params, 'entero', int, opcional=True, por_defecto=100)
      
      # un valor que se obtiene después de pasar por una función
      x = get_paramw(params, 'x', 
                     lambda v: simplejson.loads(str(v)))
                    
      f = get_paramq(params, 'fecha', strtodate)     
    """
    
    if not opcional:
        if not params.has_key(nombre):
            raise EFaltaParametro(nombre)
        
        else:
            try:
                return tipo(params[nombre])
            except:
                raise EFaltaParametro(nombre)
                    
    else:
        if params.has_key(nombre):
            try:
                return tipo(params[nombre])
            except:
                return por_defecto
        
        else:
            return por_defecto
        
def jsonize(func):
    def _jsonize(_self, *args, **kwargs):
        return simplejson.dumps(func(_self, *args, **kwargs))
        
    return _jsonize

def get_params(form, excepciones):
    """
    Devuelve un diccionario con los parámetros de 'form' que no están
    incluidos en 'excepciones'
    
    IN
      form         <dict>
      excepciones  <list>
      
    OUT
      <dict>
    """
    
    resultado = {}
    for k, v in form.items():
        if k not in excepciones:
            resultado[k] = str(v.value)
        
    return resultado

def get_paramsw(params, excepciones):
    """
    Devuelve un diccionario con los parámetros de 'params' que no están
    incluidos en 'excepciones'.
    
    IN
      params       <dict>
      excepciones  <list>
      
    OUT
      <dict>
    """
    
    resultado = {}
    for k, v in params.iteritems():
        if k not in excepciones:
            resultado[k] = str(v)
        
    return resultado

def get_usuario(form):    
    return get_param(form, 'id_usuario', int), get_param(form, 'id_sesion', str),

#def strtodate(s, fmt='%d/%m/%Y'):
#    return datetime.strptime(s, fmt).date()

class EFechaIncorrecta(Exception):
    def __init__(self, s):
        Exception.__init__(self)
        self.s = s
        
    def __str__(self):
        return 'La fecha "%s" es incorrecta' % self.s

def strtodate(s, fmt='%d/%m/%Y', no_exc=False):
    """
    IN
      s <str>
      
    OUT
      <date>
    """
    
    # build regex
    regex = r'^\s*%s\s*$' % (fmt.replace('%d', r'(?P<day>\d{1,2})').\
                             replace('%m', r'(?P<month>\d{1,2})').\
                             replace('%Y', r'(?P<year>\d{4})'))
        
    m1 = re.search(regex, s)
    if m1:
        try:
            day = int(m1.groupdict().get('day') or 1)
            month = int(m1.groupdict().get('month') or 1)
            year = int(m1.groupdict().get('year') or 1)
            
            return dt.date(year, month, day)
        
        except Exception:
            if no_exc: return None
            raise Exception('Fecha incorrecta: "%s"' % s)

#def strtodate(s, no_exc=False, month_day=False):
#    """
#    Devuelve la fecha representada por la cadena 's'.
#    Formatos posibles para 's':
#      d/m/yyyy (1/2/1970, 01/2/1970, 1/02/1970, 01/02/1970)
#      d-m-yyyy (1-2-1970, 01-2-1970, 1-02-1970, 01-02-1970)
#      yyyy/m/d (1970/2/1, 1970/2/01, 1970/02/1, 1970/02/01)
#      yyyy-m-d (1970-2-1, 1970-2-01, 1970-02-1, 1970-02-01)
#      
#      *(d y m representados con 1 ó 2 dos dígitos)     
#    
#    IN
#      s <str>
#      
#    OUT
#      <date>
#    """
#    
#    # dd/mm/yyyy
#    # dd-mm-yyyy
#    m1 = re.search(r'^\s*(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s*$', s)
#    if m1:
#        try:
#            return date(int(m1.group(3)),
#                        int(m1.group(2)),
#                        int(m1.group(1))
#                        )
#        except:
#            if no_exc: return None
#            raise EFechaIncorrecta(s)
#        
#    else:
#        # yyyy/mm/dd
#        # yyyy-mm-dd
#        m2 = re.search(r'^\s*(\d{4})[/-](\d{1,2})[/-](\d{1,2})\s*$', s)
#        
#        if m2:
#            try:        
#                return date(int(m2.group(1)),
#                            int(m2.group(2)),
#                            int(m2.group(3))
#                            )
#            except:
#                if no_exc: return None
#                raise EFechaIncorrecta(s)
#        else:
#            if no_exc: return None
#            raise EFechaIncorrecta(s)
        
def strtodate2(s):
    return strtodate(s, no_exc=True)

def strtotime(s):
    m = re.search(r'^(\d{1,2}):(\d{1,2}):?(\d{1,2})?', s)
    return dt.time(int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))

def strtobool(s):
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise TypeError('No es un tipo booleano')
    
def strlen(v, l):
    """
    """
    
    v = str(v)
    
    if len(v) != l:
        raise TypeError('Longitud incorrecta')
    
    return v
    
# ...tostr
def datetostr(d, fmt='%d/%m/%Y'):
    if d is None:
        return ''
    
    else:
        try:
            return d.strftime(fmt)
        except ValueError:
            return ''

def timetostr(t, fmt='%H:%M'):
    if t is None:
        return ''
    
    else:
        return t.strftime(fmt)
    
def inicio_fin_mes(d):
    """
    Devuelve el primer y el último día del mes en la fecha 'fecha'.
    
    IN
      fecha <date>
      
    OUT
      (<date>, <date>)
    """
    
    inicio = dt.date(d.year, d.month, 1)
    mes_siguiente = inicio + dt.timedelta(days=31)
    fin = dt.date(mes_siguiente.year, mes_siguiente.month, 1) - dt.timedelta(days=1)

    return (inicio, fin,)

def inicio_fin_semana(d):
    """
    Returns monday and sunday of the week for the given date. 
    IN
      d  <date>
      
    OUT
      (<date>, <date>,)
    """
    
    inicio = d - dt.timedelta(d.weekday())
    fin = inicio + dt.timedelta(days=6)
    
    return (inicio, fin,)
    
def format_float(value, thousands_sep=',', decimal_sep='.', 
                 show_sign=False, n_dec=2, format=None):
    """
    IN
      value          <float> / <str>
      thousands_sep  <str>  (opcional => ',')
      decimal_sep    <str>  (opcional => '.')
      show_sign      <bool> (opcional => False)
      n_dec          <int>  (opcional => 2)
      format         <str>  (opcional => None)
      
    OUT
      <str>
      x,xxx.xx
      x.xxx,xx
      +x,xxx.xx
      -x,xxx.xx      
    """

    if format:
        #  9,999.00  (thousands_sep="," decimal_sep=".", n_dec=2)
        #  9.999,00  (thousands_sep="." decimal_sep=",", n_dec=2)
        #  9,999.000 (thousands_sep="," decimal_sep=".", n_dec=3)
        # +9.999,00  (thousands_sep="." decimal_sep=",", n_dec=2, show_sign=True)
        #   9999.00  (thousands_sep="", decimal_sep=".", n_dec=2)
        m_format = re.search(r'^(\+)?[1-9](\.|,)?[1-9]{3}(\.|,)(0*)$', format)
        if m_format:
            show_sign = m_format.group(1) is not None
            thousands_sep = m_format.group(2) or ''
            decimal_sep = m_format.group(3) or ''
            n_dec = len(m_format.group(4))
    
    fmt = '%%+%d.%df' % (n_dec, n_dec)
    
    if isinstance(value, int):
        value = float(value)
    
    if isinstance(value, float) or isinstance(value, Decimal):
        text = fmt % value
        
    elif isinstance(value, str) or value is None:
        text = fmt % float(value or 0)
    
    m = re.search(r'([\+-]?)0*(\d*)\.(\d+)', text)
    
    sign = m.group(1)
    if sign and sign != '-':
        if not show_sign:
            sign = ''
    
    int_part = m.group(2)
    dec_part = m.group(3)
    
    if int_part:
        parte_entera = range(len(int_part))
        parte_entera.reverse()
        
        j = 0
        result = ''
        for i, j in zip(parte_entera, range(len(int_part))):
            if j != 0 and j % 3 == 0:
                result = thousands_sep + result
                
            result = int_part[i] + result
            
    else:
        result = '0'        
    
    # 1,234.56
    return '%(sign)s%(int_part)s%(sep)s%(dec_part)s' % \
                dict(sign=sign or '',
                     int_part=result, 
                     sep=decimal_sep, 
                     dec_part=dec_part)

def default_fmt_float(value):
    return format_float(value, thousands_sep='.', decimal_sep=',')
