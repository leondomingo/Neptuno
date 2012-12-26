# -*- coding: utf-8 -*-

from neptuno.sendmail import send_mail
import datetime as dt

if __name__ == '__main__':
    send_mail(('administracion@centrolinden.com', 'administracion@centrolinden.com'), 
              [('leon.domingo@ender.es', 'León Domingo')],
              'prueba-%s' % dt.datetime.now(), 'mensaje', 
              'mail.webhostingpad.com',
              #'mail.centrolinden.com',
              'administracion@centrolinden.com', 'lindenatenea',
              #cc=[('leon.domingo@ender.es', 'León Domingo')],
              ssl=True)
