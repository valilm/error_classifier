import math
import num2words
from num2words import num2words

########## functions for robot error prediction ["robot", "child_task"]

def number_in_words(number):
    return num2words(number, lang='nl')


def similarity_start(correct_answer, processed_answer):
    """
    similarity_start returns the similarity score of the beginning of correct_answer and processed_answer

    :param correct_answer (int): the correct answer of the multiplication problem
    :param processed_answer (int): the answer processed by the robot
    :return: similarity_score (float): percentage of similarity 
    """ 
    n = min(len(correct_answer), len(processed_answer))
    for i in range(n):
        #print(i)
        if correct_answer[i] != processed_answer[i]:
            return i / n
        
    # score should be 1 only if the processed answer is a subset of the correct_answer, not the other way around
    # because it matters which of the numbers is the given answer by the child, if the child said 250 
    # but the answer was 150, then it was not the robots fault
    if(len(processed_answer) <= len(correct_answer)): 
        return n / min(len(correct_answer), len(processed_answer))
    else:
        return 0

    
def similarity_end(correct_answer, processed_answer):
    """
    similarity_end returns the similarity score of the end of correct_answer and processed_answer

    :param correct_answer (int): the correct answer of the multiplication problem
    :param processed_answer (int): the answer processed by the robot
    :return: similarity_score (float): percentage of similarity 
    """ 
    n = min(len(correct_answer), len(processed_answer))
    similarity_score = 0
    for i in range(1, n+1):
        if correct_answer[-i] != processed_answer[-i]:
            similarity_score = (i-1)/n
            return(similarity_score)
    if(len(processed_answer) <= len(correct_answer)):
        return n / min(len(correct_answer), len(processed_answer))
    else:
        return 0


    
def is_there_variation(number):
    """
    is_there_variation checks if the given number has two ways of being outspoken such as 1200 
    --> 'duizendtweehonderd' AND 'twaalfhonderd'

    :param number (int): any number
    :return: True/False (bool): True if number has different ways to be said
    """ 
    if number >= 1100 and number <= 9900 and (number % 100) == 0 and (number % 1000) != 0:
        return True
    else:
        return False
    

