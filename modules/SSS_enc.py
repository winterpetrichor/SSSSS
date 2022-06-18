import os #to check for existing directory and make one if it doesn't exist
import shutil #cleanup
import sys #to get size of bytearrays

#password encryption and decryption module
import enc_modules

#Shamir Secret Sharing  module
import SSS_modules
import SSS_dec_rand

#import GUI
import tkinter as tk
from tkinter import filedialog

prog = 0

def enc_main(mindec, maxdec, s1, p1, savedir, foldername, fileprefix):
    
    # sharing scheme
    t = mindec
    n = maxdec

    #secret
    m1 = s1

    #pad end of text with underscores (no reason for it to be underscores, could be anything),
    #but padding end of text to account for SSS encryption artefacts noted in testing(?)
    mlenadj = ((len(m1)//23)+1)*23 - (len(m1))
    m = m1 + '___end___' + '_' * mlenadj

    #password
    password = p1

    #encode secret as utf-8 bytes, then convert to integer for SSS processing
    mBytes = m.encode("utf-8")
    mInt = int.from_bytes(mBytes, byteorder="big")
    secret = mInt    

    # Phase I: Generation of shares
    shares = SSS_modules.generate_shares(n, t, secret)

    #create subfolder for secrets at selected location
    path = savedir
    
    if os.path.exists(path+'\\'+foldername) is False:
        try:
            os.makedirs(path+'\\'+foldername)
            patherr = 0
        except:
            patherr = 1

    else:
        patherr = 1

    #counters
    cnt = 0
    suc_cnt = 0
    fail_cnt = 0
    
    
    for sh in shares:
        sha = str(sh)
        
        #secret file names
        name = path + '/' + foldername + '/' + fileprefix + '_secret_' + str(cnt) +'.bin'
        
        #password encrypt shares
        enc = enc_modules.password_encrypt(sha.encode(), password) 
        with open(name, "wb") as binary_file:
            
            #write files
            binary_file.write(enc)
            
        #for next file name
        cnt = cnt+1 

        #read and verify file is written correctly
        with open(name, 'rb') as verif:
            token = bytearray()
            for a in range (sys.getsizeof(verif)):
                token+=verif.read(1)

            #verify file matches encrypted share data
            if token == enc: 
                #log file success
                suc_cnt = suc_cnt + 1
            else:
                #log encryption file error
                fail_cnt = fail_cnt + 1

    
    #automatic decryption testing and re-encoding if unicode error occurs
    try:
        ou2, ou3, prog = SSS_dec_rand.dec_rand(p1, path+'\\'+foldername, n, t)
        if ou3 == True:
            try:
                shutil.rmtree(path+'\\'+foldername)
            except OSError as e:
                #print("Error: %s : %s" % (dir_path, e.strerror))
                return
            try:
                while os.path.exists(path+'\\'+foldername) is True:
                    try:
                        shutil.rmtree(path+'\\'+foldername)
                    except OSError as e:
                        #print("Error: %s : %s" % (dir_path, e.strerror))
                        return
                os.makedirs(path+'\\'+foldername)
                patherr = 0
            except:
                patherr = 1
            enc_main(t, n, m1, password, path, foldername)
    except UnicodeDecodeError:
        
        shutil.rmtree(foldername)
        os.makedirs(path+'\\'+foldername)
        enc_main(t, n, m1, password, path, foldername)

    return(fail_cnt, suc_cnt, foldername, patherr, prog)
