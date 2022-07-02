#gui elements
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from functools import partial #to allow passing parameters to functions in button commands

import os #filepaths
import sys #exit

#encryption & decryption modules
sys.path.insert(0,'./modules')
import SSS_enc
import SSS_dec

#for folder name
from datetime import datetime


intro_warn_str = ('PLEASE READ THE FOLLOWING CAREFULLY TO UNDERSTAND THE \
APPLICATION AND ITS LIMITATIONS.\n\n\
The intent of this code is to use 1) a password, and 2) programatically \
generated encryption key, to encrypt the seed phrase of a digital wallet so \
that its parts can be distributed in different, varying digital locations \
(e.g. multiple cloud storage services) to mitigate against the risk of losing \
access to physical copies of SSS shares or otherwise trying to secure the \
entire (complete or unencrypted) seed phrase in a cloud service, which \
has inherent risk.\n\n\
You will need your secret (seed phrase or other text you wish to obfuscate), \
and a password, (ideally a \
strong one, stored in a password manager that is not linked to your shares). \
This password will be used to symmetrically encrypt your data with \
Fernet encryption provided by the cryptography library.\n\n\
[ https://pypi.org/project/cryptography/ ]\n\n\
The software is intended to be used to encrypt and then split your secret \
in a manner that would allow you to use X number of Y total shares to \
reconstruct your secret. You may set X = Y when using if you would prefer to \
have a system where all shares are required before decryption. \n\n\
This software is provided "as-is", using this software means that you agree \
that the developer(s) cannot be held liable for any undesirable outcomes that \
can be traced back to your use of this software.\n\n\
YOU and ONLY YOU are responsible for the strength of your password, \
the accuracy of the secrets and passwords entered, and the security of your \
share files generated. I do not claim that is foolproof or unhackable, \
but it is designed to be a reasonably secure method, if implemented \
correctly, and with a bit of luck.\n\n\
I thereby wish you good luck!\n\n\n\
ICYMI, PLEASE READ THE ABOVE CAREFULLY TO UNDERSTAND THE APPLICATION \
AND ITS LIMITATIONS\n\n\n\
By clicking "Ok" below, you accept all responsibility for any outcomes of \
using this software, otherwise, please click "Cancel" to exit the software.')

encwarnstr = \
           'Please store your secret files safely and in different, \
relatively secure digital locations such as different cloud services that \
use at least 2FA to allow access.\n\n\
Please also note that data degradation on physical hardware \
is real, and consider keeping multiple copies (still separately) or also \
using another backup method for your secret or seed phrase, such as \
mnemonics, paper steel, etc. This method is only meant to provide you with \
easier, more reliable alternative access to your secret compared to \
finding your physical records or collecting digital\physical shares from \
other individuals or locations.'

def introwindow():
    root = Tk()
    root.withdraw()
    return messagebox.askokcancel("SSSSS Intro", intro_warn_str)

