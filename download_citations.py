#################################################################
#################################################################
# Download the journal list year by year.                       #
# Start chrome using the command                                #
# /opt/google/chrome/chrome -remote-debugging-port=9014 --user-data-dir="/home/vpauwels/Selenium_Dump" #
#################################################################
#################################################################

import time
import getpass
import os
import pandas as pd
import sys
import math
import fitz

import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date

#################################################################
# Extract the useful information from the pdf.                  #
#################################################################

def extract_ncit(ubuntu_version):

    pwd=os.getcwd()
    fn=pwd+'/citations.pdf'
    if (os.path.exists(fn) == True):
        syscall='\\rm '+fn
        os.system(syscall)

    pref=pwd+'/citations'

    pyautogui.hotkey('ctrl','p')
    print_wait(5)
    pyautogui.press('enter')
    print_wait(2)
    if (ubuntu_version >= 21):
        pyautogui.hotkey('alt','tab')
        time.sleep(1)
        pyautogui.hotkey('alt','tab')
        time.sleep(1)
    pyautogui.typewrite('\b')
    time.sleep(1)
    pyautogui.typewrite(pref)
    time.sleep(1)
    pyautogui.typewrite('\n')
    time.sleep(1)

    ncit=0

    with fitz.open(fn) as doc:
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

    for i in range(0,nline):
        if (len(line[i]) > 0):
            words=line[i].split(' ')
            if (len(words) == 3):
                if ( (words[1] == 'results') and (words[2] == 'cited:') ):
                    ncit_s=words[0].replace(',','')
                    ncit=int(ncit_s)

    syscall='\\rm '+fn
    os.system(syscall)

    return(ncit)

#################################################################
# Check if a variable is nan.                                   #
#################################################################

def isNaN(var):

    return (var != var)

#################################################################
# Print the start message.                                      #
#################################################################

def start_msg(URL):

    print("\a")
    print("==============================================")
    print("| Downloading the references for each paper. |")
    print("==============================================")
    print("\n\n")

    uname=getpass.getuser()

    print("Start chrome using the command")
    cmd='/opt/google/chrome/chrome -remote-debugging-port=9014 --user-data-dir="/home/'+uname+'/Selenium_Dump"'
    print(cmd)
    print("\aWhen this is done, press <Enter>.")
    a=input()
    print("Make sure to activate the browser window.")
    print_wait(5)

    return(uname)

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
# Print out the total duration.                                 #
#################################################################

def duration(starttime):

    ostr='\n\aFinal duration: '
    ostr=ostr+str("{:,}".format(round(time.time()-starttime,3)))
    ostr=ostr+' seconds.'
    print(ostr)

    return()

#################################################################
# Print the journal and the year.                               #
#################################################################

def print_j(J_names,ijo,iy):

    ostr='Processing '+J_names['Short'][ijo]+' '+str(iy)+'.'
    print(ostr)

    return()

#################################################################
# Prepare the input file name.                                  #
#################################################################

def prep_fn(J_names,ijo,iy,irep):

    i_fn='LISTS/'+J_names['Short'][ijo]+'/'+J_names['Short'][ijo]
    i_fn=i_fn+'_'+str(iy)+'_'+str(irep)+'.xls'

    return(i_fn)

#################################################################
# Check if the required directories exist.                      #
#################################################################

def check_directory(Short,uname):

    if (os.path.exists('CITATIONS') == False):
        os.system('mkdir CITATIONS')

    o_fn='CITATIONS/'+Short
    if (os.path.exists(o_fn) == False):
        syscall='mkdir '+o_fn
        os.system(syscall)

    recs_fn='/home/'+uname+'/Downloads/savedrecs.xls'
    if (os.path.exists(recs_fn) == True):
        syscall='rm '+recs_fn
        os.system(syscall)

    return()

#################################################################
# Print out which paper is being downloaded.                    #
#################################################################

def print_paper(Short,iy,ipap,npap,n_dwnl,n_thr):

    ostr='Downloading '+Short+' '+str(iy)+', paper '+str(ipap+1)
    ostr=ostr+' out of '+str(npap)+', download '+str(n_dwnl)
    ostr=ostr+' out of '+str(n_thr)+'.'
    print(ostr)

    return()

#################################################################
# Get the "Export Records to Excel" window.                     #
#################################################################

