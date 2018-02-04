import os
from psychopy import visual, data, logging, event, core
from numpy import random
from config_management import config_manager
import IST_objects
from utils import load_files_by_ext


def main():
    config = config_manager.ConfigManager('IST_memory.config')
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
    filename = config.config.get('log_location') + os.sep + '{}_{}_{}_IST_memory'.format(participant.id, participant.session,data.getDateStr()) + '.csv'
    file_writer = open(filename, 'a')
    file_writer.write(
        'participant_id, session, trial_number, global_time, picture, old/new, time_of_choice, confidence, time_con_rating,\n')

    endExpNow = False

    # set up display
    win = visual.Window(size=(1440, 900), fullscr=True, screen=0,
                        allowGUI=False, allowStencil=False, monitor='testMonitor',
                        color='black', colorSpace='rgb', blendMode='avg', useFBO=True)

    # set up directions
    old_new = visual.TextStim(win, text=u"Old/New", pos=(0, -0.77), bold=True)
    confidence_rating = visual.TextStim(win, text=u"1   2   3", pos=(0, 0), height=0.3, bold=True)
    confidence_text = visual.TextStim(win, text=u"low                     high", pos=(0, -0.3), height=0.1, bold=True)

    # collect all images
    all_indoor_imgs = load_files_by_ext(config.config.get('indoor_image_path'), config.config.get('image_file_ext'))
    all_outdoor_imgs = load_files_by_ext(config.config.get('outdoor_image_path'), config.config.get('image_file_ext'))
    all_living_imgs = load_files_by_ext(config.config.get('living_image_path'), config.config.get('image_file_ext'))
    all_nonliving_imgs = load_files_by_ext(config.config.get('non_living_image_path'), config.config.get('image_file_ext'))

    total_images = all_indoor_imgs + all_outdoor_imgs + all_living_imgs + all_nonliving_imgs

    # shuffle and randomize all images
    random.shuffle(total_images)

    num_of_images = 8 #len(total_images)

    for x in range(num_of_images):
        pic = total_images[x]
        visual_select = visual.ImageStim(win, image=pic)
        visual_select.draw()
        old_new.draw()
        win.flip()
        trial_clock.reset(0)
        status_in = event.waitKeys(maxWait=10, keyList=['left','right'], modifiers=False, timeStamped=trial_clock)
        confidence_rating.draw()
        confidence_text.draw()
        win.flip()
        trial_clock.reset(0)
        conf_in = event.waitKeys(maxWait=10, keyList=['left','down','right'], modifiers=False, timeStamped=trial_clock)
        core.wait(0.5)
        trial = IST_objects.ConfidenceTrial(x+1, globalClock.getTime(), pic, status_in, conf_in)
        file_writer.write(participant.csv_format() + trial.csv_format()+'\n')

    print'!!!!!!!!!!!!!!!!!!!!!!!!!'
    file_writer.close()


if __name__ == '__main__':
    main()

