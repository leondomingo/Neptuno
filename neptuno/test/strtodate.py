# -*- coding: utf-8 -*-

import re
from datetime import date

def strtodate(s, fmt='%d/%m/%Y', no_exc=False):
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
    
    # build regex
    regex = r'^\s*%s\s*$' % (fmt.replace('%d', r'(?P<day>\d{1,2})').\
                             replace('%m', r'(?P<month>\d{1,2})').\
                             replace('%Y', r'(?P<year>\d{4})'))
        
    # dd/mm/yyyy
    # dd-mm-yyyy
    #m1 = re.search(r'^\s*(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s*$', s)
    m1 = re.search(regex, s)
    if m1:
        try:
            day = int(m1.groupdict().get('day') or 1)
            month = int(m1.groupdict().get('month') or 1)
            year = int(m1.groupdict().get('year') or 1)
            
            return date(year, month, day)
        
        except Exception:
            raise
            if no_exc: return None
            raise Exception('Fecha incorrecta: "%s"' % s)
        
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
                raise Exception('Fecha incorrecta: "%s"' % s)
        else:
            if no_exc: return None
            raise Exception('Fecha incorrecta: "%s"' % s)

if __name__ == '__main__':
    
    d1 = strtodate('3-2011', fmt='%m-%Y')
    print d1    