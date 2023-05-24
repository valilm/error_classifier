# error_classifier
classifies errors in child-robot interaction based on processed answer

the error classifier predicts the type of error based only on data of the mathematical task and the given answer, in this case multiplication problem. It takes the correct answer of the problem (product) and the answer that was processed by the robot and returns one of the following error types ('other_error' if none of the error types could be predicted):
- "robot_late"
- "robot_soon"
- 

Main script can be run:

python main.py 41000 41

-> returns: robot_late

Use Case: Children of elementary school solving multiplication math problems in interaction with the NAO robot
