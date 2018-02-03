#!/usr/bin/env python2
#psychopy version v1.85.2

# memory test for the information sampling using pictures
# created 01/21/2018 by AH lasted edited 02/04/2018 by AH

import os
import sys
from psychopy import visual, data, logging, event, core, gui
from numpy import random
import glob
from PIL import Image

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding()) + '/'
os.chdir(_thisDir)
print _thisDir

# Store info about the experiment session
expName = 'IS_memory.py'
expInfo = {'participant':'', 'session':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

#set up file creation
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date']) + '.csv'
file = open(filename, 'a')
file.write("participant_id, " + "session," + "trial_number, " + "picture, " + "old/new, " + "time_of_choice, " + "confidence, " + "time_con_rating, " + "\n")

def add_data_to_file():
    file.write(expInfo['participant'] + ", " + expInfo['session'] + ", " + str(x) + ", ")

#set up logging information
globalClock = core.Clock()  # if this isn't provided the log times will reflect secs since python started
logging.setDefaultClock(globalClock)

#logFile = logging.LogFile(filename+'.log', filemode='a', level=logging.EXP)
#logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False
#--------------------Start Code--------------------------

#set up display
win = visual.Window(size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,monitor='testMonitor',
    color='black', colorSpace='rgb', blendMode='avg', useFBO=True)

#set up directions
old_new = visual.TextStim(win, text=u"Old/New", pos=(0,-0.77), bold=True)
confidence_rating = visual.TextStim(win, text=u"1   2   3", pos=(0,0), height=0.3, bold=True)
confidence_text = visual.TextStim(win, text=u"low                    high", pos=(0,-0.3), height=0.1, bold=True)

#image pathways
image_path_indoor = 'images/indoor_resized/'
image_path_outdoor = 'images/outdoor_resized/'
image_path_living = 'images/living_resized/'
image_path_nonliving = 'images/nonliving_resized/'

path_indoor = _thisDir + image_path_indoor
path_outdoor = _thisDir + image_path_outdoor
path_living = _thisDir + image_path_living
path_nonliving = _thisDir + image_path_nonliving

#load all images 
def loadindoorImages(path_indoor):
    indoor_img_list = os.listdir(image_path_indoor)
    loadindoorImages = []
    for image in indoor_img_list:
        if image.endswith('.jpg'):
            loadindoorImages.append(path_indoor + image)
    return loadindoorImages

def loadoutdoorImages(path_outdoor):
    outdoor_img_list = os.listdir(image_path_outdoor)
    loadoutdoorImages = []
    for image in outdoor_img_list:
        if image.endswith('.jpg'):
            loadoutdoorImages.append(path_outdoor + image)
    return loadoutdoorImages

def loadlivingImages(path_living):
    living_img_list = os.listdir(image_path_living)
    loadlivingImages = []
    for image in living_img_list:
        if image.endswith('.jpg'):
            loadlivingImages.append(path_living + image)
    return loadlivingImages

def loadnonlivingImages(path_nonliving):
    nonliving_img_list = os.listdir(image_path_nonliving)
    loadnonlivingImages = []
    for image in nonliving_img_list:
        if image.endswith('.jpg'):
            loadnonlivingImages.append(path_nonliving + image)
    return loadnonlivingImages

#collect all images
all_indoor_imgs = loadindoorImages(path_indoor)
all_outdoor_imgs = loadoutdoorImages(path_outdoor)
all_living_imgs = loadlivingImages(path_living)
all_nonliving_imgs = loadnonlivingImages(path_nonliving)

total_images = all_indoor_imgs + all_outdoor_imgs + all_living_imgs + all_nonliving_imgs

#shuffle and randomize all images
random_total_images = random.shuffle(total_images)

num_of_images = 10
#len(total_images)

#define button presses
def old_new_press():
    key_press = event.waitKeys(maxWait=10, keyList=['left','right'], modifiers=False, timeStamped=globalClock)
    if key_press != None:
        if 'left' in key_press[0]:
            file.write(',' + 'old' + ',' + str(key_press[0][1]))
        elif 'right' in key_press[0]:
            file.write(',' + 'new' + ',' + str(key_press[0][1]))
    else:
        file.write('No Selection, No Time')
    return key_press

def confidence_press():
    key_press = event.waitKeys(maxWait=10, keyList=['left','down','right'], modifiers=False, timeStamped=globalClock)
    if key_press != None:
        if "left" in key_press[0]:
            file.write(',' + '1, ' + str(key_press[0][1]) +'\n')
        elif "down" in key_press[0]:
            file.write(',' + '2, ' + str(key_press[0][1]) +'\n')
        elif "right" in key_press[0]:
            file.write(',' + '3, ' + str(key_press[0][1]) +'\n')
    else:
        file.write('No Selection, No Time\n')
    return key_press

for x in range(num_of_images):
    add_data_to_file()
    pic = total_images[x]
    visual_select = visual.ImageStim(win, image = pic)
    visual_select.draw()
    file.write(','+ pic.split(os.sep)[-1])
    old_new.draw()
    win.flip()
    old_new_press()
    confidence_rating.draw()
    confidence_text.draw()
    win.flip()
    confidence_press()
    core.wait(0.5)

print'!!!!!!!!!!!!!!!!!!!!!!!!!'


