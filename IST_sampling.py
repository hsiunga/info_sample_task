import os
from psychopy import visual, data, logging, event, core
import random
from config_management import config_manager
import IST_objects
from utils import load_files_by_ext, list_sample
from trial_types import trial_types

config = config_manager.ConfigManager('IST_memory.config')

# collect all images
all_indoor_imgs = load_files_by_ext(config.get('indoor_image_path'), config.get('image_file_ext'))
all_outdoor_imgs = load_files_by_ext(config.get('outdoor_image_path'), config.get('image_file_ext'))
all_living_imgs = load_files_by_ext(config.get('living_image_path'), config.get('image_file_ext'))
all_nonliving_imgs = load_files_by_ext(config.get('non_living_image_path'), config.get('image_file_ext'))

sample_button_img = config.get('sample_button_path')
indoor_button_img = config.get('indoor_button_path')
outdoor_button_img = config.get('outdoor_button_path')
living_button_img = config.get('living_button_path')
nonliving_button_img = config.get('nonliving_button_path')
ioc_judgement_button_img = config.get('ioc_judgement_button_path')
lnc_judgement_button_img = config.get('lnc_judgement_button_path')


def identify_trial_pictures(prob_dist, majority_cat, total_samples):
    if majority_cat == 'living':
        majority_sample = get_picture_from_list(all_living_imgs, int(total_samples * prob_dist))
        minority_sample = get_picture_from_list(all_nonliving_imgs, int(total_samples * (1 - prob_dist)))
    elif majority_cat == 'nonliving':
        majority_sample = get_picture_from_list(all_nonliving_imgs, int(total_samples * prob_dist))
        minority_sample = get_picture_from_list(all_living_imgs, int(total_samples * (1 - prob_dist)))
    elif majority_cat == "indoor":
        majority_sample = get_picture_from_list(all_indoor_imgs, int(total_samples * prob_dist))
        minority_sample = get_picture_from_list(all_outdoor_imgs, int(total_samples * (1 - prob_dist)))
    else:
        # majority_cat == 'outdoor'
        majority_sample = get_picture_from_list(all_outdoor_imgs, int(total_samples * prob_dist))
        minority_sample = get_picture_from_list(all_indoor_imgs, int(total_samples * (1 - prob_dist)))

    return majority_sample + minority_sample


def get_picture_from_list(picture_list, num_of_pics):
    # sample num_of_pics from picture_list
    return list_sample(picture_list, num_of_pics, False)


def start_screen(win, cat_type, reward_type, wait=None):
    ready_screen = visual.TextStim(win, text=u"Ready?", pos=(0, 0), bold=True)
    if reward_type >= 5:
        reward = visual.TextStim(win, text=u"$5", pos=(0, -0.2), bold=True)
    else:
        reward = visual.TextStim(win, text=u"$1", pos=(0, -0.2), bold=True)
    if cat_type == 'ioc':
        cat = visual.TextStim(win, text=u"indoor v. outdoor", pos=(0, 0.2), bold=True)
    else:
        cat = visual.TextStim(win, text=u"living v. non-living", pos=(0, 0.2), bold=True)
    sample_screen(win, [ready_screen, reward, cat], wait)


def button_position():
    random.randint(1, 3)
    if random.choice == 1:
        xdelta = 0.85
    else:
        xdelta = -0.85
    return xdelta


def sample_screen(win, items, wait=None):
    for item in items:
        item.draw()
    win.flip()
    if wait:
        core.wait(wait)


def create_trial_buttons(win, majority_cat):
    sample_button = visual.ImageStim(win, image=sample_button_img, pos=(0, 0))
    xdelta = button_position()

    if majority_cat == 'indoor':
        maj_button = visual.ImageStim(win, image=indoor_button_img, pos=(xdelta, 0))
        min_button = visual.ImageStim(win, image=outdoor_button_img, pos=(-xdelta, 0))
    elif majority_cat == 'outdoor':
        maj_button = visual.ImageStim(win, image=outdoor_button_img, pos=(xdelta, 0))
        min_button = visual.ImageStim(win, image=indoor_button_img, pos=(-xdelta, 0))
    elif majority_cat == 'living':
        maj_button = visual.ImageStim(win, image=living_button_img, pos=(xdelta, 0))
        min_button = visual.ImageStim(win, image=nonliving_button_img, pos=(-xdelta, 0))
    else:  # majority_cat == 'non-living'
        maj_button = visual.ImageStim(win, image=nonliving_button_img, pos=(xdelta, 0))
        min_button = visual.ImageStim(win, image=living_button_img, pos=(-xdelta, 0))
    if xdelta < 0:
        majority_side = 'left'
    else:
        majority_side = 'right'
    return sample_button, maj_button, min_button, majority_side


def return_unused_pic(unused_pic):
    if 'indoor' in unused_pic:
        list_sample(all_indoor_imgs, 0, False, [unused_pic])
    elif 'outdoor' in unused_pic:
        list_sample(all_outdoor_imgs, 0, False, [unused_pic])
    elif 'living' in unused_pic:
        list_sample(all_living_imgs, 0, False, [unused_pic])
    elif 'nonliving' in unused_pic:
        list_sample(all_nonliving_imgs, 0, False, [unused_pic])