def get_save_window(driver):

    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="snRecListTop"]/app-export-menu/div/button/span[1]'
            ))).click()
        time.sleep(0.25)

        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="exportToExcelButton"]'
            ))).click()
        time.sleep(0.25)
    except:
        pass

    time.sleep(0.25)
    pyautogui.press('esc')
    time.sleep(0.25)

    return()

#################################################################
# Save the excel file.                                          #
#################################################################

def save_file(driver,i_ref_rep,nref,uname,Location):

    try:
# Select the full record option.
        if (Location == 'Home'):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/app-wos/div/div/main/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/div[1]/wos-select/button/span[1]'))).click()
        if (Location == 'Office'):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/app-wos/div/div/main/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/div[1]/wos-select/button/span[1]'))).click()
        time.sleep(0.25)

        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,
            '//*[@id="global-select"]/div/div[2]/div[3]/span'))).click()
        time.sleep(0.25)

# Select the first and last record.
        print('Selecting the first and last record.')

        if (Location == 'Home'):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="radio3"]/label/span[2]'
                ))).click()
        if (Location == 'Office'):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="radio3"]/label/span[2]'
                ))).click()
        time.sleep(0.25)

        if (nref > 1000):

            if (Location == 'Home'):
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                    By.XPATH,
                '/html/body/app-wos/div/div/main/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-form-field[1]/div/div[1]/div[3]'))).click()
            if (Location == 'Office'):
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                    By.XPATH,
                '/html/body/app-wos/div/div/main/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-form-field[1]/div/div[1]/div[3]'))).click()
            time.sleep(0.25)
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.typewrite('\b')
            pyautogui.typewrite('\b')
            pyautogui.typewrite('\b')
            pyautogui.typewrite('\b')
            time.sleep(0.25)

            ostr1=str(i_ref_rep*1000+1)
            pyautogui.typewrite(ostr1)

            if (Location == 'Home'):
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                    By.XPATH,
                '/html/body/app-wos/div/div/main/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-form-field[2]/div/div[1]/div[3]'))).click()
            if (Location == 'Office'):
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                    By.XPATH,
                '/html/body/app-wos/div/div/main/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/fieldset/mat-radio-group/div[3]/mat-form-field[2]/div/div[1]/div[3]'))).click()
            time.sleep(0.25)
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.press('right')
            pyautogui.typewrite('\b')
            pyautogui.typewrite('\b')
            pyautogui.typewrite('\b')
            pyautogui.typewrite('\b')
            time.sleep(0.25)

            nfin=(i_ref_rep+1)*1000
            if (nfin > nref):
                nfin=nref
            ostr2=str(nfin)
            pyautogui.typewrite(ostr2)

# Click the export button.

        if (Location == 'Home'):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,
            '/html/body/app-wos/div/div/main/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/div[2]/button[1]/span[1]/span'))).click()
        if (Location == 'Office'):
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,
            '/html/body/app-wos/div/div/main/div/div/div[2]/app-input-route[1]/app-export-overlay/div/div[3]/div[2]/app-export-out-details/div/div[2]/form/div/div[2]/button[1]/span[1]/span'))).click()
        time.sleep(0.25)

    except:
        pass

    return()

#################################################################
# Save the paper file.                                          #
#################################################################

def save_paper(driver,ncit,uname,Short,DOI,Location):

    DOI=DOI.replace('/','_')
    DOI=DOI.replace('(','_')
    DOI=DOI.replace(')','_')
    DOI=DOI.replace('<','_')
    DOI=DOI.replace('>','_')
    DOI=DOI.replace(';','_')
    DOI=DOI.replace(':','_')

    n_ref_rep=1+int(ncit/1000)
    for i_ref_rep in range(0,n_ref_rep):
        get_save_window(driver)
        save_file(driver,i_ref_rep,ncit,uname,Location)
        recs_fn='/home/'+uname+'/Downloads/savedrecs.xls'
        nsec=0
        while ( (os.path.exists(recs_fn) == False) and (nsec < 30) ):
            ostr='Waiting for the download, '+str(nsec)+' out of '+str(30)+'.'
            print(ostr)
            time.sleep(1)
            nsec=nsec+1
        if (os.path.exists(recs_fn) == False):
            repeat=1
        if (ncit == 0):
            repeat=0
        if (os.path.exists(recs_fn) == True):
            syscall='\mv /home/'+uname+'/Downloads/savedrecs.xls CITATIONS/'
            syscall=syscall+Short+'/'+DOI+'_'
            syscall=syscall+str(i_ref_rep)+'.xls'
            print(syscall)
            os.system(syscall)
            repeat=0

    return(repeat)

