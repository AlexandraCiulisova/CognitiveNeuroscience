#import libraries
import psychtoolbox as ptb
from psychopy import prefs, core, visual, event, sound, monitors
import glob
import pandas as pd
import os
from triggers import setParallelData
prefs.hardware['audioLib'] = ['PTB'] #inserting preference here for lowest latency option


# path to the file
experimental_pyfile_path = os.path.abspath(__file__)
# path to the directory with the py file containing the experiment
path = os.path.dirname(experimental_pyfile_path)


# define logfile 
# prepare pandas data frame for recorded data
columns = ['trial_number','response', 'trial_type', 'music_condition', 'stim_condition']
logfile = pd.DataFrame(columns=columns)

# define fixation cross
def fixation(win):
    msg = visual.TextStim(win,"+")

    for frame in range(30): 
        msg.draw()
        if frame==1: 
            win.callOnFlip(setParallelData, 100)
            pullTriggerDown = True
        else: 
            win.callOnFlip(setParallelData, 0)
            pullTriggerDown = False
        win.flip()
        #if frame == 1: print(100)


#define function for keyboard input
def get_response(img):
    key = event.waitKeys(keyList = ["left", "right", "escape"]) #which keys should be used for response?
    if key[0] == "escape":
        core.quit()
    else:
        response = 0 if key[0]=="left" else 1
    return response
#response 0 (right)= coherent, response 1 (left)= incoherent


# now we can define all paths we will be using (e.g. to the stimuli and where we want to save the csv relative to the experimental path!)
dataframe_path = os.path.join(path, "my_data4.csv")

# read csv file containing names of stimuli folders
df = pd.read_csv(dataframe_path) 
'''
stimuli_path = os.path.join(path, "stimuli")
print("path to stimuli: ", stimuli_path)
'''
#contains 5 columns: 
#[trial_type]: 0 or 1, (for action or sentence)
#[music] name of folder containing 8 audio files
#[stim] either a string of word segments separeated by ";" or folder name of 8 images 
#[music_condition] 0 or 1 for congruent or incongruent
#[stim_condition] 0 or 1 for coherent or incoherent



logfiles_path = os.path.join(path, "logfiles")

# make sure that there is a logfile directory and otherwise make one
if not os.path.exists("logfiles"):
    os.makedirs("logfiles")

date = "test" #change this before running!
# define logfile name
logfile_name = os.path.join(path,logfiles_path,"logfile_{}.csv".format(date))


#presenting instructions

# define window
my_monitor = monitors.Monitor('testMonitor')
win = visual.Window(monitor = my_monitor, fullscr = True, units = "pix")
msg = visual.TextStim(win,height = 40, text="You will be asked to rate the semantic coherence of some sentences and image sequences.\n\nPress the [Left] arrow for Coherent and the [Right] one for Incoherent.\n\n Music will be played throughout, but you should ignore it and only care about the sentences and images \n\n Press [Left] to start") 
msg.draw()
win.flip()
keys = event.waitKeys(keyList = ["left"])


trial_number = 0 #initialise this counting variable

pullTriggerDown = False

