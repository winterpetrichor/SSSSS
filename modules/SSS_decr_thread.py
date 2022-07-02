from decimal import * #to avoid binary fraction rounding errors 
import os #to check for existing directory and files
import sys #to get size of bytearrays

#password encryption and decryption module
import enc_modules

#Shamir Secret Sharing  module
import SSS_modules

#combination testing
from itertools import combinations

#testing progress
from math import comb

def decr(shs, p1, savedir, filcnt, results, deccount):
    #variables
    password = p1
    t_len = 0
    sha = []
    pool = []
    ioerr = []
    
    #decrypt shares with password provided
    for ba in shs:
        try:
            dec = enc_modules.password_decrypt(ba, password).decode()
        except AttributeError:
            continue
        try:
            dec = dec.replace('(','')
            dec = dec.replace(')','')
            sha.append(dec)
        except:
            return
            
    #get required length of decimal context for decrypting        
    for st in sha:
        tup = tuple(map(int, st.split(',')))
        pool.append(tup)
        if t_len < len(str(tup[-1])):
            t_len = len(str(tup[-1]))
        else:
            t_len = t_len

    #adjust length of decimal context
    getcontext().prec = t_len

    reconstr = ''
    #reconstruct secret from decrypted shares
    try:
        reconstr = SSS_modules.reconstruct_secret(pool)
        fail = False
        results[deccount]=reconstr
        return(reconstr, fail)
    except:
        reconstr = 'decryption failed'
        fail = True
        return(reconstr, fail)