#################################################################
# Download a record and put it in the correct folder.           #
#################################################################

def download_and_move(driver,uname,
        iy,J_names,ijo,data,ipap,n_dwnl,n_thr,Location,ubuntu_version):

    repeat=1
    n_repeat=0
    while (repeat == 1):
        n_repeat=n_repeat+1
        print_paper(J_names['Short'][ijo],iy,ipap,
                data.shape[0],n_dwnl,n_thr)
        link='https://www.webofscience.com/wos/woscc/'
        link=link+'citing-summary/'
        link=link+data['UT (Unique WOS ID)'][ipap]
        link=link+'?from=woscc'
        driver.get(link)
        time.sleep(0.25)
        ncit=int(data['Times Cited, WoS Core'][ipap])
        if (ncit > 1000):
            print_wait(5)
            ncit=extract_ncit(ubuntu_version)
        if (ncit == 0):
            repeat=0
        if (ncit > 0):
            DOI=data['DOI'][ipap]
            if (isNaN(DOI) == True):
                wos_id=data['UT (Unique WOS ID)'][ipap]
                if (isNaN(wos_id) == False):
                    DOI=str(wos_id.split(':')[1])
            if (isNaN(DOI) == True):
                repeat=0
            if (isNaN(DOI) == False):
                repeat=save_paper(driver,ncit,uname,
                        J_names['Short'][ijo],DOI,Location)
                n_dwnl=n_dwnl+1
                if (n_dwnl > n_thr):
                    n_dwnl=1
                    logout(driver)
                    login(driver)
        if (n_repeat == 5):
            repeat=0

    return(n_dwnl)

#################################################################
# Process one year for a journal.                               #
#################################################################

def process_journal_year(irep1,pap1,n_thr,n_dwnl,driver,J_names,ijo,iy,uname,
        Location,run_opt,ubuntu_version):

    irep=0
    while (irep >= 0):
        i_fn=prep_fn(J_names,ijo,iy,irep)
        if (os.path.exists(i_fn) == False):
            irep=-9999
        if (os.path.exists(i_fn) == True):
            print_j(J_names,ijo,iy)

            data=pd.read_excel(i_fn)
            paper_1=0
            if (irep == irep1):
                paper_1=pap1
            for ipap in range(paper_1,data.shape[0]):
                igo=1
                if (run_opt == 3):
                    igo=0
                    if (data['Times Cited, WoS Core'][ipap] > 1000):
                        igo=1
                if (igo == 1):
                    n_dwnl=download_and_move(driver,uname,
                            iy,J_names,ijo,data,ipap,
                            n_dwnl,n_thr,Location,ubuntu_version)

            irep=irep+1

    return(n_dwnl)

#################################################################
# Log on to the website.                                        #
#################################################################

def login_old(new_laptop,driver):

    driver.get('https://www.webofscience.com')
    print_wait(2)

    if (new_laptop == 1):
        time.sleep(1)
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
#                By.XPATH,'//*[@id="signIn-btn"]'))).click()
                By.XPATH,'/html/body/app-wos/div/div/header/app-header/div[1]/div[2]/div/div[3]/button[1]'))).click()
        time.sleep(1)
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
                By.XPATH,'//*[@id="mat-menu-panel-3"]/div/div/a[1]'))).click()
        time.sleep(1)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="signIn-btn"]/span[1]/span[1]'))).click()

    print('Logged in.')
    print_wait(20)

    return()

def login(driver):

     pyautogui.hotkey('ctrl','l')
     time.sleep(0.5)
     pyautogui.press('backspace')
     time.sleep(0.5)
#     pyautogui.typewrite('https://www.webofscience.com')
     pyautogui.typewrite('https://access.clarivate.com/login?app=wos&referrer=wpath%3D%252Fwoscc%252Fbasic-search%26wstate%3D%257B%257D&locale=en-US')
     time.sleep(0.5)
     pyautogui.press('enter')
     print('Going to the logon page.')
     print_wait(20)
     for irep in range(0,6):
         pyautogui.press('tab')
     time.sleep(0.5)
     pyautogui.press('enter')
     print('Waiting to be logged on.')
     print_wait(20)

     return()

