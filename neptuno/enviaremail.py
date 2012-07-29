# -*- coding: utf-8 -*-

from sendmail import send_mail

def enviar_email(remitente, destinatarios, asunto, mensaje, 
                 servidor, login, password, ficheros=[], html='', cc=[], bcc=[], 
                 charset='iso-8859-1'):
    
    send_mail(remitente, destinatarios, asunto, mensaje, servidor, login, password,
              files=ficheros, html=html, cc=cc, bcc=bcc, charset=charset)
    
def normalizar_a_html(texto):
    return texto.\
        replace('\'', '&#39;').\
        replace('&', '&amp;').\
        replace('#', '&#35;').\
        replace('á', '&aacute;').\
        replace('Á', '&Aacute;').\
        replace('é', '&eacute;').\
        replace('É', '&Eacute;').\
        replace('í', '&iacute;').\
        replace('Í', '&Iacute;').\
        replace('ó', '&oacute;').\
        replace('Ó', '&Oacute;').\
        replace('ú', '&uacute;').\
        replace('Ú', '&Uacute;').\
        replace('ü', '&uuml;').\
        replace('Ü', '&Uuml;').\
        replace('ñ', '&ntilde;').\
        replace('Ñ', '&Ntilde;').\
        replace('<', '&lt;').\
        replace('>', '&gt;').\
        replace('¡', '&iexcl;').\
        replace('?', '&iquest;').\
        replace('"', '&quot;').\
        replace('%', '&#37;')
        