def main():
    # Store info about the experiment session
    participant_no = raw_input('Participant Number:')
    session_no = raw_input('Session Number:')
    raw_input('Press enter when you are ready to start the task.')
    participant = IST_objects.Participant(participant_no, session_no)

    # set up logging information
    globalClock = core.MonotonicClock()  # if this isn't provided the log times will reflect secs since python started
    trial_clock = core.Clock()
    sample_clock = core.Clock()
    logging.setDefaultClock(globalClock)

    # set up file creation
    filename = config.config.get('log_location') + os.sep + '{}_{}_{}_IST_sampling'.format(participant.id,
                                                                                           participant.session,
                                                                                           data.getDateStr()) + '.csv'
    file_writer = open(filename, 'a')
    file_writer.write('participant_id, session, trial_no, global_time, category_of_pics, probability, reward_type, '
                      'majority_cat, final_choice, final_choice_time, num_of_samples, global_final_choice_time, '
                      'total_trial_time, sample_no, picture_path, dec_to_sample_time, global_picture_onset, '
                      'image_judgement, time_of_judge, global_time_of_judge, \n')

    # set up display
    win = visual.Window(size=(1440, 900), fullscr=True, screen=0,
                        allowGUI=False, allowStencil=False, monitor='testMonitor',
                        color='black', colorSpace='rgb', blendMode='avg', useFBO=True)

    # set up directions
    judge_ioc = visual.ImageStim(win, image=ioc_judgement_button_img, pos=(0, 0))
    judge_lnc = visual.ImageStim(win, image=lnc_judgement_button_img, pos=(0, 0))

    feedback_positive = visual.TextStim(win, text=u"Successful!", pos=(0, 0), bold=True)
    feedback_negative = visual.TextStim(win, text=u"Unsuccessful!", pos=(0, 0), bold=True)

    # create fixation cross
    blank_fixation = visual.TextStim(win, text='+', color=u'white')

    # number of trials (must divide by 16 evenly)
    total_num_trials = 16
    pic_per_trial = 10

    trial_types_idx = [(x % 16) + 1 for x in range(total_num_trials)]
    random.shuffle(trial_types_idx)

    # start looping through trials
    for no, trial in enumerate(trial_types_idx):
        trial_data = trial_types.get(trial)
        trial_object = IST_objects.OverallTrial(
            no + 1, globalClock.getTime(), trial_data.get('category_of_pic'), trial_data.get('probability_dist'),
            trial_data.get('reward_type'), trial_data.get('majority_cat'))
        trial_pics = identify_trial_pictures(trial_object.prob_dist, trial_object.majority_cat, pic_per_trial)
        random.shuffle(trial_pics)

        # beginning trial from user's perspective
        trial_clock.reset()
        start_screen(win, trial_data.get('category_of_pic'), trial_data.get('reward_type'), wait=2)
        sample_button, maj_button, min_button, trial_object.majority_side = create_trial_buttons(win,
                                                                                                 trial_object.majority_cat)
        next_unseen_pic = 0

        for idx, sample_pic in enumerate(trial_pics):
            sample_screen(win, [sample_button, maj_button, min_button])
            sample_clock.reset(0)
            choice_to_sample = event.waitKeys(maxWait=10, keyList=['left', 'down', 'right'], modifiers=False,
                                              timeStamped=sample_clock)

            if 'down' in choice_to_sample[0]:
                # allocate all sample data
                sample = IST_objects.SamplesInTrial(idx + 1, sample_pic, sample_clock.getTime(), globalClock.getTime())
                visual_select = visual.ImageStim(win, image=sample_pic)
                sample_clock.reset(0)
                globalClock.getTime()
                sample_screen(win, [visual_select, maj_button, min_button], 3)
                if trial_data.get('category_of_pic') == 'ioc':
                    sample_screen(win, [visual_select, maj_button, min_button, judge_ioc])
                else:
                    sample_screen(win, [visual_select, maj_button, min_button, judge_lnc])
                image_judgement = event.waitKeys(maxWait=8, keyList=['left', 'right'], modifiers=False,
                                                 timeStamped=sample_clock)
                if image_judgement:
                    sample.image_judgement = image_judgement[0][0]
                    sample.time_of_judge = image_judgement[0][1]
                else:
                    sample.image_judgement = 'No Judgement'
                    sample.time_of_judge = 'No Time'
                sample.global_time_of_judgment = globalClock.getTime()
                trial_object.add_sample(sample)
            else:
                if 'left' in choice_to_sample[0]:
                    if trial_object.majority_side == 'left':
                        feedback = [feedback_positive]
                    else:
                        feedback = [feedback_negative]
                else:
                    if trial_object.majority_side == 'right':
                        feedback = [feedback_positive]
                    else:
                        feedback = [feedback_negative]
                sample_screen(win, feedback, 1.5)
                trial_object.set_final_choice(choice_to_sample[0][0])
                trial_object.final_choice_time = choice_to_sample[0][1]
                trial_object.global_final_choice_time = globalClock.getTime()
                trial_object.total_trial_time = trial_clock.getTime()
                next_unseen_pic = idx
                break
        for unused_pic in trial_pics[next_unseen_pic:]:
            return_unused_pic(unused_pic)
        sample_screen(win, [blank_fixation], 1.5)
        if trial_object.num_of_pics_sampled == 0:
            file_writer.write(participant.csv_format() + trial_object.csv_format() + '\n')
        else:
            for samp in trial_object.samples:
                file_writer.write(participant.csv_format() + trial_object.csv_format() + samp.csv_format() + '\n')
    file_writer.flush()
    file_writer.close()


# def test():
#     for button in all_buttons:
#         print(button)


if __name__ == '__main__':
    main()
    # test()
