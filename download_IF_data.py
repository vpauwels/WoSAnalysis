#################################################################
#################################################################
# Download the calculations of the Impact Factor data.          #
# Download the journal list year by year.                       #
# Start chrome using the command                                #
# /opt/google/chrome/chrome -remote-debugging-port=9014 --user-data-dir="/home/vpauwels/Selenium_Dump" #
#################################################################
#################################################################

import time
import getpass
import os
import pandas as pd

import pyautogui

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import date

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
    today=str(date.today())
    year=today.split('-')[0]
    month=today.split('-')[1]

    pwd=os.getcwd()

    csv_fn='/home/'+uname+'/Downloads/ValentijnPauwels_JCR_JournalResults_'
    csv_fn=csv_fn+month+'_'+year+'.csv'

    print("Make sure you are on the Monash network, either using a VPN")
    print("or by using the Monash wired network.")
    print("Start chrome using the command")
    cmd='/opt/google/chrome/chrome -remote-debugging-port=9014 --user-data-dir="/home/'+uname+'/Selenium_Dump"'
    print(cmd)
    print("Log on to the Journal Citation Reports:")
    print(URL)
    print("Make sure to be logged on.")
    print("Make sure to click all the options away.")
    print("\aWhen all this is done, press <Enter>.")
    a=input()
    print("Activate the browser window.")
    print_wait(5)

    if (os.path.exists('IF_DATA') == False):
        os.system('mkdir IF_DATA')

    return(pwd,csv_fn,month,year,uname)

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
# Determine the length of the journals list file.               #
#################################################################

def length(csv_fn):

    syscall='wc '+csv_fn+' > len.txt'
    os.system(syscall)
    i_ptr=open('len.txt','r')
    pars=i_ptr.readline()
    par=pars.split(' ')
    nline=-9999
    ipar=-1
    while (nline < 0):
        ipar=ipar+1
        if (par[ipar] != ''):
            nline=int(par[ipar])
    i_ptr.close()
    syscall='rm len.txt'
    os.system(syscall)
    syscall='rm '+csv_fn
    os.system(syscall)

    return(nline)

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
# Enter the journal name.                                       #
#################################################################

def enter_journal(URL,driver,J_names,ijo):

    dir_fn='IF_DATA/'+J_names['Short'][ijo]
    if (os.path.exists(dir_fn) == False):
        syscall='mkdir '+dir_fn
        os.system(syscall)
    driver.get(URL)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((
        By.XPATH,'//*[@id="search-bar"]'))).click()
    time.sleep(0.25)
    element=driver.find_element(By.XPATH,'//*[@id="search-bar"]')
    time.sleep(0.25)
    element.click()
    element.send_keys(J_names['Long'][ijo])

    print_wait(5)

    element.send_keys(Keys.RETURN)

    print_wait(5)

    return(dir_fn)

#################################################################
# Click on the journal.                                         #
#################################################################

def click_journal(driver,csv_fn):

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((
        By.XPATH,
        '/html/body/div[1]/div[2]/div/div[1]/div[4]/div/div[3]/div/mat-icon'
        ))).click()
    time.sleep(0.25)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((
        By.XPATH,'//*[@id="mat-menu-panel-2"]/div/button[1]'))).click()
    time.sleep(0.25)

    while (os.path.exists(csv_fn) == False):
        time.sleep(1)
        print('Waiting for the csv file to download.')

    nline=length(csv_fn)

    if (nline == 9):
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/div[1]/div[2]/div/div[2]/div/div/section[1]/mat-table/mat-row/mat-cell[1]/span',
            ))).click()
        time.sleep(0.25)
    if (nline > 9):
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((
            By.XPATH,
            '/html/body/div[1]/div[2]/div/div[2]/div/div/section[1]/mat-table/mat-row[1]/mat-cell[1]/span',
            ))).click()
        time.sleep(0.25)

    return()

#################################################################
# Locate the impact factor on the screen.                       #
#################################################################

def search_IF(iy):

    pyautogui.hotkey('ctrl','f')
    search_str=str(iy)+' JOURNAL IMPACT FACTOR'
    time.sleep(1)
    pyautogui.typewrite(search_str)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.press('esc')
    time.sleep(0.5)
    pyautogui.press('tab')
    pyautogui.press('tab')

    return()

