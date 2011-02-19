# -*- coding: utf-8 -*-

import os
import smtplib
from email import Encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def enviar_email(remitente, destinatarios, asunto, mensaje, 
                 servidor, login, password, ficheros=[]):
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
    
    if ficheros:
        msg_f = MIMEMultipart()
        msg_f.attach(msg)
        
        msg = msg_f
        
        for f in ficheros:
            part = MIMEBase('application', 'otect-stream')
            part.set_payload(open(f, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 
                            'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)
            
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