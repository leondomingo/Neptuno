# -*- coding: utf-8 -*-

class Dict(dict):
    def __init__(self, **kw):
        for k, v in kw.iteritems():
            if isinstance(v, dict) or isinstance(v, Dict):
                self[k] = Dict(**v)
            
            else:
                self[k] = v
            
    def __getattr__(self, name):
        if self.has_key(name):
            return self[name]
        
    def __setattr__(self, name, value):
        self[name] = value
            
            
if __name__ == '__main__':
    
    d = Dict(uno=1, dos=2.2, tres=[])
    print d.uno
    print d.dos
    
    d.tres.append('leon')
    d.tres.append('domingo')
    print ' '.join(d.tres)
    
    # atributo que no estaba definido en el __init__
    d.hola = 'hola'
    print d.hola
    
    # en tres niveles
    d2 = Dict(uno=1, dos=dict(a=dict(a1=1, a2=2), b=2))
    
    print 'd2:', d2, type(d2)
    print d2.dos.a.a1
    print d2.dos.a.a2