# -*- coding: utf-8 -*-

from email import Encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re
import smtplib

def send_mail(from_, to_, subject, message, server, login, password, files=[], 
              html='', cc=[], bcc=[], reply_to=None, charset='utf-8', ssl=False):
    """
    IN
      from_          (<e-mail address>, <name>)
      to_            [(<e-mail address>, <name>), ...]
      subject        <str>
      message        <str>
      server         <str> (smtp.domain.com, smtp.domain.com:<port>)
      login          <str>
      password       <str>
      files          [<str>, ...] (optional)
                     [(<StringIO>, <str>), ...] (optional)
      html           <str>        (optional)
      cc             [(<e-mail address>, <name>), ...]
      bcc            [(<e-mail address>, <name>), ...]
      reply_to       <str> => None
      charset        <str> => utf-8
      ssl            <bool> => False
      
      For example,
        send_mail(('pperez@gmail.com', 'Pepe Pérez'),
                  ['malopez@gmail.com', 'María López'), (mlopez@yahoo.com, 'María')],
                  'Hello, world!', 'How you doing?\n\nPepe',
                  'smtp.gmail.com', 
                  'pperez@gmail.com', 'ilovemarialopez')
                     
    """
    
    msg = MIMEText(message)
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

    files_obj = []        
    if files:
        if not msg_root:
            msg_root = MIMEMultipart()
            msg_root.attach(msg)
            msg = msg_root
            
        for f in files:
            part = MIMEBase('application', 'octet-stream')
            if isinstance(f, (str, unicode,)):
                f_name = os.path.basename(f)
                
                f = open(f, 'rb')
                files_obj.append(f)
                
            else:
                # tuple (<file-like>, <file name>,)
                f, f_name = f
                f.seek(0)
                
            part.set_payload(f.read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % f_name)
            msg.attach(part)
            
    msg['Subject'] = Header(subject, charset)
    msg['From'] = '%s <%s>' % (from_[1], from_[0])
    
    nombres = ['%s <%s>' % (dst[1], dst[0]) for dst in to_]
    msg['To'] = ';'.join(nombres)
    msg['Cc'] = ';'.join(['%s <%s>' % (dst[1], dst[0]) for dst in cc])
    
    # reply-to
    if reply_to:
        msg.add_header('Reply-to', reply_to)
    
    # identify the port in given host (smtp.domain.com:123)
    m_server = re.search(r'^([\w\-\.]+)(:\d+)?', server)
    port = m_server.group(2)
    if port:
        port = dict(port=int(port.replace(':', '')))

    else:
        port = {}
        
    SMTP_ = smtplib.SMTP
    if ssl:
        smtplib.SMTP_SSL
        
    s = SMTP_(m_server.group(1), **port)
    try:
        s.set_debuglevel(False)
        
        # authenticate to the server
        s.ehlo()
        
        # STARTTLS?
        if s.has_extn('STARTTLS'):
            s.starttls()
            s.ehlo() # re-identify ourselves over TLS connection
            
        # login
        s.login(login, password)
        
        emails_dst_to = [dst[0] for dst in to_]
        emails_dst_cc = [dst[0] for dst in cc]
        emails_dst_bcc = [dst[0] for dst in bcc]
        
        emails_dst = emails_dst_to + emails_dst_cc + emails_dst_bcc 
        
        # send e-mail
        result = s.sendmail(from_[0], emails_dst, msg.as_string())
        
        # close files (if there's any)
        for f in files_obj:
            f.close()
        
        return result
    
    finally:
        s.quit()
        
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
        
