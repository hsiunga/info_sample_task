import os
from psychopy import visual, data, logging, event, core
from numpy import random
from config_management import config_manager
import IST_objects


config = config_manager.ConfigManager('IST_memory.config')


def load_images(path):
    ret_list = []
    img_list = os.listdir(path)
    for image in img_list:
        if image.endswith(config.config.get('image_file_ext')):
            ret_list.append(path + os.sep + image)
    return ret_list


def main():
    # Store info about the experiment session
    participant_no = raw_input('Participant Number:')
    session_no = raw_input('Session Number:')
    raw_input('Press enter when you are ready to start the task.')
    participant = IST_objects.Participant(participant_no, session_no)

    # set up logging information
    globalClock = core.Clock()  # if this isn't provided the log times will reflect secs since python started
    logging.setDefaultClock(globalClock)
    # set up file creation
    filename = config.config.get('log_location') + os.sep + '{}_{}_{}_IST_memory'.format(participant.id, participant.session,data.getDateStr()) + '.csv'
    file_writer = open(filename, 'a')
    file_writer.write(
        'participant_id, session, trial_number, picture, old/new, time_of_choice, confidence, time_con_rating,\n')

    endExpNow = False

    # set up display
    win = visual.Window(size=(1440, 900), fullscr=True, screen=0,
                        allowGUI=False, allowStencil=False, monitor='testMonitor',
                        color='black', colorSpace='rgb', blendMode='avg', useFBO=True)

    # set up directions
    old_new = visual.TextStim(win, text=u"Old/New", pos=(0, -0.77), bold=True)
    confidence_rating = visual.TextStim(win, text=u"1   2   3", pos=(0, 0), height=0.3, bold=True)
    confidence_text = visual.TextStim(win, text=u"low                    high", pos=(0, -0.3), height=0.1, bold=True)

    # collect all images
    all_indoor_imgs = load_images(config.config.get('indoor_image_path'))
    all_outdoor_imgs = load_images(config.config.get('outdoor_image_path'))
    # all_living_imgs = load_images(config.config.get('living_image_path'))
    # all_nonliving_imgs = load_images(config.config.get('non_living_image_path'))

    total_images = all_indoor_imgs + all_outdoor_imgs #+ all_living_imgs + all_nonliving_imgs

    # shuffle and randomize all images
    random_total_images = random.shuffle(total_images)

    num_of_images = 3 #len(total_images)


    for x in range(num_of_images):
        pic = total_images[x]
        visual_select = visual.ImageStim(win, image=pic)
        visual_select.draw()
        old_new.draw()
        win.flip()
        status_in = event.waitKeys(maxWait=10, keyList=['left','right'], modifiers=False, timeStamped=globalClock)
        confidence_rating.draw()
        confidence_text.draw()
        win.flip()
        conf_in = event.waitKeys(maxWait=10, keyList=['left','down','right'], modifiers=False, timeStamped=globalClock)
        core.wait(0.5)
        trial = IST_objects.ConfidenceTrial(x+1, pic, status_in, conf_in)
        file_writer.write(participant.csv_format() + trial.csv_format()+'\n')

    print'!!!!!!!!!!!!!!!!!!!!!!!!!'
    file_writer.close()


if __name__ == '__main__':
    main()

