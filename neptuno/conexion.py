# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from const_datos_neptuno import CONF_HOST, CONF_DB, CONF_USER, CONF_PASSW
from neptuno.const_datos_neptuno import IMPLTYPE_FIREBIRD, IMPLTYPE_POSTGRESQL

class Conexion(object):
    
    def __init__(self, config, impl_type=IMPLTYPE_POSTGRESQL):
        """
        IN
          config {
                  'host':     <str>,
                  'db':       <str>,
                  'user':     <str>,
                  'password': <str>
                 }
                 
          impl_type <str> ('postgres', 'firebird')
        """
        
        # config
        self.config = config            
        
        # impl_type
        self.impl_type = impl_type            
            
        self.engine = create_engine(self.connectionstr(self.config),
                                    pool_size=1, pool_recycle=30)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def connectionstr(self, config):
        """
        Implementaciones actuales:
          postgres://postgres:5390post@localhost/tandem
          firebird://SYSDBA:masterkey@localhost/argos        
        """
        tipo = 'postgresql'
        if self.impl_type == IMPLTYPE_FIREBIRD:
            tipo = 'firebird'                     

        return '%s://%s:%s@%s/%s' % \
            (tipo,
             config[CONF_USER], config[CONF_PASSW], 
             config[CONF_HOST], config[CONF_DB])

    def __del__(self):        
        self.session.close()        
        self.engine.dispose()