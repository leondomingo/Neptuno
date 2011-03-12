# -*- coding: utf-8 -*-

from datetime import datetime, date
import simplejson
import re
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
                return por_defecto
                    
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

def strtodate(s, no_exc=False):
    """
    Devuelve la fecha representada por la cadena 's'.
    Formatos posibles para 's':
      d/m/yyyy (1/2/1970, 01/2/1970, 1/02/1970, 01/02/1970)
      d-m-yyyy (1-2-1970, 01-2-1970, 1-02-1970, 01-02-1970)
      yyyy/m/d (1970/2/1, 1970/2/01, 1970/02/1, 1970/02/01)
      yyyy-m-d (1970-2-1, 1970-2-01, 1970-02-1, 1970-02-01)
      
      *(d y m representados con 1 ó 2 dos dígitos)     
    
    IN
      s <str>
      
    OUT
      <date>
    """
    
    # dd/mm/yyyy
    # dd-mm-yyyy
    m1 = re.search(r'^\s*(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s*$', s)
    if m1:
        try:
            return date(int(m1.group(3)),
                        int(m1.group(2)),
                        int(m1.group(1))
                        )
        except:
            if no_exc: return None
            raise EFechaIncorrecta(s)
        
    else:
        # yyyy/mm/dd
        # yyyy-mm-dd
        m2 = re.search(r'^\s*(\d{4})[/-](\d{1,2})[/-](\d{1,2})\s*$', s)
        
        if m2:
            try:        
                return date(int(m2.group(1)),
                            int(m2.group(2)),
                            int(m2.group(3))
                            )
            except:
                if no_exc: return None
                raise EFechaIncorrecta(s)
        else:
            if no_exc: return None
            raise EFechaIncorrecta(s)
        
def strtodate2(s):
    return strtodate(s, no_exc=True)

def strtotime(s, fmt='%H:%M'):
    return datetime.strptime(s, fmt).time()

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
    
def inicio_fin_mes(fecha):
    """
    Devuelve el primer y el último día del mes en la fecha 'fecha'.
    
    IN
      fecha <date>
      
    OUT
      (<date>, <date>)
    """
    
    inicio = date(fecha.year, fecha.month, 1)
    
    mes_siguiente = date.fromordinal(inicio.toordinal() + 31)
    fin = date.fromordinal(date(mes_siguiente.year, 
                                mes_siguiente.month, 
                                1).toordinal() - 1)
    
    return (inicio, fin,)
    
def format_float(valor, separador_miles=',', separador_decimal='.',
                 mostrar_signo=False, n_decimales=2):
    """
    IN
      valor              <float> / <str>
      separador_miles    <str>  (opcional => ',')
      separador_decimal  <str>  (opcional => '.')
      mostrar_signo      <bool> (opcional => False)
      n_decimales        <int>  (opcional => 2)
      
    OUT
      <str>
      x,xxx.xx
      x.xxx,xx
      +x,xxx.xx
      -x,xxx.xx      
    """
    
    fmt = '%%%d.%df' % (n_decimales, n_decimales)
    
    if isinstance(valor, int):
        valor = float(valor)
    
    if isinstance(valor, float) or isinstance(valor, Decimal):
        texto = fmt % valor
        
    elif isinstance(valor, str) or valor is None:
        texto = fmt % float(valor or 0)
    
    m = re.search(r'([\+-]?)0*(\d*)\.(\d+)', texto)

    signo = m.group(1)
    if signo and signo != '-':
        if not mostrar_signo:
            signo = ''
    
    entero = m.group(2)
    decimal = m.group(3)
    
    if entero:
        parte_entera = range(len(entero))
        parte_entera.reverse()
        
        j = 0
        resultado = ''
        for i, j in zip(parte_entera, range(len(entero))):
            if j != 0 and j % 3 == 0:
                resultado = separador_miles + resultado
                
            resultado = entero[i] + resultado
            
    else:
        resultado = '0'        
    
    # 1,234.56
    return '%(signo)s%(p_entera)s%(sep)s%(p_decimal)s' % \
                dict(signo=signo or '',
                     p_entera=resultado, 
                     sep=separador_decimal, 
                     p_decimal=decimal)

def default_fmt_float(valor):
    return format_float(valor, separador_miles='.', separador_decimal=',')