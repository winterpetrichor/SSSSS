#this module was originally meant to spot test random combinations
#of secret files, but I decided to test all possible combinations
#to be sure

from decimal import * #to avoid binary fraction rounding errors 
import os #to check for existing directory and files
import sys #to get size of bytearrays

#Shamir Secret Sharing  decryption thread module
import SSS_decr_thread

#combination testing
from itertools import combinations

#testing progress
from math import comb

#multithreading
from threading import Thread

#for progressbar
import tkinter as tk
from tkinter import *
from tkinter import ttk

#progressbar window setup
progroot = Tk()
progroot.title("Decryption testing progress")
progroot.columnconfigure(0, weight=1)
progroot.rowconfigure(0, weight=1)
progroot.geometry("675x100")
progframe = ttk.Frame(progroot)
progframe.grid(column=0, row=0, sticky=(N, W, E, S))
proglab=tk.StringVar(progframe, value = '0.0%')
cyclestat=tk.StringVar(progframe, value = 'N/A')
progress = ttk.Progressbar(progframe, orient = HORIZONTAL, length = 500, mode = 'determinate')
progress.grid(column=1, row=1, sticky=EW, padx=5,pady=5)
proglabel = ttk.Label(progframe, textvariable=proglab).grid(column=2, row=1, sticky=W, padx=5, pady=5)
ttk.Label(progframe, text="Note: Decryption testing may take several cycles...").grid(column=0,columnspan=2,row=0,sticky=W,padx=5,pady=5)
ttk.Label(progframe, text="Cycle Progress:").grid(column=0,row=1,sticky=E,padx=5,pady=5)
ttk.Label(progframe, text="Last Cycle Results:").grid(column=0,row=2,sticky=E,padx=5,pady=5)
cyclestatus = ttk.Label(progframe, textvariable=cyclestat).grid(column=1, row=2, sticky=W, padx=5, pady=5)
progroot.withdraw()


def dec_rand(p1, savedir, n, t):
    #get total number of combinations for min shares and create threads and results lists
    total = comb(n, t)
    threads = [None] * total
    results = [None] * total

    #path
    path = savedir
    
    #empty variables for loops, etc. 
    shs = []
    shs1 = []
    filelist = []
    filcnt = 0
    combolist = []

    #parse files
    for fil in os.listdir(path):
        if fil.endswith(".bin"):
            filcnt += 1
            try:
                file = os.path.join(path, fil)
                filelist.append(file)
            except:
                return
            
    for i in combinations(filelist, t):
        combolist.append(i)
    
    for i in combolist:
        for j in i:
            try:
                with open(j, "rb") as f:
                    token = bytearray()
                    for a in range (sys.getsizeof(f)):
                        token+=f.read(1)
                shs1.append(token)
            except IOError:
                ioerr.append(fil)
        shs.append(shs1)
        shs1 = []

#multithreading for decryption testing
    def decmult(shs, i, p1, savedir, filcnt, total, results):
        #show progress window
        progroot.deiconify()

        #variables
        deccount = 0
        update_perc = 0
        prog = update_perc
        finthreads = []
        statres=''

        #start threads
        for i in shs:
            threads[deccount] = Thread(target=SSS_decr_thread.decr, args=(i, p1, savedir, filcnt, results, deccount))
            threads[deccount].start()
            deccount += 1
            #each iteration of threads starting
            for u in range(deccount):
                #check which started threads have finished
                if not threads[u].is_alive():
                    #and see if they succeeded or not
                    if results[u] == None:
                        failm = True
                        reconstr = results
                        #update progressbar window
                        failresultcount = results.count(None)
                        successresultcount = len(results)-failresultcount
                        statres = f'Successful decryption {successresultcount} times out of {failresultcount+successresultcount}'
                        cyclestat.set(str(statres))
                        return(results, failm, prog)
                    else:
                        if u not in finthreads:
                            finthreads.append(u)
                        #update progressbar window
                        prog = (len(finthreads)*1000//total)/10
                        progress['value']=prog
                        proglab.set(str(prog)+'%')
                        progroot.update()

        #get results
        for i in range(len(threads)):
            threads[i].join()

        #double check for failures
        if None in results:
            failm = True
        else:
            failm = False
            progroot.withdraw()
        reconstr = results[0]
        
        return(reconstr, failm, prog)

#execute threads
    reconstr, failm, prog = decmult(shs, i, p1, savedir, filcnt, total, results)

    return(reconstr, failm, prog)

    
