# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

def enviar_email(remitente, destinatarios, asunto, mensaje, 
                 servidor, login, password):
    """
    IN
      remitente (<email>, <nombre>)
      destinatarios [(<email>, <nombre>), ...]
      asunto <str>
      mensaje <str>
      servidor <str>
      login <str>
      password <str>
      
      Por ejemplo,
        enviar_email(('pperez@gmail.com', 'Pepe Pérez'),
                     [('malopez@gmail.com', 'María López'), (mlopez@yahoo.com, 'María')],
                     'Hola, mundo!', '¿Qué tal por ahí?\n\nPepe',
                     'smtp.gmail.com', 
                     'pperez@gmail.com', 'ilovemarialopez')
                     
    """
    
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = '%s <%s>' % (remitente[1], remitente[0])
    
    nombres = ['%s <%s>' % (dst[1], dst[0]) for dst in destinatarios]
    msg['To'] = ';'.join(nombres)
    
    s = smtplib.SMTP(servidor)
    try:
        try:
            s.set_debuglevel(False)
            
            # autenticarse con el servidor
            s.ehlo()
            
            # tiene STARTTLS?
            if s.has_extn('STARTTLS'):
                s.starttls()
                s.ehlo() # re-identify ourselves over TLS connection
                
            # login
            s.login(login, password)
            
            emails_destino = [dst[0] for dst in destinatarios]
            
            # enviar e-mail
            resultado = s.sendmail(remitente[0], emails_destino, msg.as_string())
            
            return resultado
        
        finally:
            s.quit()
            
    except Exception, e:
        print str(e)
    
if __name__ == '__main__':
    
    import cStringIO
    
    mensaje = cStringIO.StringIO()    
    mensaje.write('ESTO ES OTRA pruebita')
    mensaje.seek(0)
    
    r = enviar_email(('leon.domingo@ender.es', 'León Domingo Ortín'),
                     [('tengounplanb@gmail.com', 'León Domingo Ortín'),
                      ('leon.domingo@gmail.com', 'Pepe Pérez')],
                     'Esto es una prueba', mensaje.read(),
                     'smtp.gmail.com', 'leon.domingo@ender.es', '5390ld')
    
    print r