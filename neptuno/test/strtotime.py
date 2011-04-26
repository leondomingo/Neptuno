# -*- coding: utf-8 -*-

import neptuno.util as util

if __name__ == '__main__':
    
    h1 = util.strtotime('10:30')
    print h1
    
    h2 = util.strtotime('11:12:13')
    print h2
    
    # 9:5 == 09:05
    h3 = util.strtotime('9:5')
    print h3
    