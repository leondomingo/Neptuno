# -*- coding: utf-8 -*-

import os
import smtplib
from email import Encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def enviar_email(remitente, destinatarios, asunto, mensaje, 
                 servidor, login, password, ficheros=[], html='', charset='iso-8859-1'):
    """
    IN
      remitente      (<email>, <nombre>)
      destinatarios  [(<email>, <nombre>), ...]
      asunto         <str>
      mensaje        <str>
      servidor       <str>
      login          <str>
      password       <str>
      ficheros       [<str>, ...] (opcional)
      html           <str>        (opcional)
      
      Por ejemplo,
        enviar_email(('pperez@gmail.com', 'Pepe Pérez'),
                     [('malopez@gmail.com', 'María López'), (mlopez@yahoo.com, 'María')],
                     'Hola, mundo!', '¿Qué tal por ahí?\n\nPepe',
                     'smtp.gmail.com', 
                     'pperez@gmail.com', 'ilovemarialopez')
                     
    """
    
    msg = MIMEText(mensaje)
    msg.set_type('text/plain')
    msg.set_charset(charset)
    
    msg_root = None
    if html:
        msg_root = MIMEMultipart('related')
        msg_root.preamble = 'This is a multi-part message in MIME format.'
        
        if html:
            msg_alt = MIMEMultipart('alternative')
            
            msg_alt.attach(msg)
            
            msg_html = MIMEText(html)
            msg_html.set_type('text/html')
            msg_html.set_charset(charset)

            msg_alt.attach(msg_html)
            
            msg_root.attach(msg_alt)
            
        msg = msg_root
        
    if ficheros:
        if not msg_root:
            msg_root = MIMEMultipart()
            msg_root.attach(msg)
            msg = msg_root
            
        for f in ficheros:
            part = MIMEBase('application', 'octet-stream')
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