#ENCRYPT SCREEN
def encryptwindow():
    #main window setup
    root = Tk()
    root.title("SSSSS (Shamir's Secret Sharing Seed Splitter) - Encryption Screen")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    #share splitting entry
    ttk.Label(mainframe, text="").grid(column=0, row=0, sticky=E, padx=5, pady=5)
    minlab = ttk.Label(mainframe, text="Minimum shares for decryption: ").grid(column=1, row=1, sticky=E, padx = 5, pady = 5)
    t = IntVar(root)
    t_entry = ttk.Entry(mainframe, width=4, textvariable=t)
    t_entry.grid(column=2, row=1, sticky=(W))
    
    ttk.Label(mainframe, text="Total number of shares: ").grid(column=3, row=1, sticky=E, padx = 5, pady = 5)
    n = IntVar(root)
    n_entry = ttk.Entry(mainframe, width=4, textvariable=n)
    n_entry.grid(column=4, row=1, sticky=(W))

    #button functions for show/hide masking
    def tp1():
        if s1_entry.cget('show') == '':
            s1_entry.config(show='*')
        else:
            s1_entry.config(show='')

    def tp2():
        if s2_entry.cget('show') == '':
            s2_entry.config(show='*')
        else:
            s2_entry.config(show='')

    def tp3():
        if p1_entry.cget('show') == '':
            p1_entry.config(show='*')
        else:
            p1_entry.config(show='')

    def tp4():
        if p2_entry.cget('show') == '':
            p2_entry.config(show='*')
        else:
            p2_entry.config(show='')

    umklab = ttk.Label(mainframe, text="Masking").grid(column=8, columnspan=3, row=1, padx = 0, pady = 5, sticky=E)
    umkbtntxt = '*'
    ttk.Button(mainframe, text=umkbtntxt, width = 3, command = tp1).grid(column=9, row=2, padx = 0, pady = 5)
    ttk.Button(mainframe, text=umkbtntxt, width = 3, command = tp2).grid(column=9, row=3, padx = 0, pady = 5)
    ttk.Button(mainframe, text=umkbtntxt, width = 3, command = tp3).grid(column=9, row=4, padx = 0, pady = 5)
    ttk.Button(mainframe, text=umkbtntxt, width = 3, command = tp4).grid(column=9, row=5, padx = 0, pady = 5)

    #browse button    
    pathname = os.getcwd()
    def browsebutton(pathname):
        filename = filedialog.askdirectory(title="Choose the location to save the encrypted secret files", initialdir=pathname)
        pathname = filename.replace("/", "\\")
        browse.set(pathname)

    ttk.Button(mainframe, text="Browse", command=partial(browsebutton,pathname)).grid(column=8, columnspan=2, ipadx=8, row=6, padx = 0, pady = 5, sticky=E)
    
    #entry labels
    ttk.Label(mainframe, text="Share Splitting: ").grid(column=0, row=1, sticky=E, padx = 5, pady = 5)
    ttk.Label(mainframe, text="Secret: ").grid(column=0, row=2, sticky=E, padx = 5, pady = 5)
    ttk.Label(mainframe, text="Confirm secret: ").grid(column=0, row=3, sticky=E, padx = 5, pady = 5)
    ttk.Label(mainframe, text="Password: ").grid(column=0, row=4, sticky=E, padx = 5, pady = 5)
    ttk.Label(mainframe, text="Confirm password: ").grid(column=0, row=5, sticky=E, padx = 5, pady = 5)
    
    #entry for passwords and secrets, masked with *
    s1 = StringVar(root, value = '')
    s1_entry = tk.Entry(mainframe, width = 105, show = '*', textvariable = s1)
    s1_entry.grid(column=1, row=2, columnspan=8, sticky=(W), padx = 5, pady = 5)
    s2 = StringVar(root, value = '')
    s2_entry = tk.Entry(mainframe, width = 105, show = '*', textvariable = s2)
    s2_entry.grid(column=1, row=3, columnspan=8, sticky=(W), padx = 5, pady = 5)
    p1 = StringVar(root, value = '')
    p1_entry = tk.Entry(mainframe, width = 105, show = '*', textvariable = p1)
    p1_entry.grid(column=1, row=4, columnspan=8, sticky=(W), padx = 5, pady = 5)
    p2 = StringVar(root, value = '')
    p2_entry = tk.Entry(mainframe, width = 105, show = '*', textvariable = p2)
    p2_entry.grid(column=1, row=5, columnspan=8, sticky=(W), padx = 5, pady = 5)
    
    #browse label and entry
    ttk.Label(mainframe, text="  Save location for secret files: ").grid(column=0, row=6, sticky=E, padx = 5, pady = 5)
    ttk.Label(mainframe, text="Note: A new subfolder will be created at \
the specified location to contain secret files.").grid(column=1, columnspan=9, row=8, sticky=W, padx = 5, pady = 0)
    
    browse = StringVar(root, value = pathname)
    browse_entry = tk.Entry(mainframe, width = 92, textvariable = browse)
    browse_entry.grid(column=1, row=6, columnspan=6, sticky=(W), padx = 5, pady = 5)

    ttk.Label(mainframe, text="Prefix for secret filenames: ").grid(column=0, row=7, sticky=E, padx = 5, pady = 5)
    prefix = StringVar(root, value = "")
    prefix_entry = tk.Entry(mainframe, width = 110, textvariable = prefix)
    prefix_entry.grid(column=1, row=7, columnspan=9, sticky=(W), padx = 5, pady = 5)

    ttk.Label(mainframe, text="").grid(column=0, row=9, sticky=E, padx = 5, pady = 0)    

    #retrieve user entered data
    def encryptbutton():
        mindec = t.get()
        maxdec = n.get()
        s1 = s1_entry.get()
        s2 = s2_entry.get()
        p1 = p1_entry.get()
        p2 = p2_entry.get()
        savedir = browse_entry.get()
        now = datetime.now()
        date_time = str(now.strftime("%Y-%m-%d-%H-%M-%S"))
        foldername = 'encrypted_secret_files_' + date_time
        fileprefix = prefix_entry.get()
        
    #validate retrieved data
        if mindec > maxdec or mindec == 0 or maxdec == 0:
            tk.messagebox.showerror(title='Share quantity error', message='The minimum number of shares \
for decrypting cannot be greater than the total number of shares. These quantities also cannot be 0.')

        elif s1 != s2 or s1 == '':
            tk.messagebox.showerror(title='Secret verification error', message='Secrets do not match, or secrets are blank, \
please try again.')
            
        elif p1 != p2 or p1 == '':
            tk.messagebox.showerror(title='Password verification error', message='Passwords do not match, or passwords are blank, \
please try again.')

        elif os.path.exists(savedir) is False:
            tk.messagebox.showerror(title='Secret save directory error', message='There was a problem finding \
the specified directory, please consider selecting another directory and try again.')

    #if entered data is valid, proceed to encryption step
        else:
            tk.messagebox.showinfo(title='Notice', message=('After encryption, decryption testing will test \
all possible combinations of the MINIMUM number of shares, this may take several cycles and re-encryption to help ensure \
successful decryption later on, please be patient.\n\n\
Note that this testing only ensures that all combinations of the MINIMUM number of shares will result in successful decryption.\
This testing does NOT ensure that using MORE than the minimum will result in successful decryption.\
Click "Ok" to continue.'))
            fail_cnt, suc_cnt, foldername, patherr, prog = SSS_enc.enc_main(mindec, maxdec, s1, p1, savedir, foldername, fileprefix)
            suc_cnt1=str(suc_cnt)
            fail_cnt1=str(fail_cnt)
            if patherr == 1:
                tk.messagebox.showerror(title='Folder error', message='There was a problem finding \
or creating the specified directory, please consider selecting another directory and try again.')
            else:
                if fail_cnt == 0:
                    tk.messagebox.showinfo(title='Encryption success!', message=f'All files written and \
and successfully verified!\n\n\
{suc_cnt1} file(s) written and successfully verified, {fail_cnt1} file(s) failed.\n\n\
Files were written to: {savedir}\{foldername} \n\n\
Decryption of all combinations of the minimum number of secret files \
revealed that the secret integrity was preserved. \n\n\
PLEASE DO YOUR OWN TEST DECRYPTION OF THE MINIMUM NUMBER OF RANDOMLY SELECTED SECRET FILES GENERATED, TO BE SURE.')
                    tk.messagebox.showinfo(title='Encryption success!', message=(encwarnstr + '\n\n\
REMINDER: PLEASE DO YOUR OWN TEST DECRYPTION OF THE MINIMUM NUMBER OF RANDOMLY SELECTED SECRET FILES GENERATED, TO BE SURE.'))
                else:
                    enc_err_message = f'Some encryption or file writing errors seem to have occured, please try \
again.\n\n{suc_cnt1} files written and successfully verified, {fail_cnt1} file(s) failed.'
                    tk.messagebox.showerror(title='Encryption error', message=enc_err_message)
            
        return

    #main window buttons
    ttk.Button(mainframe, text="Review intro", command=introbutton).grid(column=1, row=10, padx = 5, pady = 5)
    ttk.Button(mainframe, text="Exit", command=exitbutton).grid(column=2, row=10, padx = 5, pady = 5)
    ttk.Button(mainframe, text="Decrypt", command=partial(decryptbutton, root)).grid(column=3, row=10, padx = 5, pady = 5)
    ttk.Button(mainframe, text="Encrypt", command=encryptbutton).grid(column=4, row=10, padx = 5, pady = 5)


    def on_closing():
        root.destroy()
        sys.exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind("<Return>", encryptbutton)
    root.resizable(False,False)
    root.mainloop()

