# -*- coding: utf-8 -*-

from neptuno.dict import Dict

if __name__ == '__main__':
    
    d = Dict(**dict(uno=[dict(a=1, b=2), 
                         dict(c=3, d=4)],
                    dos=Dict(m=1, n=2)))
    print d
    print d.uno[0].a
    d.dos.a2 = 3
    d.uno[0].c = 333
    d.uno.append(Dict(x=100, y=200))
    print d