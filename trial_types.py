pic_cat = 'category_of_pic'
distribution_type = 'probability_dist'
reward = 'reward_type'
majority_cat = 'majority_cat'

indoor_outdoor_cat = 'ioc'
living_nonliving_cat = 'lnc'
easy_dist = 0.60
hard_dist = 0.60
high_reward = 5
low_reward = 1
indoor = 'indoor'
outdoor = 'outdoor'
living = 'living'
nonliving = 'nonliving'

trial_types = {}

trial_types[1] = {pic_cat: indoor_outdoor_cat, distribution_type: easy_dist, reward: high_reward, majority_cat: indoor}
trial_types[2] = {pic_cat: indoor_outdoor_cat, distribution_type: hard_dist, reward: high_reward, majority_cat: indoor}
trial_types[3] = {pic_cat: indoor_outdoor_cat, distribution_type: easy_dist, reward: low_reward, majority_cat: indoor}
trial_types[4] = {pic_cat: indoor_outdoor_cat, distribution_type: hard_dist, reward: low_reward, majority_cat: indoor}
trial_types[5] = {pic_cat: indoor_outdoor_cat, distribution_type: easy_dist, reward: high_reward, majority_cat: outdoor}
trial_types[6] = {pic_cat: indoor_outdoor_cat, distribution_type: hard_dist, reward: high_reward, majority_cat: outdoor}
trial_types[7] = {pic_cat: indoor_outdoor_cat, distribution_type: easy_dist, reward: low_reward, majority_cat: outdoor}
trial_types[8] = {pic_cat: indoor_outdoor_cat, distribution_type: hard_dist, reward: low_reward, majority_cat: outdoor}
trial_types[9] = {pic_cat: living_nonliving_cat, distribution_type: easy_dist, reward: high_reward, majority_cat: living}
trial_types[10] = {pic_cat: living_nonliving_cat, distribution_type: hard_dist, reward: high_reward, majority_cat: living}
trial_types[11] = {pic_cat: living_nonliving_cat, distribution_type: easy_dist, reward: low_reward, majority_cat: living}
trial_types[12] = {pic_cat: living_nonliving_cat, distribution_type: hard_dist, reward: low_reward, majority_cat: living}
trial_types[13] = {pic_cat: living_nonliving_cat, distribution_type: easy_dist, reward: high_reward, majority_cat: nonliving}
trial_types[14] = {pic_cat: living_nonliving_cat, distribution_type: hard_dist, reward: high_reward, majority_cat: nonliving}
trial_types[15] = {pic_cat: living_nonliving_cat, distribution_type: easy_dist, reward: low_reward, majority_cat: nonliving}
trial_types[16] = {pic_cat: living_nonliving_cat, distribution_type: hard_dist, reward: low_reward, majority_cat: nonliving}

minority_category = {indoor:outdoor, outdoor:indoor, living:nonliving, nonliving:living}
