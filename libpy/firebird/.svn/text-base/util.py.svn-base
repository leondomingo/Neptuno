# -*- coding: utf-8 -*-

from datetime import datetime, time
from sqlalchemy import Column, Sequence, Integer, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.databases.firebird import FBString, FBDate, FBInteger
from libpy.firebird.const_datos_olympo import BOOL_TRUE, BOOL_FALSE

# funciones    

def clase_codobjeto(cod_clase):
    """
    def clase_codobjeto(int cod_clase)
    Devuelve una cadena formada por el nombre de la clase más 'COD_OBJETO'. Por ejemplo "OBJ_12345.COD_OBJETO"
    """
    return 'obj_%d.cod_objeto' % cod_clase

def nombre_tabla(cod_clase):
    """
    def nombre_tabla(int cod_clase)
    Devuelve el nombre de una tabla (OBJ_XXXX) que corresponde a la clase 'cod_clase'"""
    return 'obj_%d' % cod_clase

def nombre_coleccion(clase):
    """
    def nombre_coleccion(int clase)
    Devuelve el nombre de la colección (COL_XXXX) de la clase 'clase'
    """
    return 'col_%d' % clase

def nombre_largo(clase, atributo):
    if isinstance(clase, int):
        return 'obj_%d_%s' % (clase, atributo.lower())
    else:
        return '%s_%d' % (clase, atributo.lower())

def cod_atributo(atributo):
    """
    def cod_atributo(str atributo)
    Devuelve el código de un atributo"""
    return int(atributo.upper().replace('ATR_', ''))

def cod_clase(clase):
    """
    def cod_clase(str clase)
    Devuelve el código de la clase 'clase' (OBJ_XXX)"""
    return int(clase.upper().replace('OBJ_', ''))

def cod_objeto(clase):
    """
    def cod_objeto(int clase)
    Devuelve el objeto 'Column' correspondiente al COD_OBJETO de la clase 'clase'""" 
    return Column('cod_objeto', FBInteger, Sequence('GEN_%d' % clase, increment=1), primary_key=True)

def atributo_objeto(atributo, clase_enlazada):
    """
    def atributo_objeto(str atributo, int clase_enlazada)
    Devuelve el objeto 'Column' correspondiente a un atributo tipo 'objeto' 
    enlazado a la clase 'clase_enlazada'
    """
    return Column(atributo, Integer, ForeignKey(clase_codobjeto(clase_enlazada)))

def fecha_de_creacion(atributo):
    """
    def fecha_de_creacion(str atributo)
    Devuelve un objeto 'Column' para el atributo 'atributo' configurado como
    un atributo 'Fecha de Creación'"""
    return Column(atributo, TIMESTAMP, default=datetime.now())

def fecha_de_actualizacion(atributo):
    """
    def fecha_de_actualizacion(str atributo)
    Devuelve un objeto 'Column' para el atributo 'atributo' configurado como
    un atributo 'Fecha de Actualización'"""    
    return Column(atributo, TIMESTAMP, onupdate=datetime.now(), default=datetime.now())

class ValorLogico(object):
    
    def __init__(self, field):
        # 1, 2 ó None        
        self.field = field
        
    def __get__(self, instance, cls):
        
        valor_logico = getattr(instance, self.field) 
        
        if valor_logico == BOOL_TRUE:        
            return True
        
        elif valor_logico == BOOL_FALSE:
            return False
        
        else:
            return None        
    
    def __set__(self, instance, valor):
                
        if valor is None:
            setattr(instance, self.field, None)
        else:
            if valor:
                setattr(instance, self.field, BOOL_TRUE)
            else:
                setattr(instance, self.field, BOOL_FALSE)
    
def sin_espacios(cadena):
    """
    def sin_espacios(str cadena)
    Devuelve una cadena en minúsculas, sin espacios y cambiando las letras acentuadas 
    por su correspondiente sin acentuar
    """
    
    cadena = str(cadena.encode('utf-8')).lower().replace(' ', '_')
    
    #print 'cadena =', cadena, type(cadena)
                
    anterior = '_'
    resultado = ''            
    for c in cadena:
        if c in ['á', 'é', 'í', 'ó', 'ú', 'ü', 'ñ'] or str(c).isalpha() or str(c).isdigit():
            if c == 'á':
                c = 'a'
            elif c == 'é':
                c = 'e'
            elif c == 'í': 
                c = 'i'
            elif c == 'ó':
                c = 'o'
            elif c in ['ú', 'ü']:
                c = 'u'
            elif c == 'ñ':
                c = 'n'
        else:
            c = '_'
            
        if anterior == '_':
            c = c.upper()
        
        if c != '_':
            resultado += c
        
        anterior = c
    
    print 'resultado =', resultado
    return resultado

