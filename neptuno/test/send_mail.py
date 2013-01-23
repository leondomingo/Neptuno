# -*- coding: utf-8 -*-

from neptuno.sendmail import send_mail
import datetime as dt

if __name__ == '__main__':
    send_mail(('facturas@ihmadrid.info', 'IH Madrid'), 
              [('leon.domingo@ender.es', 'León Domingo')],
              'prueba-%s' % dt.datetime.now(), 'mensaje', 
              'smtpout.europe.secureserver.net',
              'facturas@ihmadrid.info', 'IHmad2013',
              ssl=True) #, reply_to_='empresas@ihmadrid.com')