def get_variation(number):
    """
    get_variation returns the alternative way of saying a number in dutch, if there is any
    1200 --> 'duizendtweehonderd' AND 'twaalfhonderd'

    :param number (int): any number (e.g., 1200)
    :return: spoken_variation (str): (e.g, 'twaalfhonderd')
    """ 
    spoken_variation=""
    if is_there_variation(number):
        first_part = number_in_words(number//100)
        spoken_variation = first_part + "honderd"
        
    return spoken_variation


def check_robot_error(correct_answer, processed_answer):
    """
    check_robot_error checks if it is likely an error related to the robot, or in particular to speech recognition error

    :param correct_answer (int): the correct solution of the multiplication problem
    :para processed_answer (int): the answer processed by the robot
    :return: True/False (bool): returns true if it is a robot error
    """ 

    correct_answer_str = number_in_words(correct_answer)
    processed_answer_str = number_in_words(processed_answer)
    sim_start = similarity_start(correct_answer_str, processed_answer_str)
    sim_end = similarity_end(correct_answer_str, processed_answer_str)
    
    if is_there_variation(correct_answer):
        variation_correct = get_variation(correct_answer)
        if sim_start != 1:
            sim_start = similarity_start(variation_correct, processed_answer_str)
        if sim_end != 1:
            sim_end = similarity_end(variation_correct, processed_answer_str)
        
    elif is_there_variation(processed_answer):
        variation_given = get_variation(processed_answer)
        if sim_start != 1:
            sim_start = similarity_start(correct_answer_str, variation_given)
        if sim_start != 1:
            sim_end = similarity_end(correct_answer_str, variation_given)
        

    if sim_start == 1 or sim_end == 1:
        return True
    else:
        return False
    
########## functions for child error prediction

def check_child_error(correct_answer, processed_answer):
    """
    check_child_error checks if it is likely an error related to the child, or in particular to child competence
    so far we assume it is child related for cases in which the child does not provide any answer, because the child 
    did not try to solve it, of course that could also be as the task was way to difficult and needs to be discussed

    :param correct_answer (int): the correct solution of the multiplication problem
    :para processed_answer (int): the answer processed by the robot
    :return: True/False (bool): returns true if it is a child related error
    """ 
    # if the processed answer is -1 that no answer was submitted, either the child pushed the purple foot 
    # for "i don't know the answer" or waited to long to answer and pushed the purple foot when the robot asked for the answer
    if processed_answer == -1:
        return True
    else:
        return False    
    
    


############### functions for within task error prediction

def check_added_zero(correct_answer, given_answer):
    """
    check_added_zero checks if the given answer was just having too many zeros

    :param correct_answer (int): the correct answer of the multiplication problem
    :param given_answer (int): the given answer by the child
    :return: True/False
    """ 
    if given_answer > correct_answer and correct_answer != 0:
        if math.log10(given_answer/correct_answer).is_integer():
            return True
        
    return False
    
    
def check_missing_zero(correct_answer, given_answer):
    """
    check_missing_zero checks if the given answer was just missing one ore more zeros

    :param correct_answer (int): the correct answer of the multiplication problem
    :param given_answer (int): the given answer by the child
    :return: True/False
    """ 
    if given_answer < correct_answer and given_answer != 0:
        if math.log10(correct_answer/given_answer).is_integer():
            return True
        
    return False
    


def check_number_twist(correct_answer, given_answer):
    """
    check_number_twist checks if there are two numbers twisted in the given_answer

    :param correct_answer (int): the correct answer of the multiplication problem
    :param given_answer (int): the given answer by the child
    :return: True/False
    """ 
    # Convert the numbers to strings
    given_answer_str = str(given_answer)
    correct_answer_str = str(correct_answer)

    # Check if the lengths of the numbers are the same
    if len(given_answer_str) == len(correct_answer_str):
        # Check if the digits are the same, but possibly in a different order
        if sorted(given_answer_str) == sorted(correct_answer_str):
            return True

    return False


def check_missing_addition(sum_left, sum_right, given_answer):
    """
    check_missing_addtition checks if there are two numbers twisted in the given_answer

    :param sum_left (int): multiplier
    :param sum_right (int): multiplicant 
    :param given_answer (int): the given answer by the child
    :return: True/False
    """ 
    correct_answer = sum_left*sum_right

    if given_answer < correct_answer:
        if (given_answer % sum_right) == 0:
            return True

    return False


def check_added_addition(sum_left, sum_right, given_answer):
    """
    check_added_addtition checks if 

    :param sum_left (int): multiplier
    :param sum_right (int): multiplicant 
    :param given_answer (int): the given answer by the child
    :return: True/False
    """ 
    correct_answer = sum_left*sum_right

    if given_answer > correct_answer:
        if (given_answer % sum_right) == 0:
            return True

    return False


# Check if the correct and given answer differ in only one digit
def check_one_digit(correct_answer, given_answer):
    """
    check_one_digit 

    :param correct_answer(int): the correct answer of the multiplication problem
    :param given_answer (int): the given answer by the child
    :return: True/False
    """ 
    correct_answer_str = str(correct_answer)
    given_answer_str = str(given_answer)

    # Check if the numbers have the same length
    if len(correct_answer_str) != len(given_answer_str):
        return False

    differing_digit_count = 0

    # Compare the digits at corresponding positions
    for digit1, digit2 in zip(correct_answer_str , given_answer_str):
        if digit1 != digit2:
            differing_digit_count += 1
            if differing_digit_count > 1:
                return False

    # Return True if only one differing digit found
    return differing_digit_count == 1



def predict_task_error_8(row):
    """
    predict_task_error_8 predicts the type of task related error or 'no_class' if none of the classes fit the problem

    :param row(int): the row of the data frame
    :return: one of 8 classes (str): ['child_competence', 'added_zero', 'missing_zero', 
    'number_twist', 'missing_addition', 'added_addition', 'one_digit', 'no_class']
    """ 
    sum_left = row['sum_left']
    sum_right = row['sum_right']
    correct_answer = row['sum_answer']
    given_answer = row['given_answer']
    
    if given_answer == -1:
        return 'child_competence'
    elif check_added_zero(correct_answer, given_answer):
        return 'added_zero'
    elif check_missing_zero(correct_answer, given_answer):
        return 'missing_zero'
    elif check_number_twist(correct_answer, given_answer):
        return 'number_twist'
    elif check_missing_addition(sum_left, sum_right, given_answer):
        return 'missing_addition'
    elif check_added_addition(sum_left, sum_right, given_answer):
        return 'added_addition'
    elif check_one_digit(correct_answer, given_answer):
        return 'one_digit'
    else:
        return 'no_class'
    
    
def predict_task_error_5(row):
    """
    predict_task_error_8 predicts the type of task related error or 'no_class' if none of the classes fit the problem

    :param row(int): the row of the data frame
    :return: one of 5 classes (str): ['child_competence', 'zero', 'number_twist', 'addition', 'one_digit', 'no_class']
    """ 
    sum_left = row['sum_left']
    sum_right = row['sum_right']
    correct_answer = row['sum_answer']
    given_answer = row['given_answer']
    
    if check_added_zero(correct_answer, given_answer) or check_missing_zero(correct_answer, given_answer):
        return 'zero'
    elif check_number_twist(correct_answer, given_answer):
        return 'number_twist'
    elif check_missing_addition(sum_left, sum_right, given_answer) or check_added_addition(sum_left, sum_right, given_answer):
        return 'addition'
    elif check_one_digit(correct_answer, given_answer):
        return 'one_digit'
    else:
        return 'no_class'
    
    
    
def check_task_error(correct_answer, processed_answer, sum_left, sum_right):
    """
    check_task_error checks if it is likely an error related to the task

    :param correct_answer (int): the correct solution of the multiplication problem (product)
    :param processed_answer (int): the answer processed by the robot
    :param sum_left (int): multiplier
    :param sum_right (int): multiplicant 
    :return: True/False (bool): returns true if it is a robot error
    """ 
    if check_added_zero(correct_answer, processed_answer):
        return True
    elif check_missing_zero(correct_answer, processed_answer):
        return True
    elif check_number_twist(correct_answer, processed_answer):
        return True
    elif check_missing_addition(sum_left, sum_right, processed_answer):
        return True
    elif check_added_addition(sum_left, sum_right, processed_answer):
        return True
    elif check_one_digit(correct_answer, processed_answer):
        return True
    else:
        return False
    
    
# function for main error prediction ["robot", "child", task"]

def predict_error_3(row):
    if row['evaluation'] == False:
        if check_child_error(row['sum_answer'], row['given_answer']):
            return 'child'
        if check_robot_error(row['sum_answer'], row['given_answer']):
            return 'robot'
        else:
            return 'task'
    else:
        return None

    
def predict_error_4(row):
    if row['evaluation'] == False:
        if check_child_error(row['sum_answer'], row['given_answer']):
            return 'child'
        if check_robot_error(row['sum_answer'], row['given_answer']):
            return 'robot'
        if check_task_error(row['sum_answer'], row['given_answer'], row['sum_left'], row['sum_right']):
            return 'task'
        else:
            return 'no_classification'
    else:
        return None
    

    
def predict_error_2(row):

    correct_answer = number_in_words(row['sum_answer'])
    processed_answer = number_in_words(row['given_answer'])
    sim_start = similarity_start(correct_answer, processed_answer)
    sim_end = similarity_end(correct_answer, processed_answer)
    
    if is_there_variation(row['sum_answer']):
        variation_correct = get_variation(row['sum_answer'])
        if sim_start != 1:
            sim_start = similarity_start(variation_correct, processed_answer)
        if sim_end != 1:
            sim_end = similarity_end(variation_correct, processed_answer)
        
    elif is_there_variation(row['given_answer']):
        variation_given = get_variation(row['given_answer'])
        if sim_start != 1:
            sim_start = similarity_start(correct_answer, variation_given)
        if sim_start != 1:
            sim_end = similarity_end(correct_answer, variation_given)
            
    # only if the processed answer matches 100% with the start or the end of correct answer --> robot fault
    if sim_start == 1 or sim_end == 1:
        return 'robot'
    else:
        return 'child_task'

#TEST
print(similarity_end('vierduizendtweehonderd','tweehonderd'))
'''
print('test number_in_words')
print(number_in_words(4200) == 'vierduizendtweehonderd')
print(number_in_words(1000) == 'duizend')
print(number_in_words(250) == 'tweehonderdvijftig')
print(number_in_words(150) == 'honderdvijftig')

print('test similarity_start')
print('check start: correct: 4200, processed: 200', similarity_start(number_in_words(4200), (number_in_words(200))) == 0)
print('check start: correct: 200, processed: 4200', similarity_start(number_in_words(200), (number_in_words(4200))) == 0)

# 320, 300 should give score of 1
print('check start: correct: 320 and processed: 300', similarity_start(number_in_words(320), (number_in_words(300))) == 1)
print('check start: correct: 300 and processed: 320', similarity_start(number_in_words(300), (number_in_words(320))) == 0)
# !! as 4200 can be said as tweeenviertighondernd, this should not be 1!!
print('check start: correct: 4200 and processed: 42', similarity_start(number_in_words(4200), (number_in_words(42))) == 0)

print('test similarity_end')
print('check end: correct 4200 and processed 200', similarity_end(number_in_words(4200), (number_in_words(200))) == 1)
print('check end: correct 250 and processed 150', similarity_end(number_in_words(250), (number_in_words(150))) == 1)
print('check end: correct 150 and processed 250', similarity_end(number_in_words(150), (number_in_words(250))) == 0)

print('test get_variation')
print(get_variation(1200) == 'twaalfhonderd')
print(get_variation(5300) == 'drieënvijftighonderd')



print('test check_task_error')
print(check_task_error(270, 27, 9, 30) == True)
print(check_task_error(400, 100, 5, 80) == True)
print(check_task_error(13600,1350,17,800) == False)
print(check_task_error(144,20,8,18) == False)


print("Test check_added_zero")
print(check_added_zero(1000, 10000) == True)
print(check_added_zero(40, 40000) == True)
print(check_added_zero(10000, 100) == False)   
print(check_added_zero(40, 4002) == False) 

print("Test check_missing_zero")
print(check_missing_zero(1000, 10000) == False)
print(check_missing_zero(40, 40000) == False)
print(check_missing_zero(10000, 100) == True)
print(check_missing_zero(300, 3) == True)   
print(check_missing_zero(40, 4002) == False)  

print("Test check_number_twist")
print(check_number_twist(243, 234) == True)
print(check_number_twist(542, 426) == False)

print(check_missing_addition(8, 300, 2100) == True)
print(check_missing_addition(8, 300, 2200) == False)

# Test
print(check_added_addition(8, 300, 2700) == True)
print(check_added_addition(8, 300, 2100) == False)
print(check_added_addition(8, 300, 2200) == False)

# Test
print(check_one_digit(1400, 1300) == True)
print(check_one_digit(640, 610) == True)
print(check_one_digit(540, 450) == False)
'''