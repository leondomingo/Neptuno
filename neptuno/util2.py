# -*- coding: utf-8 -*-

from datetime import datetime, date

# strto...
def strtodate(s, fmt='%d/%m/%Y'):
    return datetime.strptime(s, fmt).date()

def strtotime(s, fmt='%H:%M'):
    return datetime.strptime(s, fmt).time()

def strtobool(s):
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False    
    else:
        raise TypeError('No es un tipo booleano')    

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