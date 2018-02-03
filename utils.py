from collections import Counter
import numpy


def cross_call_replacement(func):
    """This is a decorator to be used for cross call replacements for sampling against a list.
    Essentially, if replace is False, it will cache the items that have been sampled for each call
    and these won't be passed through to the sampling functionality on subsequent calls."""
    already_pulled = []

    def inn(l, num, replace=True):
        if not replace:
            pass_list = list_diff_w_dups(l, already_pulled)
            if len(pass_list) < num:
                raise Exception('not enough remaining unique items to return a list of items that haven\'t been used already')
            rlist = func(pass_list, num, False)
            already_pulled.extend(rlist)
            return rlist
        else:
            return func(l, num, True)
    return inn


def list_diff_w_dups(list1, list2):
    count = Counter(list1)
    count.subtract(list2)
    return list(count.elements())


@cross_call_replacement
def list_sample(l, num, replace=True):
    print('remaining list {}'.format(l))
    return list(numpy.random.choice(l,num,replace))
