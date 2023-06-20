# This is a Python script that takes sum_left (int), sum_right (int), correct_answer (int), processed_answer (int)
# and returns a list of strings containing one of the following predicted error types:
# ["robot_soon", "robot_late", "child_no_answer", "task_extra_zeros", "task_missing_zeros",

import num2words
import sys
from utils import *


def classifier(args):
    """
    classifier(args) returns the type of errors predicted based only on multiplication problem data

    :param sum_left (int): the multiplier
    :param sum_right (int): the multiplicand
    :param correct_answer (int): the correct answer of the multiplication problem (the product)
    :param processed_answer (int): the answer processed by the robot
    :return: predicted error type (str):
    """
    prediction = []
    #sum_left_int = int(args(1))
    #sum_right_int = int(args(2))
    correct_answer_int = int(args[1])
    processed_answer_int = int(args[2])

    if correct_answer_int == processed_answer_int:
        return'no_error'
    else:

    #print(correct_answer_int, type(correct_answer_int), processed_answer_int,  type(processed_answer_int))

        correct_answer_str = number_in_words(correct_answer_int)
        processed_answer_str = number_in_words(processed_answer_int)
        sim_start = similarity_start(correct_answer_str, processed_answer_str)
        sim_end = similarity_end(correct_answer_str, processed_answer_str)


        if is_there_variation(correct_answer_int):
            variation_correct = get_variation(correct_answer_int)
            if sim_start != 1:
                sim_start = similarity_start(variation_correct, processed_answer_str)
            if sim_end != 1:
                sim_end = similarity_end(variation_correct, processed_answer_str)

        elif is_there_variation(processed_answer_int):
            variation_given = get_variation(processed_answer_int)
            if sim_start != 1:
                sim_start = similarity_start(correct_answer_str, variation_given)
            if sim_start != 1:
                sim_end = similarity_end(correct_answer_str, variation_given)

        # only if the processed answer matches 100% with the start or the end of correct answer --> robot fault

        if sim_start == 1:
            # when the child was talking too late (zestigduizend --> zestig)
            # "you have to talk sooner"
            return 'robot_late'
        elif sim_end == 1:
            # when the child was talking too soon (tweeenviertighonderd --> honderd)
            # you have to wait a little longer
            return 'robot_soon'

        if sim_start == 1 or check_40_case(correct_answer_int, processed_answer_int):
            print("Oh sorry I did not fully get that. Please repeat your answer once my eyes turn green.")
            return ('robot_late')
        elif sim_end == 1:
            print("Oh sorry I did not fully get that. Please repeat your answer once my eyes turn green.")
            return('robot_soon')
        elif check_correction_trial(correct_answer_int, processed_answer_int):
            return('robot_correction')
        elif check_added_zero(correct_answer_int, processed_answer_int):
            print("You almost got it. We just need to get rid of some zeros.")
            return('task_extra_zeros')
        elif check_missing_zero(correct_answer_int, processed_answer_int):
            print("You almost got it. You are just missing some zeros.")
            return('task_missing_zeros')
        elif check_number_twist(correct_answer_int, processed_answer_int):
            print('You almost got it. You just twisted two numbers')
            return('number_twist')
        else:
            return('other_error')

    #return prediction



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result_list = classifier(sys.argv)
    print(result_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
