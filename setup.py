# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='Neptuno2',
      version='1.0.61',
      author=u'León Domingo',
      author_email='leon.domingo@ender.es',
      description=('A little set of utilities that Ender has been using in their web projects'),
      #license=???,
      keywords='neptuno ender web',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
      ],
      url='http://www.ender.es',      
      packages=['neptuno',
                'neptuno.postgres',
                'neptuno.templates',
      ],
      package_data={
            'neptuno': ['default/*.*', 
                        'default/update/*.*',
                        'default/update/TODO',
                        'default/update/new-issue',
                        'default/update/ejemplo/*.*',                        
                        ],
            'neptuno.templates': ['*.xml'],
      },
      install_requires=[
        'psycopg2',
        'SQLAlchemy==0.6.8',
        'lxml',
        'xlrd',
        'xlwt',
        'simplejson',
        'jinja2',
      ],
     )
