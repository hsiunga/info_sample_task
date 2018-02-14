import os
from trial_types import minority_category


class Participant():

    def __init__(self, id, sesh):
        self.id = id
        self.session = sesh

    def csv_format(self):
        return '{}, {}, '.format(self.id, self.session)


class SamplesInTrial():

    def __init__(self, sample_no, picture_path, dec_to_sample_time, global_picture_onset):
        self.sample_no = sample_no
        self.dec_to_sample_time = dec_to_sample_time
        assert isinstance(global_picture_onset, object)
        self.global_picture_onset = global_picture_onset
        self.picture_path = picture_path
        self.picture_name = self.picture_path.split(os.sep)[-1]
        self.image_type = self.picture_name.split('_')[0]
        self.image_judgement = None
        self.time_of_judge = None
        self.global_time_of_judgment = None

    def csv_format(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}'.format(self.sample_no, self.picture_path, self.picture_name,
                                                       self.dec_to_sample_time, self.global_picture_onset,
                                                       self.image_judgement, self.time_of_judge,
                                                       self.global_time_of_judgment)

class OverallTrial():

    def __init__(self, trial_no, global_time, category_of_pics, probability, reward_type, majority_cat):
        self.trial_no = trial_no
        self.global_time = global_time
        self.category_type = category_of_pics
        self.prob_dist = probability
        self.reward_type = reward_type
        self.majority_cat = majority_cat
        self.final_choice = None #indoor, outdoor, living, non
        self.final_choice_time = None
        self.global_final_choice_time = None
        self.samples = []
        self.majority_side = None
        self.num_of_pics_sampled = 0
        self.total_trial_time = None

    def csv_format(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '.format(self.trial_no, self.global_time, self.category_type,
                                               self.prob_dist, self.reward_type, self.majority_cat, self.final_choice,
                                                           self.final_choice_time, self.num_of_pics_sampled,
                                                                 self.global_final_choice_time, self.total_trial_time)

    def add_sample(self, sample):
        self.samples.append(sample)
        self.num_of_pics_sampled = len(self.samples)

    def set_final_choice(self, final_dir):
        if self.majority_side == final_dir:
            self.final_choice = self.majority_cat
        else:
            self.final_choice = minority_category[self.majority_cat]


class ConfidenceTrial():

    def __init__(self, trial_no, global_time, picture_path, status, confidence):
        self.trial_no = trial_no
        self.global_time = global_time
        self.picture_path = picture_path
        self.old_new = None
        self.status_input = status
        self.confidence_input = confidence
        self.picture_name = self.picture_path.split(os.sep)[-1]
        self.__parse_key_press_status()
        self.__parse_key_press_conf()

    def __parse_key_press_status(self):
        if self.status_input:
            #[(status, time)]
            self.status_time = self.status_input[0][1]
            if 'left' in self.status_input[0]:
                self.status = 'old'
            elif 'right' in self.status_input[0]:
                self.status = 'new'
        else:
            self.status = 'No Selection'
            self.status_time = 'No Time'

    def __parse_key_press_conf(self):
        if self.confidence_input:
            self.conf_time = self.confidence_input[0][1]
            if 'left' in self.confidence_input[0]:
                self.confidence = 1
            elif 'down' in self.confidence_input[0]:
                self.confidence = 2
            elif 'right' in self.confidence_input[0]:
                self.confidence = 3
        else:
            self.confidence = 'No Selection'
            self.conf_time = 'No Time'

    def csv_format(self):
        return '{}, {}, {}, {}, {}, {}, {}, {}'.format(self.trial_no, self.global_time, self.picture_name, self.old_new,
                                               self.status, self.status_time, self.confidence, self.conf_time)
