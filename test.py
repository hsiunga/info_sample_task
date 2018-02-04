# from config_management import config_manager
# import os
#
# input = 'left'
# input2 = 'right'
#
# class InputsOnPicture():
#     def __init__(self, inp):
#         self.input = inp
#         if self.input == 'left':
#             self.picture_type = 'old'
#         elif self.input == 'right':
#             self.picture_type = 'new'
#
#     def write_to_csv(self, file):
#         file.write(self)
#
#     def __str__(self):
#         return self.picture_type + ', ' + self.input
#
# a = InputsOnPicture('left')
# print(a)
# import os
# t = '/test/path/file.txt'
# print(t.split(os.sep)[-1])
#
# print(os.sep)
#
# tw = [('left', 1.124)]
# print(tw)
# print('left' in tw[0])
# print(tw[0][1])
#
# config = config_manager.ConfigManager('IST_memory.config')
# print(config.config.get('image_file_ext'))
#
#
# def load_images(path):
#     ret_list = []
#     img_list = os.listdir(path)
#     for image in img_list:
#         if image.endswith(config.config.get('image_file_ext')):
#             ret_list.append(path + os.sep + image)
#     return ret_list
#
# im_list = load_images(config.config.get('outdoor_image_path'))
# print(im_list)