import random
from collections import Counter


def main():
    total = 1000
    dist = .70
    amount_to_sample = 20
    sampled_by_user = 6
    runs_in_sim = 5000
    ones = [1 for x in range(int(total * dist))]
    zeros = [0 for x in range(int(total * (1-dist)))]
    sample_set = ones + zeros
    # t = sim(sample_set, runs_in_sim, lambda x : Counter(random.sample(x, amount_to_sample)).get(1))
    # print(t)
    t = sim(sample_set, runs_in_sim, lambda x: Counter(random.sample(x, amount_to_sample)[:sampled_by_user]).get(1))
    print(t)
    half_of_sample = int(sampled_by_user/2)
    gt_half = [x for x in t if x > half_of_sample]
    lt_half = [x for x in t if x < half_of_sample]
    half = [x for x in t if x == half_of_sample]
    print('{} trials had more than {} ones'.format(len(gt_half), half_of_sample))
    print('ending sampling here would result in {}% correct'.format(len(gt_half)/runs_in_sim*100))
    print('{} trials had less than {} ones'.format(len(lt_half), half_of_sample))
    print('{} trials had {} ones'.format(len(half), half_of_sample))


def sim(set, runs, func):
    result = []
    for x in range(runs):
        ret = func(set)
        result.append(ret if ret else 0)
    return result


if __name__ == '__main__':
    main()