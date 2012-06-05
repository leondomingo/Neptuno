# -*- coding: utf-8 -*-

import sys
from neptuno.dataset import DataSet

if __name__ == '__main__':
    
    print sys.executable
    
    ds = DataSet(['uno', 'dos', 'tres'])
    print(ds)
    
    ds.append([u'león', 2, 3])
    print(ds)
    
    ds.append_col(('cuatro', u'Cuatrö', 'int'))
    print type(str(ds).decode('utf-8'))
    
    ds[0]['cuatro'] = 4
    print ds