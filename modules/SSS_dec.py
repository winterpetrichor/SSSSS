from decimal import * #to avoid binary fraction rounding errors 
import os #to check for existing directory and files
import sys #to get size of bytearrays

#password encryption and decryption module
import enc_modules

#Shamir Secret Sharing  module
import SSS_modules

def dec_main(p1, savedir):

    path = savedir

    #empty variables for loops, etc. 
    shs = []
    filelist = []
    t_len = 0
    filcnt = 0
    sha = []
    pool = []
    ioerr=[]
    
    #parse files
    for fil in os.listdir(path):
        if fil.endswith(".bin"):
            filcnt += 1
            try:
                file = os.path.join(path, fil)
                filelist.append(file)
                with open(file, "rb") as f:
                    token = bytearray()
                    for a in range (sys.getsizeof(f)):
                        token+=f.read(1)
                        
                    shs.append(token)
                
            except IOError:
                ioerr.append(fil)

    #password = input('Enter password: ')
    password = p1

    #decrypt shares with password provided
    for ba in shs:
        try:
            dec = enc_modules.password_decrypt(ba, password).decode()
            passerr = 0
        except AttributeError:
            continue
        except:
            passerr = 1
        try:
            dec = dec.replace('(','')
            dec = dec.replace(')','')
            sha.append(dec)
            passerr = 0
        except:
            passerr = 1
            
    #get required length of decimal context for decrypting        
    for st in sha:
        tup = tuple(map(int, st.split(',')))
        pool.append(tup)
        if t_len < len(str(tup[-1])):
            t_len = len(str(tup[-1]))
        else:
            t_len = t_len

    #adjust length of decimal context
    try:
        getcontext().prec = t_len
    except:
        ioerr.append('getcontexterr')

    reconstr = ''
    #reconstruct secret from decrypted shares
    try:
        reconstr = SSS_modules.reconstruct_secret(pool)
        errno = 0
    except UnicodeDecodeError:
        errno = 1
        
    return(errno, reconstr, filcnt, ioerr, passerr)