#################################################################
# Log out of the web of science.                                #
#################################################################

def logout(driver):

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,
    '/html/body/app-wos/div/div/header/app-header/div[1]/div[2]/div/div[3]/button/span'
            ))).click()
    time.sleep(1)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,'//*[@id="mat-menu-panel-2"]/div/div/a[3]'))).click()
    print('Logged out.')
    print_wait(20)

    return()

#################################################################
# Determine the location where the code is run.                 #
#################################################################

def det_loc(argv,J_names):

    ijo1=-1
    ijo2=-1
    if (len(argv) != 4):
        print("Run the code as:")
        print("python3 download_citations.py Home num1 num2")
        print("or")
        print("python3 download_citations.py Office num1 num2")
        print("num1 and num2 are zero if one laptop downloads everything.")
        print("Otherwise, num1 is the part of the total number of")
        print("journals divided by num2.")
        exit()
    Location=argv[1]
    if ( (Location != 'Office') and (Location != 'Home') ):
        print("Run the code as:")
        print("python3 download_citations.py Home num1 num2")
        print("or")
        print("python3 download_citations.py Office num1 num2")
        print("num1 and num2 are zero if one laptop downloads everything.")
        print("Otherwise, num1 is the part of the total number of")
        print("journals divided by num2.")
        exit()
    num1=int(argv[2])
    num2=int(argv[3])
    if ( (num1 == 0) and (num2 != 0) ):
        print ("If the second number is nonzero the first cannot be zero.")
        exit()
    if (num1 > num2):
        print("The first number cannot be larger than the second.")
        exit()

    if (num2 == 0):
        ijo1=0
        ijo2=J_names.shape[0]
    if (num2 > 0):
        part=math.ceil(J_names.shape[0]/num2)
        ijo2=num1*part
        ijo1=ijo2-part
        if ( (ijo2 < J_names.shape[0]) and (num1 == num2) ):
            ijo2=J_names.shape[0]
        if (ijo2 > J_names.shape[0]):
            ijo2=J_names.shape[0]

    return(Location,ijo1,ijo2)

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
#################################################################
# Start the main code.                                          #
#################################################################
#################################################################

def main():

    starttime=time.time()

    ubuntu_version=release()

    J_names=pd.read_csv('journals_ALL.csv')
    Location,ijo1,ijo2=det_loc(sys.argv,J_names)

    run_opt=1
# 1: Download all records for all journals.
# 2: A second pass, only download the missing records.
# 3: Redownload the papers with more than 1000 citations.

    URL='https://www.webofscience.com'

    uname=start_msg(URL)

    chrome_options=Options()
    chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9014")

    executable='/home/'+uname+'/.wdm/drivers/chromedriver/linux64/102.0.5005.61/chromedriver'
    s=Service(executable)

    driver=webdriver.Chrome(service=s,options=chrome_options)

    login(driver)
    n_dwnl=1
    n_thr=300

    for ijo in range(ijo1,ijo2):
        if (run_opt == 2):
            i_fn='Missing_Files/'+J_names['Short'][ijo]+'_Missing.csv'
            if (os.path.exists(i_fn) == True):
                data=pd.read_csv(i_fn)
                for ipap in range(0,data.shape[0]):
                    iy=data['Publication Year'][ipap]
                    if (isNaN(iy) == False):
                        iy=int(iy)
                    if (isNaN(iy) == True):
                        iy=-9999
                    n_dwnl=download_and_move(driver,uname,iy,
                            J_names,ijo,data,ipap,n_dwnl,n_thr,Location,
                            ubuntu_version)
        if ( (run_opt == 1) or (run_opt == 3) ):
            irep1=0
            year1=int(J_names['First Year'][ijo])
            check_directory(J_names['Short'][ijo],uname)
            for iy in range(year1,int(J_names['Last Year'][ijo])+1):
                pap1=0
                irep1=0
                n_dwnl=process_journal_year(irep1,pap1,n_thr,n_dwnl,
                        driver,J_names,ijo,iy,uname,Location,
                        run_opt,ubuntu_version)

    duration(starttime)

main()
