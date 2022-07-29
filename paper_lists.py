#################################################################
#################################################################
# Read the lists of papers per journal per year.                #
#################################################################
#################################################################

import fitz
import pyautogui
import os
import time
import getpass
import platform
import distro

import pandas as pd

#################################################################
# Print the waiting time.                                       #
#################################################################

def print_wait(nsec):

    sec=nsec
    while (sec > 0):
        ostr='Waiting '+str(sec)+' seconds.'
        print(ostr)
        time.sleep(1)
        sec=sec-1

    return()

#################################################################
# Print the start message.                                      #
#################################################################

def start_message(Y1,Y2):

    print('Make sure to be logged on to the WoS search engine.')
    print('This is : https://www.webofscience.com/wos/woscc/basic-search')
    print('To be on the safe side, use google chrome.')
    print('Have two search lines, with the first for "Publication Titles".')
    print('The second should be "Publication Date".')
    print('\a\nIf this is the case, press <Enter>.')
    a=input()
    print('Make sure to active the browser window.')
    print_wait(5)

    return()

#################################################################
# Check if the required directories exist.                      #
#################################################################

def check_dirs(short):

    dirname='LISTS'
    if (os.path.exists(dirname) == False):
        syscall='mkdir '+dirname
        os.system(syscall)

    dirname='LISTS/'+short
    if (os.path.exists(dirname) == False):
        syscall='mkdir '+dirname
        os.system(syscall)

    return(dirname)

#################################################################
# Go to the publications for each year page.                    #
#################################################################

def go_to_year_results(J_names,ijo,iyear):

    dirname=check_dirs(J_names['Short'][ijo])
    pyautogui.hotkey('ctrl','f')
    time.sleep(1)
    pyautogui.typewrite('Publication Titles')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite('\b')
    time.sleep(1)
    search_str=J_names['Long'][ijo]
    search_str=search_str.replace('-',' ')
    search_str=search_str.replace('&','')
    pyautogui.typewrite(search_str)
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    for itab in range(0,6):
        pyautogui.press('tab')
        time.sleep(0.25)
    ostr=str(iyear)+'-01-01'
    pyautogui.typewrite(ostr)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    ostr=str(iyear)+'-12-31'
    pyautogui.typewrite(ostr)
    time.sleep(1)
    for itab in range(0,5):
        pyautogui.press('tab')
        time.sleep(0.25)
    pyautogui.press('enter')

    return()

#################################################################
# Print out the total duration.                                 #
#################################################################

def duration(starttime):

    ostr='\n\aFinal duration: '
    ostr=ostr+str("{:,}".format(round(time.time()-starttime,3)))
    ostr=ostr+' seconds.'
    print(ostr)

    return()

#################################################################
# Get the ubuntu version.                                       #
#################################################################

def release():

    os.system('lsb_release -a > t.txt')
    i_ptr=open('t.txt','r')
    pars=i_ptr.readline()
    pars=i_ptr.readline()
    pars=i_ptr.readline()
    par=str.split(pars)
    ubuntu=par[1].split('.')
    ubuntu_version=int(ubuntu[0])
    i_ptr.close()
    os.system('rm t.txt')

    return(ubuntu_version)

#################################################################
# Check which platform the code is working on.                  #
#################################################################

def get_platform():

    uname=getpass.getuser()
    ubuntu_version=release()
    pwd=os.getcwd()

    return(pwd,ubuntu_version,uname)

#################################################################
# Download the pdf with the citation information.               #
#################################################################

def download_citation_pdf(pwd,ubuntu_version):

    if (os.path.exists('citation_data.pdf') == True):
        os.system('rm citation_data.pdf')
    pyautogui.hotkey('ctrl','p')
    print_wait(10)
    pyautogui.press('enter')
    print_wait(4)
    if (ubuntu_version == 22):
        pyautogui.hotkey('alt','tab')
        time.sleep(1)
        pyautogui.hotkey('alt','tab')
        time.sleep(1)
    pyautogui.typewrite('\b')
    time.sleep(1)
    o_fn=pwd+'/'+'citation_data'
    time.sleep(1)
    pyautogui.typewrite(o_fn)
    time.sleep(1)
    pyautogui.press('enter')
    while (os.path.exists('citation_data.pdf') == False):
        print('Waiting for the pdf to download.')
        time.sleep(1)

    return()

#################################################################
# Extract the number of references from the pdf.                #
#################################################################

