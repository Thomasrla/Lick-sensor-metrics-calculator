# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:13:22 2023

@author: Thomas La
"""

import pandas as pd
import numpy as np
import glob

sessionday = "session X"

mouse = {'H01': ['male', 'Med'],
          'H02': ['male', 'Med'],
          # 'H04': ['male', 'Med'],
          'H06': ['female', 'Lat'],
          'H07': ['female', 'Med'],
          'H08': ['female', 'Med'],
          # 'H09': ['female', 'Lat'],
          #'H11': ['male', 'Lat'],
          'H12': ['male', 'Lat'],
          'H13': ['male', 'Lat'],
          'H15': ['male', 'Med'],
          # 'H16': ['female', 'Med'],
          # 'H17': ['female', 'Med'],
          'H18': ['female', 'Lat'],
          # 'H19': ['female', 'Med'],
          'H20': ['female', 'Med']
          }

df = pd.DataFrame()

for h in mouse:
    path =r"C:\Users\break\Documents\testing pyhon"
    filenames = glob.glob(path + "/*.csv")
    for p in filenames: 
        tokens = p.split('\\')
        # print(tokens)
        if h in tokens[-1]:
            break
    else: # no break
        print(f'{h}.csv not found')
        continue
    
    print(f'Found {h}.csv')
    
    csv = pd.read_csv(p, header=None)
    print(csv)
    
    #readjusts the 9 and 0 index for licks
    for i in np.arange(len(csv)):
        if csv.iloc[i][0].startswith('9 ') == True :
            newlabel = csv.iloc[i][0].split()
            newlabel[0] = '9 9 '
            adjustedlickstamp = "".join(newlabel)
            csv.iloc[i] = adjustedlickstamp
        elif csv.iloc[i][0].startswith('0 ') == True :
            newlabel = csv.iloc[i][0].split()
            newlabel[0] = '0 0 '
            adjustedlickstamp = "".join(newlabel)
            csv.iloc[i] = adjustedlickstamp
            
    csv = pd.DataFrame(csv[0].str.split(' ',2).tolist(),
                                     columns = ['index','step', 'timestamp'])
    
    datadict = {'ax': ['13', '1', '3'],
                'ay': ['14', '1', '4'],
                'bx': ['23', '2', '3'],
                'by': ['24', '2', '4']
                }
    
    
    dictionary = { 'mousename':[],'mousesex':[],'sessionday':[], 'trialtype':[], 
                 'cueslickprobability':[],'cuesavglickspercue':[], 'cuesavglatencypercue':[], 
                 'firstcuelickprobability':[], 'firstavglickspercue':[], 'firstavglatencypercue':[], 
                 'secondcuelickprobability':[], 'secondavglickspercue':[], 'secondavglatencypercue':[], 
                 'rewlickprobability':[], 'rewavglicksperrew':[], 'rewavglatencyperrew':[]
                 }
    
    for i in datadict:
        trialname = i
        trialindex = datadict[i][0]
        trialfirstcue = datadict[i][1]
        trialsecondcue = datadict[i][2]
        
        licks = csv.query("index == '9'")
        trialtype = csv.query("index == @trialindex")
        firstcue = trialtype.query("step == @trialfirstcue")
        secondcue = trialtype.query("step == @trialsecondcue")
        
        def lickmath(startevent, delay):
            lickedtrials = 0 
            sumfirstlick = 0
            totallicks = 0

            #index through each trial, finds stats for each event
            for j in np.arange(len(startevent)):
                #this will reset the number of licks for each trial
                lickstamps = np.array([])
            
                #index through each lick for one event onset
                for k in np.arange(len(licks)):
                    #subtracts the licktimestamp from startevent and checks if lick is within the event
                    if (0 >= int(startevent.iloc[j][2]) - int(licks.iloc[k][2]) >= delay):
                        #adds each corresponding lick to the event onset
                        lickstamps = np.append(lickstamps, np.array(licks.iloc[k][2]))
                        
                #aggregates total licks to an averaging pool        
                totallicks = len(lickstamps) + totallicks
                if len(lickstamps) > 0:
                    #finds the first lick for latency calculation and adds it to an averaging pool
                    firstlick = int(lickstamps[0]) - int(startevent.iloc[j][2])
                    sumfirstlick = firstlick + sumfirstlick
                    #if this is a licked event, index by one for averaging     
                    lickedtrials = lickedtrials + 1
            #summary calculations and avoid diving by 0        
            if lickedtrials > 0: 
                lickprob = lickedtrials / len(startevent) 
                avglicks = totallicks / lickedtrials
                avglatency = sumfirstlick / lickedtrials
            else: 
                lickprob = 0
                avglicks = 0
                avglatency = 0
            return lickprob, avglicks, avglatency
        
        cues = lickmath(firstcue, -4000)
        first =lickmath(firstcue, -2000) 
        second =lickmath(secondcue, -2000)
        rew = lickmath(firstcue, -8000)

        dictionary['mousename'].append(h)
        dictionary['mousesex'].append(mouse[h][0])
        dictionary['session'].append(sessionday)
        dictionary['trialtype'].append(trialname)
        dictionary['cueslickprobability'].append(cues[0])
        dictionary['cuesavglickspercue'].append(cues[1])
        dictionary['cuesavglatencypercue'].append(cues[2])
        dictionary['firstcuelickprobability'].append(first[0])
        dictionary['firstavglickspercue'].append(first[1])
        dictionary['firstavglatencypercue'].append(first[2])
        dictionary['secondcuelickprobability'].append(second[0])
        dictionary['secondavglickspercue'].append(second[1])
        dictionary['secondavglatencypercue'].append(second[2])
        dictionary['rewlickprobability'].append(rew[0])
        dictionary['rewavglicksperrew'].append(rew[1])
        dictionary['rewavglatencyperrew'].append(rew[2])
    
    xdf = pd.DataFrame.from_dict(dictionary)
    df = df.append([xdf], ignore_index= True)
    
    
 
df.to_csv(r'C:/Users/break/Downloads/test.csv', index= False, header = True)
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        