#loop through trials
for i in range(80): #80 irl, or 40 if we do break between blocks
    trial_number += 1
    sound_folder_name = os.path.join(path, "EEG_chords",df.iloc[i,3],"*")
    my_sound_list = sorted(glob.glob(sound_folder_name))
    msg = visual.TextStim(win,"+", height = 50)

    for frame in range(30): 
        msg.draw()
        if frame==1: 
            win.callOnFlip(setParallelData, 100)
            pullTriggerDown = True
        else: 
            win.callOnFlip(setParallelData, 0)
            pullTriggerDown = False
        win.flip()
        #if frame == 1: print(100)
    
    if df.iloc[i,5] == 1: #check for language or action
        my_word_list = df.iloc[i,1].split(sep = "-") #list
        
        for j in range(7): #loop through sentence
            
            my_sound = sound.Sound(my_sound_list[j], secs = 0.6)
            text = my_word_list[j]
            
            
            msg = visual.TextStim(win, text, height = 50)
            
            for frame in range(int(60*0.6)):
                msg.draw()
                if frame == 1:
                    win.callOnFlip(setParallelData, 10*(j+1))
                    pullTriggerDown = True
                    nextFlip = win.getFutureFlipTime(clock='ptb')
                    my_sound.play(when=nextFlip)
                else:
                    win.callOnFlip(setParallelData, 0)
                    pullTriggerDown = False
                win.flip()
        #last trial out of loop       
        my_sound = sound.Sound(my_sound_list[7], secs = 1.2) 
        text = my_word_list[7]
        trigger = int(df.iloc[i,2] *4 + df.iloc[i,4] *2 + df.iloc[i,5]+1)
        
        msg = visual.TextStim(win, text, height = 50)
        
        for frame in range(int(60*1.2)):
            msg.draw()
            if frame == 1:
                win.callOnFlip(setParallelData, trigger)
                pullTriggerDown = True
                nextFlip = win.getFutureFlipTime(clock='ptb')
                my_sound.play(when=nextFlip)
            #if frame == 1: print(trigger) #testing
            else:
                win.callOnFlip(setParallelData, 0)
                pullTriggerDown = False
            win.flip()
        
        msg = visual.TextStim(win, "+", height = 50)
        
        for frame in range(2):
            if frame == 1:
                win.callOnFlip(setParallelData, 200)
                pullTriggerDown = True
            else:
                win.callOnFlip(setParallelData, 0)
                pullTriggerDown = False
            msg.draw()
            win.flip()
        response = get_response(msg)
        setParallelData(response+11)
    else: 
        img_folder_name = os.path.join(path,df.iloc[i,1],"*")
        my_img_list= sorted(glob.glob(img_folder_name))
        for j in range(7): #loop through pictures
            my_sound = sound.Sound(my_sound_list[j], secs = 0.6) 
            img = my_img_list[j]
            
            

            msg = visual.ImageStim(win, img, size=(800, 1000))
                
            for frame in range(int(60*0.6)):
                msg.draw()
                if frame == 1:
                    win.callOnFlip(setParallelData, 10*(j+1))
                    pullTriggerDown = True
                    nextFlip = win.getFutureFlipTime(clock='ptb')
                    my_sound.play(when=nextFlip)
                else:
                    win.callOnFlip(setParallelData, 0)
                    pullTriggerDown = False
                win.flip()
            
#do last trial out of loop to do trigger and different core.wait time    
        my_sound = sound.Sound(my_sound_list[7], secs = 1.2) 
        trigger = int(df.iloc[i,2] *4 + df.iloc[i,4] *2 + df.iloc[i,5]+1) 
         
         
        #nextFlip = win.getFutureFlipTime(clock='ptb')
        #my_sound.play(when=nextFlip)
            
        img = my_img_list[7]
        msg = visual.ImageStim(win, img, size=(800, 1000))
        '''
        for frame in range(duration*FRAME_RATE): 
            msg.draw()
            if frame==1: 
                win.callOnFlip(setParallelData, trigger)
                pullTriggerDown = True
                #start sound
            else: 
                win.callOnFlip(setParallelData, trigger)
                pullTriggerDown = False
            win.flip()
        ''' 
        for frame in range(int(60*1.2)):
            msg.draw()
            if frame == 1:
                win.callOnFlip(setParallelData, trigger)
                pullTriggerDown = True
                nextFlip = win.getFutureFlipTime(clock='ptb')
                my_sound.play(when=nextFlip)
            else:
                win.callOnFlip(setParallelData, 0)
                pullTriggerDown = False
            win.flip()
            #if frame == 1: print(trigger) #testing
        
        
        #msg.draw()
        
        #win.callOnFlip(setParallelData, trigger)
        #pullTriggerDown = True  # Trigger is active now
        
        #win.flip() #implement trigger for this 
        #print(trigger)
        #core.wait(1.2)
        
        #pullTriggerDown = False  # Reset the trigger after it has been pulled
        
        msg = visual.TextStim(win, "+", height = 50)
        for frame in range(2):
            if frame == 1:
                win.callOnFlip(setParallelData, 200)
                pullTriggerDown = True
            else:
                win.callOnFlip(setParallelData, 0)
                pullTriggerDown = False
            msg.draw()
            win.flip()
        response = get_response(msg)
        setParallelData(response+11)
        
        

        
    logfile = logfile.append({
    'trial_number': trial_number,
    'response': response,
    'trial_type': df.iloc[i,5],
    'music_condition': df.iloc[i,4],
    'stim_condition': df.iloc[i,2]}, ignore_index = True)
    

logfile.to_csv(logfile_name)