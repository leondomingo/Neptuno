# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='Neptuno',
      version='1.0',
      author='León Domingo',
      author_email='leon.domingo@ender.es',
      url='www.ender.es',      
      packages=['libpy',
                'libpy.excepciones',  
                'libpy.firebird', 
                'libpy.firebird.exc',
                'libpy.postgres'],
      install_requires=[
        'xlrd',
        'xlwt',
        'simplejson'],
     )