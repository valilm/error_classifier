# error_classifier
classifies errors in child-robot interaction based on processed answer

Use Case: Children of elementary school solving multiplication math problems while interacting with the NAO robot. Detecting the type of error can later help to give error specific feedback in the moment, an error occurs. That also includes the ability of the robot to detect a mistake in communication, so frustration can be mitigated. 

The error classifier predicts the type of error based only on data of the mathematical task and the given answer, in this case multiplication problem. It takes the correct answer of the problem (product) and the answer that was processed by the robot and returns one of the following error types ('other_error' if none of the error types could be predicted):

robot related errors
- "robot_soon" -> speech recognition error where the child started talking too soon, so the beginning of the answer was missed (e.g, child said 42000, robot understood 1000)
- "robot_late" -> speech recognition error where the child started talking too late, so the end of the answer was missed (e.g., child said 4800, robot understood 4008

task related errors
- "task_extra_zeros" -> the answer given by the child was just off by one or more extra zeros (e.g., correct: 7000, given: 70000)
- "task_missing_zeros" -> the answer given by the child was missing some zeros (e.g., correct: 630, given: 63)
- "number_twist" -> there are exactly two digits in the (e.g., correct: 540, given: 450)

To try the classifier install requirements and run the main script:  
pip install -r requirements.txt  
python main.py <correct_answer_int> <processed_answer_int>  

example:  
python main.py 41000 41. 

-> returns: robot_late


