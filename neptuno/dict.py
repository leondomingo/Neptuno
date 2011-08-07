# -*- coding: utf-8 -*-

class Dict(dict):
    def __init__(self, **kw):
        for k, v in kw.iteritems():
            #print type(v)
            if isinstance(v, dict) or isinstance(v, Dict):
                self[k] = Dict(**v)
                
            elif isinstance(v, list):
                v2 = []
                for item in v:
                    #print type(item)
                    if isinstance(item, dict) or isinstance(item, Dict):
                        #print 'v =', v
                        v2.append(Dict(**item))
                        
                    else:
                        #print '*v=', v
                        v2.append(item)
                        
                self[k] = v2

            elif isinstance(v, tuple):
                v2 = None
                for item in v:
                    
                    if isinstance(v, dict) or isinstance(v, Dict):
                        if not v2:
                            v2 = (Dict(**item),)
                            
                        else:
                            v2 = v2 + (Dict(**item),)
                            
                    else:
                        if not v2:
                            v2 = (item,)
                            
                        else:
                            v2 = v2 + (item,)
                    
                self[k] = v2

            else:
                self[k] = v
            
    def __getattr__(self, name):
        if self.has_key(name):
            return self[name]
        
    def __setattr__(self, name, value):
        self[name] = value
            
            
if __name__ == '__main__':
    
    origen = {"cargos": [{"id": 1, "desc": "uno"}, {"id": 2, "desc": "dos"}],
              "tupla": ({"a": 1000}, {"a": 2000},)
              }
    
    destino = Dict(**origen)
    print destino.cargos
    print destino.cargos[0].id
    
    print destino.tupla
    print destino.tupla[0].a