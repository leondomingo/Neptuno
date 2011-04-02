# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='Neptuno',
      version='2.0',
      author='León Domingo',
      author_email='leon.domingo@ender.es',
      url='www.ender.es',      
      packages=['neptuno',
                'neptuno.excepciones',  
                'neptuno.postgres'],
      install_requires=[
        'psycopg2',
        'SQLAlchemy==0.6.6',
        'lxml==2.2.7',
        'xlrd',
        'xlwt',
        'simplejson',
        'readline',
        'jinja2',
      ],
     )
