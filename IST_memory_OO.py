#!/usr/bin/env python2
#psychopy version v1.85.2

# memory test for the information sampling using pictures
# created 01/21/2018 by AH & CC lasted edited 02/13/2018 by AH

import os
from psychopy import visual, data, logging, event, core
import random
from config_management import config_manager
import IST_objects
from utils import load_files_by_ext

config = config_manager.ConfigManager('IST_memory.config')

# input subject's information sampling data and collect old images
subj_info_sample_data = 'path to info sampling data'
file_reader = open(subj_info_sample_data, 'r')
lines = file_reader.readlines()

all_old_images = []
for x in lines:
    all_old_images.append(x.split(', ')[14]) # or whatever column paths are contained in sampling task

old_images = []
for image in all_old_images:
    if image.endswith('.jpg'):
        old_images.append(image)

# collect all images and separate new from old
all_indoor_imgs = load_files_by_ext(config.get('indoor_image_path'), config.get('image_file_ext'))
all_outdoor_imgs = load_files_by_ext(config.get('outdoor_image_path'), config.get('image_file_ext'))
all_living_imgs = load_files_by_ext(config.get('living_image_path'), config.get('image_file_ext'))
all_nonliving_imgs = load_files_by_ext(config.get('non_living_image_path'), config.get('image_file_ext'))

aggregate_other_images = all_indoor_imgs + all_outdoor_imgs + all_living_imgs + all_nonliving_imgs

all_new_images = [image for image in aggregate_other_images if image not in old_images]


new_images = random.sample(all_new_images, len(old_images)/3)

# create bank of new and old pictures for memory test
total_images = old_images + new_images
random.shuffle(total_images)
num_of_images = len(total_images)


def main():
    # Store info about the experiment session
    participant_no = raw_input('Participant Number:')
    session_no = raw_input('Session Number:')
    raw_input('Press enter when you are ready to start the task.')
    participant = IST_objects.Participant(participant_no, session_no)

    # set up logging information
    globalClock = core.MonotonicClock()  # if this isn't provided the log times will reflect secs since python started
    trial_clock = core.Clock()
    logging.setDefaultClock(globalClock)
    # set up file creation
    filename = config.get('log_location') + os.sep + '{}_{}_{}_IST_memory'.format(participant.id, participant.session,
                                                                                  data.getDateStr()) + '.csv'
    file_writer = open(filename, 'a')
    file_writer.write(
        'participant_id, session, trial_number, global_time, picture, old/new, time_of_choice, confidence, '
        'time_con_rating,\n')

    endExpNow = False

    # set up display
    win = visual.Window(size=(1440, 900), fullscr=True, screen=0,
                        allowGUI=False, allowStencil=False, monitor='testMonitor',
                        color='black', colorSpace='rgb', blendMode='avg', useFBO=True)

    # set up directions
    old_new = visual.TextStim(win, text=u"Old/New", pos=(0, -0.77), bold=True)
    confidence_rating = visual.TextStim(win, text=u"1   2   3", pos=(0, 0), height=0.3, bold=True)
    confidence_text = visual.TextStim(win, text=u"low                     high", pos=(0, -0.3), height=0.1, bold=True)

    ready_screen = visual.TextStim(win, text=u"Ready?", pos=(0, 0), bold=True)
    ready_screen.draw()
    win.flip()
    event.waitKeys(maxWait=10, keyList=['space'], modifiers=False)

    for x in range(num_of_images):
        pic = total_images[x]


        visual_select = visual.ImageStim(win, image=pic)
        visual_select.draw()
        old_new.draw()
        win.flip()
        trial_clock.reset(0)
        status_in = event.waitKeys(maxWait=5, keyList=['left','right'], modifiers=False, timeStamped=trial_clock)
        confidence_rating.draw()
        confidence_text.draw()
        win.flip()
        trial_clock.reset(0)
        conf_in = event.waitKeys(maxWait=5, keyList=['left','down','right'], modifiers=False, timeStamped=trial_clock)
        blank_fixation = visual.TextStim(win, text='+', color=u'white')
        blank_fixation.draw()
        win.flip()
        core.wait(1.0)
        trial = IST_objects.ConfidenceTrial(x+1, globalClock.getTime(), pic, status_in, conf_in)
        if pic in old_images:
            trial.old_new = 'old'
        else:
            trial.old_new = 'new'
        file_writer.write(participant.csv_format() + trial.csv_format()+'\n')

    print'!!!!!!!!!!!!!!!!!!!!!!!!!'
    file_writer.close()


if __name__ == '__main__':
    main()