def calcular_funcionfecha(funcion):
    
    FF_FECHA = 0
    FF_INICIO_SEMANA = 1
    FF_INICIO_MES = 2
    FF_INICIO_MES_ANTERIOR = 3
    FF_INICIO_TRIMESTRE = 4
    FF_INICIO_ANYO = 5
    FF_FIN_SEMANA = 6
    FF_FIN_MES = 7
    FF_FIN_MES_ANTERIOR = 8
    FF_FIN_TRIMESTRE = 9
    FF_FIN_ANYO = 10
    FF_INICIO_SEMANA_ANTERIOR = 11
    FF_FIN_SEMANA_ANTERIOR = 12
    FF_INICIO_SEMANA_SIGUIENTE = 13
    FF_FIN_SEMANA_SIGUIENTE = 14

    valor = ''
    hoy = datetime.today()
    if funcion == FF_FECHA:
        valor = 'CURRENT_DATE'
    elif funcion == FF_INICIO_SEMANA:
        valor = datetime.fromordinal(hoy.toordinal() - hoy.weekday()).strftime('%Y/%m/%d')
    
    elif funcion == FF_INICIO_MES:
        valor = datetime(hoy.year, hoy.month, 1).strftime('%Y/%m/%d')
    
    elif funcion == FF_INICIO_MES_ANTERIOR:
        if hoy.month == 1:
            anyo = hoy.year - 1
            mes = 12
        else:
            anyo = hoy.year
            mes = hoy.month - 1
            
        valor = datetime(anyo, mes, 1).strftime('%Y/%m/%d')
    
    elif funcion == FF_INICIO_TRIMESTRE:
        trimestre = (hoy.month - 1) / 3 + 1
        
        if trimestre == 1:
            inicio = datetime(hoy.year, 1, 1)
        elif trimestre == 2:
            inicio = datetime(hoy.year, 4, 1)
        elif trimestre == 3:
            inicio = datetime(hoy.year, 7, 1)
        else:
            inicio = datetime(hoy.year, 10, 1)
            
        valor = inicio.strftime('%Y/%m/%d')
    
    elif funcion == FF_INICIO_ANYO:
        valor = datetime(hoy.year, 1, 1).strftime('%Y/%m/%d')
        
    elif funcion == FF_FIN_SEMANA:
        valor = datetime.fromordinal(hoy.toordinal() + 6 - hoy.weekday()).strftime('%Y/%m/%d') 
    
    elif funcion == FF_FIN_MES:
        if hoy.month == 12:
            anyo = hoy.year + 1
            mes = 1
        else:
            anyo = hoy.year
            mes = hoy.month + 1
            
        # un día menos del día 1 del mes siguiente
        valor = datetime.fromordinal(datetime(anyo, mes, 1).toordinal() - 1).strftime('%Y/%m/%d')
    
    elif funcion == FF_FIN_MES_ANTERIOR:
        # un día antes del inicio de este mes (mes de hoy)        
        valor = datetime.fromordinal(datetime(hoy.year, hoy.month, 1).toordinal() -1)
    
    elif funcion == FF_FIN_TRIMESTRE:
        trimestre = (hoy.month - 1) / 3 + 1
        
        if trimestre == 1:
            inicio = datetime(hoy.year, 3, 31)
        elif trimestre == 2:
            inicio = datetime(hoy.year, 6, 30)
        elif trimestre == 3:
            inicio = datetime(hoy.year, 9, 30)
        else:
            inicio = datetime(hoy.year, 12, 31)
            
        valor = inicio.strftime('%Y/%m/%d')
    
    elif funcion == FF_FIN_ANYO:
        hoy = datetime.today()
        valor = datetime(hoy.year, 12, 31).strftime('%Y/%m/%d')
        
    elif funcion == FF_INICIO_SEMANA_ANTERIOR:
        valor = datetime.fromordinal(hoy.toordinal() - 7 - hoy.weekday()).strftime('%Y/%m/%d')
    
    elif funcion == FF_FIN_SEMANA_ANTERIOR:
        valor = datetime.fromordinal(hoy.toordinal() - 1 - hoy.weekday()).strftime('%Y/%m/%d')
    
    elif funcion == FF_INICIO_SEMANA_SIGUIENTE:
        valor = datetime.fromordinal(hoy.toordinal() + 7 - hoy.weekday()).strftime('%Y/%m/%d')
    
    elif funcion == FF_FIN_SEMANA_SIGUIENTE:
        valor = datetime.fromordinal(hoy.toordinal() + 13 - hoy.weekday()).strftime('%Y/%m/%d')
    
    return valor

