# -*- coding: utf-8 -*-

from neptuno.enviaremail import enviar_email
import sys
import datetime as dt

if __name__ == '__main__':
    print sys.executable
    enviar_email(('leon.domingo@ender.es', 'León Domingo'), [], 
                 'prueba-%s' % dt.datetime.now(), 'mensaje', 'smtp.gmail.com', 'leon.domingo@ender.es', 'nitelite',
                 cc=[('eledeweb@gmail.com', 'León Domingo')],
                 bcc=[('tengounplanb@gmail.com', 'León Domingo')], charset='utf-8')