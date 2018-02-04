import os


class Participant():

    def __init__(self, id, sesh):
        self.id = id
        self.session = sesh

    def csv_format(self):
        return '{}, {},'.format(self.id, self.session)


class ConfidenceTrial():

    def __init__(self, trial_no, global_time, picture_path, status, confidence):
        self.trial_no = trial_no
        self.global_time = global_time
        self.picture_path = picture_path
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
        return '{}, {}, {}, {}, {}, {}, {}'.format(self.trial_no, self.global_time, self.picture_name,
                                               self.status, self.status_time, self.confidence, self.conf_time)