#################################################################
# Open the impact factor data window.                           #
#################################################################

def click_IF(xcl,ycl):

    if (xcl < 0):
        print('Activate the Linux terminal.')
        print('\aMove the cursor above the <View calculation> link.')
        print('Press <Enter>.')
        a=input()
        xcl,ycl=pyautogui.position()
        print('Active the browser.')
        print_wait(5)
    time.sleep(0.5)
    pyautogui.moveTo(xcl,ycl,duration=0.5)
    pyautogui.click(button='left')
    time.sleep(1)

    return(xcl,ycl)

#################################################################
# Save the html file.                                           #
#################################################################

def save_html(iy,ubuntu_version,pwd,dir_fn,J_names,ijo):

    pyautogui.hotkey('ctrl','s')
    time.sleep(1)
    if (ubuntu_version >= 21):
        pyautogui.hotkey('alt','tab')
        time.sleep(1)
        pyautogui.hotkey('alt','tab')
        time.sleep(1)

    o_fn=pwd+'/'+dir_fn
    o_fn=o_fn+'/'+J_names['Short'][ijo]
    o_fn=o_fn+'_'+str(iy)

    i_fn=o_fn+'.html'
    if (os.path.exists(i_fn) == True):
        syscall='rm '+i_fn
        os.system(syscall)
    i_fn=o_fn+'_files'
    if (os.path.exists(i_fn) == True):
        syscall='rm -r '+i_fn
        os.system(syscall)

    pyautogui.typewrite(o_fn)
    time.sleep(0.5)
    pyautogui.press('enter')

    i_fn=o_fn+'.html'
    while (os.path.exists(i_fn) == False):
        print('Waiting for the download.')
        time.sleep(1)
    i_fn=o_fn+'_files'
    while (os.path.exists(i_fn) == False):
        print('Waiting for the download.')
        time.sleep(1)
    syscall='rm -r '+i_fn
    os.system(syscall)

    return()

#################################################################
# Change the year that is being processed.                      #
#################################################################

def change_year(xyear,yyear):

    time.sleep(0.25)
    pyautogui.click(button='left')
    time.sleep(0.25)
    pyautogui.hotkey('ctrl','home')
    time.sleep(0.25)
    pyautogui.hotkey('ctrl','f')
    if (xyear < 0):
        print('Activate the Linux terminal.')
        print('\aMove the cursor above the <JCR Year> menu.')
        print('Press <Enter>.')
        a=input()
        xyear,yyear=pyautogui.position()
        print('Active the browser.')
        print_wait(5)
    pyautogui.moveTo(xyear,yyear,duration=0.5)
    pyautogui.click(button='left')
    time.sleep(1)
    pyautogui.typewrite(['down'])
    time.sleep(1)
    pyautogui.press('enter')
    print_wait(5)

    return(xyear,yyear)

#################################################################
#################################################################
# Start the main code.                                          #
#################################################################
#################################################################

def main():

    starttime=time.time()

    URL='https://jcr.clarivate.com/jcr/home'

    pwd,csv_fn,cur_month,cur_year,uname=start_msg(URL)
    ubuntu_version=release()

    chrome_options=Options()
    chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9014")

    executable='/home/'+uname+'/.wdm/drivers/chromedriver/linux64/102.0.5005.61/chromedriver'
    s=Service(executable)

    driver=webdriver.Chrome(service=s,options=chrome_options)

    J_names=pd.read_csv('journals_ALL.csv')

    xcl=-100
    ycl=-100
    xyear=-100
    yyear=-100

    for ijo in range(0,J_names.shape[0]):
        iy=J_names['Last Year'][ijo]
        dir_fn=enter_journal(URL,driver,J_names,ijo)
        click_journal(driver,csv_fn)
        print_wait(10)
        while (iy >= J_names['First Year'][ijo]):
            search_IF(iy)
            xcl,ycl=click_IF(xcl,ycl)
            save_html(iy,ubuntu_version,pwd,dir_fn,J_names,ijo)
            xyear,yyear=change_year(xyear,yyear)
            iy=iy-1
        pyautogui.hotkey('ctrl','w')

    duration(starttime)

main()

