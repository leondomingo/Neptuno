# -*- coding: utf-8 -*-

import random
import hashlib
import unittest

class CryptoUtils(object):
    """Clase contenedora para funciones de cifrado."""
    
    def cadena_aleatoria(self, length):
        """Genera una cadena aleatoria de longitud 'length' """
        alpha = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        randlist = [random.choice(chars) for chars in [alpha]*length]
        return ''.join(randlist)

class SaltedHash():
    """Generador de un sistema de login basado en el método Salted Hash"""
    __salt = ''
    __hash = ''
    long_salt = 8
    
    def __init__(self, password, salt=''):
        """Método inicializador de la clase SaltedHash"""
        self.__m = hashlib.md5()
        self.util = CryptoUtils()
        
        if salt == '':
            salt = self.util.cadena_aleatoria(self.long_salt)

        self.__salt = salt
        
        # Generamos el valor del salted hash
        self.__hash = self.reHash(password)
    
    def getHash(self):
        return self.__hash

    def getSalt(self):
        return self.__salt
    
    def reHash(self, newpassword):
        """Genera el hash"""        
        
        # En principio hashlib.md5 no dispone de función clear por ello lo vuelvo a crear
        self.__m = hashlib.md5()
        self.__m.update(newpassword + self.__salt)        
        return self.__m.hexdigest()
  
class TestCryptoUtils(unittest.TestCase):
    """Proporciona una serie de testunits sobre las clases de CryptoUtils"""
        
    def testSaltedHash(self):
        """Test SaltedHash"""
        psw_prueba = 'password de prueba'
        salt_prueba = 'cadena salt de prueba'
        
        sh = SaltedHash(psw_prueba, salt_prueba)
        
        # Test 1 => Comprueba el observador sobre la cadena salt
        self.failUnlessEqual(sh.getSalt(), salt_prueba)

        # Test 2 => Comprueba que se genera correctamente el salted hash
        cadena_real = psw_prueba + sh.getSalt()
        m = hashlib.md5()
        m.update(cadena_real)
        hash_real = m.hexdigest()
        self.assertEqual(sh.getHash(), hash_real)
        
        # Test 3 => Comprueba si el Hash que se genera coincide con uno predefinido
        # para 'password de prueba'+'cadena salt de prueba' es a8f8ddb6254619b085090c6b8b9c48f3
        self.failUnlessEqual(sh.getHash(), 'a8f8ddb6254619b085090c6b8b9c48f3')

    def testCadenaAleatoria(self):
        """Test CryptoUtils.CadenaAleatoria"""
        util = CryptoUtils()
        cadena = util.cadena_aleatoria(10)
        self.failUnless(len(cadena) == 10)
        self.assertEqual(len(cadena), 10)    