#DECRYPT SCREEN
def decryptwindow():

    #main window setup
    root = Tk()
    root.title("SSSSS (Shamir's Secret Sharing Seed Splitter) - Decryption Screen")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    #button functions for show/hide masking
    def tp3():
        if p1_entry.cget('show') == '':
            p1_entry.config(show='*')
        else:
            p1_entry.config(show='')

    def tp4():
        if p2_entry.cget('show') == '':
            p2_entry.config(show='*')
        else:
            p2_entry.config(show='')

    umklab = ttk.Label(mainframe, text="").grid(column=8, columnspan=3, row=1, padx = 0, pady = 5, sticky=E)
    umkbtntxt = '*'
    ttk.Button(mainframe, text=umkbtntxt, width = 3, command = tp3).grid(column=9, row=3, padx = 0, pady = 5)
    ttk.Button(mainframe, text=umkbtntxt, width = 3, command = tp4).grid(column=9, row=4, padx = 0, pady = 5)

    #browse button
    pathname = os.getcwd()
    def browsebutton(pathname):
        filename = filedialog.askdirectory(title="Choose the location where you have placed the secret files for decryption", initialdir = pathname )
        pathname = filename.replace("/", "\\")
        browse.set(pathname)

    ttk.Button(mainframe, text="Browse", command=partial(browsebutton,pathname)).grid(column=8, columnspan=2, ipadx=8, row=2, padx = 0, pady = 5, sticky=E)

    #password entry and labels
    ttk.Label(mainframe, text="Password: ").grid(column=0, row=3, sticky=E, padx = 5, pady = 5)
    ttk.Label(mainframe, text="Confirm password: ").grid(column=0, row=4, sticky=E, padx = 5, pady = 5)
    
    p1 = StringVar(root, value = '')
    p1_entry = tk.Entry(mainframe, width = 105, show = '*', textvariable = p1)
    p1_entry.grid(column=1, row=3, columnspan=8, sticky=(W), padx = 5, pady = 5)
    p2 = StringVar(root, value = '')
    p2_entry = tk.Entry(mainframe, width = 105, show = '*', textvariable = p2)
    p2_entry.grid(column=1, row=4, columnspan=8, sticky=(W), padx = 5, pady = 5)

    #browse label and entry
    ttk.Label(mainframe, text="  Folder containing ONLY secret_##.bin files: ").grid(column=0, row=2, sticky=E, padx = 5, pady = 5)
    browse = StringVar(root, value = '')
    browse_entry = tk.Entry(mainframe, width = 92, textvariable = browse)
    browse_entry.grid(column=1, row=2, columnspan=6, sticky=(W), padx = 5, pady = 5)

    #button functions
    def encryptbutton2(root):
        root.destroy()
        encryptwindow()

    def decryptbutton2():
    #retrieve user entered data
        tk.messagebox.showwarning(title='Notice!', message='Please ensure that the MINIMUM number of \
required files are in the folder. \n\n More MAY work, but during encryption, ONLY combinations of the \
MINIMUM number were tested. Using MORE than the MINIMUM has been known to sometimes fail.\n\n\
You may go to the folder while this notice is up and alter the files, then click "Ok" to continue.')
        p1 = p1_entry.get()
        p2 = p2_entry.get()
        savedir = browse_entry.get()

    #validate user entered data
        if p1 != p2:
            tk.messagebox.showerror(title='Password verification error', message='Passwords do not match, \
please try again.')

        elif os.path.exists(savedir) is False:
            tk.messagebox.showerror(title='Secret directory error', message='There was a problem finding \
the specified directory, please consider selecting another directory and try again.')
    #if data is valid, proceed to decryption step
        else:
            errno, reconstr, filcnt, ioerr, passerr = SSS_dec.dec_main(p1, savedir)
            if passerr == 1:
                tk.messagebox.showerror(title='Decryption error', message='Password appears to be incorrect.')
            else:
                if errno == 1:
                    tk.messagebox.showerror(title='Decryption error', message=f'ERROR!\n\
An unspecified error occured when attempting to decrypt {filcnt} files in {savedir}\n\n\
Some possible scenarios:\n\
- Not enough secret files based on encryption strategy.\n\
- Extraneous *.bin files in specified folder.\n\
- File corruption.\n')
                elif ioerr != []:
                    for i in ioerr:
                        ioerr2 = '\n'.join(ioerr)
                        ioerr3 = str(ioerr2)
                    tk.messagebox.showwarning(title='Error!', message=f'An unspecified \
IO error while decrypting files  from {savedir}. The affected files are:\n\
{ioerr3}\n\n\Please try other secret files if you have them, move files \
to another location, or restart and try again.')
                elif filcnt == 0:
                    tk.messagebox.showerror(title='Error!', message='No *.bin files detected in the specified folder')
                elif errno == 0:
                    tk.messagebox.showwarning(title='Success!', message=f'Secret decrypted!\n\n\
{filcnt} files decrypted from {savedir}.\n\n\
Decrypted secret is:\n\n\
{reconstr}')     
                else:
                    tk.messagebox.showerror(title='Error!', message='An unknown error has occured. Please check \
selected folder for your *.bin files, ensure the correct files are there, check your password, and try again.')
        return

    #main window buttons
    ttk.Button(mainframe, text="Review intro", command=introbutton).grid(column=2, row=8, padx = 5, pady = 5)
    ttk.Button(mainframe, text="Exit", command=exitbutton).grid(column=3, row=8, padx = 5, pady = 5)
    ttk.Button(mainframe, text="Decrypt", command=decryptbutton2).grid(column=5, row=8, padx = 5, pady = 5)
    ttk.Button(mainframe, text="Encrypt", command=partial(encryptbutton2,root)).grid(column=4, row=8, padx = 5, pady = 5)

    #some window management
    def on_closing():
        root.destroy()
        sys.exit(0)
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.bind("<Return>", decryptbutton2)
    root.resizable(False,False)
    root.mainloop()

    
#other button functions
def decryptbutton(root):
    root.destroy()
    decryptwindow()
    return

def introbutton():
    if introwindow() is True:
        return
    else:
        sys.exit(0)

def exitbutton():
    sys.exit(0)

#intro exit
if introwindow() is True:
    encryptwindow()
else:
    sys.exit(0)

