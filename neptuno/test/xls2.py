# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader
from neptuno.xlsreport import XLSReport

if __name__ == '__main__':
    pl = PackageLoader('neptuno', 'templates')
    env = Environment(loader=pl)
    template = env.get_template('test_image.xml')
    
    xr = XLSReport(template)
    xr.create({}, filename='/home/leon/test_image.xls')