#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Description: decode the position information of Dianping     
#  Author: Kalvin Ni                           
#  Date: Dec 12th, 2015                         
#  Version: 1         

#**********************************************#

  
def to_base36(value):  
    if not isinstance(value, int):  
        raise TypeError("expected int, got %s: %r" % (value.__class__.__name__, value))  
  
    if value == 0:  
        return "0"  
  
    if value < 0:  
        sign = "-"  
        value = -value  
    else:  
        sign = ""  
  
    result = []  
  
    while value:  
        value, mod = divmod(value, 36)  
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])  
  
    return sign + "".join(reversed(result))  
  
def decode(C):  
    digi = 16  
    add = 10  
    plus = 7  
    cha = 36  
    I = -1  
    H = 0  
    B = ''  
    J = len(C)  
    G = ord(C[-1])  
    C = C[:-1]  
    J -= 1  
      
    for E in range(J):  
        D = int(C[E], cha) - add  
        if D >= add:  
            D = D - plus  
        B += to_base36(D)  
        if D > H:  
            I = E  
            H = D  
  
    A = int(B[:I], digi)  
    F = int(B[I+1:], digi)  
    L = (A + F - int(G)) / 2  
    K = float(F - L) / 100000  
    L = float(L) / 100000  
    return {'lat': K, 'lng': L}  
  
if __name__ == '__main__':  
    print decode('IBGITBZUHGDVEM')  







    