def get_num_references():

    pdf='citation_data.pdf'

    with fitz.open(pdf) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    ostr=''
    nline=0
    line=[]
    for i in range(0,len(text)):
        if (text[i] != '\n'):
            ostr=ostr+text[i]
        if (text[i] == '\n'):
            line.append(ostr)
            ostr=''
            nline=nline+1

    nref=-9999

    for iline in range(0,nline):
        words=str.split(line[iline])
        if (len(words) == 9):
            imatch=0
            if (nref < 0):
                if (words[1] == 'results'):
                    imatch=imatch+1
                if (words[2] == 'from'):
                    imatch=imatch+1
                if (words[3] == 'Web'):
                    imatch=imatch+1
                if (words[4] == 'of'):
                    imatch=imatch+1
                if (words[5] == 'Science'):
                    imatch=imatch+1
                if (words[6] == 'Core'):
                    imatch=imatch+1
                if (words[7] == 'Collection'):
                    imatch=imatch+1
                if (words[8] == 'for:'):
                    imatch=imatch+1
            if (imatch == 8):
                sref=str(words[0])
                sref=sref.replace(',','')
                nref=int(sref)

    os.system('rm citation_data.pdf')

    return(nref)

#################################################################
# Get the "Export Records to Excel" window.                     #
#################################################################

def get_save_window():

    pyautogui.hotkey('ctrl','f')
    time.sleep(1)
    pyautogui.typewrite('Add To Marked List')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    for idown in range(0,7):
        pyautogui.typewrite(['down'])
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)

    return()

#################################################################
# Save the excel file.                                          #
#################################################################

def save_file(i_ref_rep,nref,uname):

    pyautogui.hotkey('ctrl','f')
    time.sleep(1)
    pyautogui.typewrite('Export Records to Excel')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite(['down'])
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.typewrite('\b')
    time.sleep(1)
    ostr1=str(i_ref_rep*1000+1)
    pyautogui.typewrite(ostr1)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    nfin=(i_ref_rep+1)*1000
    if (nfin > nref):
        nfin=nref
    ostr2=str(nfin)
    pyautogui.typewrite('\b')
    time.sleep(1)
    pyautogui.typewrite(ostr2)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.typewrite(['down'])
    pyautogui.typewrite(['down'])
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    time.sleep(1)
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')
    o_fn='/home/'+uname+'/Downloads/savedrecs.xls'
    while (os.path.exists(o_fn) == False):
        print('Waiting for the download.')
        time.sleep(1)

    return()

#################################################################
# Save the papers file.                                         #
#################################################################

def save_papers(nref,uname,J_names,ijo,iyear):

    n_ref_rep=1+int(nref/1000)
    for i_ref_rep in range(0,n_ref_rep):
        get_save_window()
        save_file(i_ref_rep,nref,uname)
        syscall='\mv /home/'+uname+'/Downloads/savedrecs.xls LISTS/'
        syscall=syscall+J_names['Short'][ijo]+'/'+J_names['Short'][ijo]
        syscall=syscall+'_'+str(iyear)+'_'+str(i_ref_rep)+'.xls'
        os.system(syscall)

    return()

#################################################################
# Go to the next search page.                                   #
#################################################################

def go_to_next_search():

    pyautogui.hotkey('ctrl','f')
    time.sleep(1)
    pyautogui.typewrite('Saved Searches and Alerts')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.press('tab')
    time.sleep(1)
    pyautogui.press('enter')

    return()

#################################################################
# Process one specific journal.                                 #
#################################################################

def process_journal(J_names,ijo,pwd,ubuntu_version,uname,Y1,Y2):

    for iyear in range(Y1,Y2):
        ostr='Processing '+J_names['Long'][ijo]+' '+str(iyear)+'.'
        print(ostr)
        go_to_year_results(J_names,ijo,iyear)
        print_wait(10)
        download_citation_pdf(pwd,ubuntu_version)
        nref=get_num_references()
        if (nref > 0):
            save_papers(nref,uname,J_names,ijo,iyear)
        go_to_next_search()

    return()

#################################################################
#################################################################
# Start the main code.                                          #
#################################################################
#################################################################

def main():

    starttime=time.time()

    Y1=2000
    Y2=2022

    start_message(Y1,Y2)

    pwd,ubuntu_version,uname=get_platform()

    J_names=pd.read_csv('journals_ALL.csv')

    for ijo in range(0,J_names.shape[0]):
        process_journal(J_names,ijo,pwd,ubuntu_version,uname,Y1,Y2)

    duration(starttime)

main()