def calcular_funcionentero(funcion):
    
    FE_DIA = 0
    FE_MES = 1
    FE_ANYO = 2
    
    hoy = datetime.today()
    
    if funcion == FE_DIA:
        valor = str(hoy.day)
    
    elif funcion == FE_MES:
        valor = str(hoy.month)
    
    elif funcion == FE_ANYO:
        valor = str(hoy.year)
    
    return valor

def operador_insensitive(filtro, operador, valor, tipo_dato):

    CC_INCLUYE = 0
    CC_NOINCLUYE = 1
    CC_EMPIEZAPOR = 2
    CC_MENOR = 3
    CC_MAYOR = 4
    CC_IGUAL = 5
    CC_DISTINTO = 6
    CC_MAYORIGUAL = 7
    CC_MENORIGUAL = 8
#    CC_TERMINAPOR = 9
    CC_ULTIMOSDIAS = 10
    CC_PROXIMOSDIAS = 11
    
    funciones_fecha = ['<Fecha>', \
                       '<InicioSemana>', \
                       '<InicioMes>', \
                       '<InicioMesAnterior>', \
                       '<InicioTrimestre>', \
                       '<InicioAño>', \
                       '<FinSemana>', \
                       '<FinMes>', \
                       '<FinMesAnterior>', \
                       '<FinTrimestre>', \
                       '<FinAño>', \
                       '<InicioSemanaAnterior>', \
                       '<FinSemanaAnterior>', \
                       '<InicioSemanaSiguiente>', \
                       '<FinSemanaSiguiente>']    
    
    funciones_entero = ['<Dia>', \
                        '<Mes>', \
                        '<Año>']
  
    resultado = ''
    if valor == '':
        resultado = filtro
        if operador == CC_INCLUYE or operador == CC_EMPIEZAPOR or \
        operador == CC_IGUAL:
            resultado = '(' + resultado + ' IS NULL '
          
            if isinstance(tipo_dato, FBString): # tipo_datos == 'str':            
                resultado = resultado + " OR %s = '')" % filtro # ' OR COALESCE(' + filtro + ", '') = '')"
            else:
                resultado += ')'
                
        elif operador == CC_NOINCLUYE:  resultado += ' IS NOT NULL'
        elif operador == CC_MENOR:      resultado += " < ''"
        elif operador == CC_MAYOR:      resultado += " > ''"
        elif operador == CC_DISTINTO:   resultado += ' IS NOT NULL'
        elif operador == CC_MAYORIGUAL: resultado += " >= ''"
        elif operador == CC_MENORIGUAL: resultado += " <= ''"
        
    else:        
        # fechas
        if isinstance(tipo_dato, FBDate): # tipo_datos == 'date':
            if operador != CC_ULTIMOSDIAS and operador != CC_PROXIMOSDIAS:
                try:
                    l = map(lambda f: f.upper(), funciones_fecha)
                    i = l.index(str(valor).upper())
                    
                    # calcular el valor de la función de fecha i
                    valor = str(valor).replace(valor, calcular_funcionfecha(i))
                except:
                    # 'valor' no está en la lista de funciones
                    if isinstance(valor, datetime):
                        fecha = valor.date()
                        hora = valor.time()
                        if fecha.year == 1900 and fecha.month == 1 and fecha.day == 1:
                            valor = hora.strftime('%H:%M')
                        else:
                            valor = fecha.strftime('%Y/%m/%d')
            
            resultado = filtro
            
            # operadores 
            if operador == CC_INCLUYE:        resultado += " = '%s'" % valor
            elif operador == CC_NOINCLUYE:    resultado += " <> '%s'" % valor
            elif operador == CC_EMPIEZAPOR:   resultado += " >= '%s'" % valor
            elif operador == CC_MENOR:        resultado += " < '%s'" %  valor
            elif operador == CC_MAYOR:        resultado += " > '%s'"  % valor
            elif operador == CC_IGUAL:        resultado += " = '%s'" % valor
            elif operador == CC_DISTINTO:     resultado += " <> '%s'" % valor
            elif operador == CC_MAYORIGUAL:   resultado += " >= '%s'" % valor
            elif operador == CC_MENORIGUAL:   resultado += " <= '%s'" % valor
            elif operador == CC_ULTIMOSDIAS:  resultado += " >= ('%s') AND (%s <= CURRENT_DATE)" % (valor.strftime('%Y/%m/%d'), filtro)
            elif operador == CC_PROXIMOSDIAS: resultado += " >= CURRENT_DATE AND %s <= ('%s')" % (filtro, valor.strftime('%Y/%m/%d')) 
            
        # cadena
        elif isinstance(tipo_dato, FBString): # tipo_datos == 'memo' or tipo_datos == 'blob' or tipo_datos == 'str':
            
            resultado = 'UPPER(%s)' % filtro
            valor = valor.upper()            
                
            # operadores            
            if operador == CC_INCLUYE:        resultado += " Like '%" + valor + "%'"
            elif operador == CC_NOINCLUYE:    resultado += " Not Like '%" + valor + "%'"
            elif operador == CC_EMPIEZAPOR:   resultado += " Like '" + valor + "%'"
            elif operador == CC_MENOR:        resultado += " < '%s'" % valor
            elif operador == CC_MAYOR:        resultado += " > '%s'" % valor
            elif operador == CC_IGUAL:        resultado += " = '%s'" % valor
            elif operador == CC_DISTINTO:     resultado += " <> '%s'" % valor
            elif operador == CC_MAYORIGUAL:   resultado += " >= '%s'" % valor
            elif operador == CC_MENORIGUAL:   resultado += " <= '%s'" % valor
            elif operador == CC_ULTIMOSDIAS:  resultado += " >= ('%s') AND (%s <= CURRENT_DATE)" % (valor.strftime('%Y/%m/%d'), filtro)
            elif operador == CC_PROXIMOSDIAS: resultado += " >= CURRENT_DATE AND %s <= ('%s')" % (filtro, valor.strftime('%Y/%m/%d'))

        else:
            # entero
            if isinstance(tipo_dato, FBInteger):
                resultado = filtro
            else:
                # real
                resultado = 'CAST(%s as NUMERIC(9, 2))' % filtro
            
            try:
                l = map(lambda f: f.upper(), funciones_entero)
                i = l.index(str(valor).upper())
                
                valor = str(valor).replace(str(valor), calcular_funcionentero(i))
            except ValueError:
                pass

            # tratar valor para quitar separador de miles (creo que no hace falta)
            
            valor = str(valor).replace(',', '.')
                
            # operadores            
            if operador == CC_INCLUYE:      resultado += " Like '%" + valor + "%'"
            elif operador == CC_NOINCLUYE:  resultado += " Not Like '%" + valor + "%'"
            elif operador == CC_EMPIEZAPOR: resultado += " Like '" + valor + "%'"
            elif operador == CC_MENOR:      resultado += ' < %s' % valor
            elif operador == CC_MAYOR:      resultado += ' > %s' % valor
            elif operador == CC_IGUAL:      resultado += ' = %s' % valor
            elif operador == CC_DISTINTO:   resultado += ' <> %s' % valor
            elif operador == CC_MAYORIGUAL: resultado += ' >= %s' % valor
            elif operador == CC_MENORIGUAL: resultado += ' <= %s' % valor
            
    return resultado


