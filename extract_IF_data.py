#################################################################
#################################################################
# Extract the IF data from the html files.                      #
#################################################################
#################################################################

import time
import os
import pandas as pd

#################################################################
# Check if a variable is nan.                                   #
#################################################################

def isNaN(var):

    return (var != var)

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
# Extract the necessary data from the html file.                #
#################################################################

def extract_data(i_fn,iy):

    ifac=-9999

    i_ptr=open(i_fn,'r')

    html=[]

    string1='Citations in '+str(iy)+' to items published in '+str(iy-2)+' ('
    string2='Number of citable items in '+str(iy-2)+' ('
    string3='last-two-year-jif-and-citations-calculation-result"> ='
    len1=len(string1)
    len2=len(string2)
    len3=len(string3)

    ifin=0
    while (ifin == 0):
        pars=i_ptr.readline()
        if (pars == ""):
            ifin=1
        if (pars != ""):
            html.append(pars)

    i_ptr.close()

    iline=-1
    while (iline < len(html)-1):
        iline=iline+1
        if (len(html[iline]) > len3):
            icol=-1
            while (icol < len(html[iline])-len3-1):
                icol=icol+1
                string=''
                for ilet in range(icol,icol+len3):
                    string=string+html[iline][ilet]
                if (string == string3):
                    icol=icol+len3+1
                    icol,string=extract_string(html,iline,icol,' ')
                    if (string != 'N/A'):
                        ifac=float(string)

                    icol=len(html[iline])

    cit1,cit2=extract_numbers(string1,html,len1)
    pub1,pub2=extract_numbers(string2,html,len2)

    return(pub1,pub2,cit1,cit2,ifac)

#################################################################
# Extract numbers according to a specific string from the file. #
#################################################################

def extract_numbers(string1,html,len1):

    pub1=-9999
    pub2=-9999

    iline=-1
    while (iline < len(html)-1):
        iline=iline+1
        if (len(html[iline]) > len1):
            icol=-1
            while (icol < len(html[iline])-len1-1):
                icol=icol+1
                string=''
                for ilet in range(icol,icol+len1):
                    string=string+html[iline][ilet]
                if (string == string1):
                    icol=icol+len1+6
                    icol,string=extract_string(html,iline,icol,'<')
                    pub1=int(string)
                    while (pub2 < 0):
                        icol=icol+1
                        string=''
                        for ilet in range(icol,icol+6):
                            string=string+html[iline][ilet]
                        if (string == '<span>'):
                            pub2=0
                            icol=icol+6
                            icol,string=extract_string(html,iline,icol,'<')
                            pub2=int(string)

                    icol=len(html[iline])

    return(pub1,pub2)

#################################################################
# Extract a specific string from a line.                        #
#################################################################

def extract_string(html,iline,icol,stop):

    string=html[iline][icol]
    icmp=0
    while (icmp == 0):
        icol=icol+1
        if (html[iline][icol] != stop):
            string=string+html[iline][icol]
        if (html[iline][icol] == stop):
            icmp=1
    string=string.replace(',','')

    return(icol,string)

#################################################################
# Process a specific journal.                                   #
#################################################################

def process_journal(ijo,J_names,Y1,Y2):

    o_fn='IF_DATA/'+J_names['Short'][ijo]+'/'+J_names['Short'][ijo]
    o_fn=o_fn+'_'+'IF_data.csv'
    PB1=[]
    PB2=[]
    NC1=[]
    NC2=[]
    IFC=[]
    YEARS=[]
    for iy in range(Y1,Y2):
        YEARS.append(iy)
        ostr='Processing '+J_names['Short'][ijo]+' '+str(iy)+'.'
        print(ostr)
        i_fn='IF_DATA/'+J_names['Short'][ijo]+'/'+J_names['Short'][ijo]
        i_fn=i_fn+'_'+str(iy)+'.html'
        if (os.path.exists(i_fn) == False):
            PB1.append(0)
            PB2.append(0)
            NC1.append(0)
            NC2.append(0)
            IFC.append(0)
        if (os.path.exists(i_fn) == True):
            pub1,pub2,cit1,cit2,ifac=extract_data(i_fn,iy)
            print(pub1,pub2,cit1,cit2,ifac)
            PB1.append(pub1)
            PB2.append(pub2)
            NC1.append(cit1)
            NC2.append(cit2)
            IFC.append(ifac)

    data={'Year':YEARS,
            'Publications 2 Years Back':PB1,
            'Publications 1 Year Back':PB2,
            'Citations 2 Years Back':NC1,
            'Citations 1 Year Back':NC2,
            'Impact Factor':IFC,
            }

    results=pd.DataFrame(data)

    results.to_csv(o_fn,sep=',',index=False)

    return()

#################################################################
#################################################################
# Start the main code.                                          #
#################################################################
#################################################################

def main():

    Y1=2000
    Y2=2022

    starttime=time.time()

    J_names=pd.read_csv('journals_IF.csv')

    for ijo in range(0,J_names.shape[0]):
        process_journal(ijo,J_names,Y1,Y2)

    duration(starttime)

main()
