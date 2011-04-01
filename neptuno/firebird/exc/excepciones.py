# -*- coding: utf-8 -*-

class ENoExisteRegistro(Exception):
    def __init__(self, cod_objeto):
        Exception.__init(self)
        self.cod_objeto = cod_objeto
        
    def __str__(self):
        return 'No existe el registro %d' % self.cod_objeto
    
class ENoExisteConsulta(Exception):
    def __init__(self, cod_consulta):
        Exception.__init(self)
        self.cod_consulta = cod_consulta
        
    def __str__(self):
        return 'No existe la consulta %d' % self.cod_consulta
    