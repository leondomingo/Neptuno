# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='Neptuno2',
      version='1.0.3',
      author='León Domingo',
      author_email='leon.domingo@ender.es',
      description=('A little set of utilities that Ender has been using in their web projects'),
      #license=???,
      keywords='neptuno ender web',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
      ],
      url='www.ender.es',      
      packages=['neptuno',
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
