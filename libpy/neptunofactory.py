# -*- coding: utf-8 -*-

from libpy.const_datos_neptuno import IMPLTYPE_POSTGRESQL, IMPLTYPE_POSTGRESQL2, \
    IMPLTYPE_FIREBIRD

IMPLEMENTATIONS = \
{
 IMPLTYPE_POSTGRESQL:
 {
  'modulo_base': 'libpy.postgres',
  'clase_usuarios': 'Usuarios'
 },
 IMPLTYPE_POSTGRESQL2:
 {
  'modulo_base': 'libpy.postgres2',
  'clase_usuarios': 'Usuarios'
 },
 IMPLTYPE_FIREBIRD:
 {
  'modulo_base': 'libpy.firebird',
  'clase_usuarios': 'UsuariosWeb'
 }
}

def get_base_module(tipo):
    modulo = IMPLEMENTATIONS[tipo]['modulo_base']
    return modulo

def load_module(tipo, modulo, nombre):
    path_modulo = '%s.%s' % (get_base_module(tipo), modulo)
    
    if isinstance(nombre, str):
        nombre = [nombre]
        
    return __import__(path_modulo, globals(), locals(), nombre, -1)

def get_claseusuarios(tipo):
    uc = __import__('nucleo.unidadescompartidas', globals(), locals(), -1)
    return getattr(uc, IMPLEMENTATIONS[tipo]['clase_usuarios'])