def strtodate(fecha):
    """
    Devuelve el objeto datetime.datetime que se corresponde con la fecha expresada en 'fecha'.
    Formato de 'fecha':
        dd/mm/yy
        dd/mm/yyyy    
    """
    
    l = fecha.split('/')
    dia = int(l[0])
    mes = int(l[1])
    if len(l[2]) == 4:
        anyo = int(l[2])
    else:
        anyo = int('20' + l[2])
        
    return datetime(anyo, mes, dia)

def strtotime(hora):
    """
    Devuelve el objeto datetime.time que se corresponde con la hora expresada en 'hora'.
    Formato de 'hora':
        hh:mm
        hh:mm:ss
    """
    
    if hora.count(':') == 1:
        dt = datetime.strptime(hora, '%H:%M')
    else:
        dt = datetime.strptime(hora, '%H:%M:%S')
        
    return time(dt.hour, dt.minute, 0)

def tratar_cadena(cadena):
    """
    Devuelve la cadena, que está codificada en ISO-8859-1 (como en Olympo), a su
    versión en UTF-8. Si cadena es nulo devuelve '' (cadena vacía)
    
    IN
      cadena <str>
      
    OUT
      <str>
    """
    if cadena is None:
        return ''
    
    else:
        return cadena.decode('iso-8859-1').encode('utf-8')