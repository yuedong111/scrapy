# -*- coding: UTF-8 -*-

import string

def stzy(st):

    if (st == None):
        return ''

    pos = -2
    while ( True == True):
        pos = st.find('"', pos+2, len(st))
        if (pos == -1):
            break
        else:
            stmp = st[:pos] + '\\' + st[pos:]
            st = stmp

    return st
