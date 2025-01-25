# Multiplication Quiz
# Prompts the user with 10 multiplication questions, ranging from 0x0 to 9x9.
# The user gets 3 tries and 8 seconds on each question.

import random, time

total_questions = 10
correct_answers = 0

for question_number in range(total_questions):
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    print(f'Question #{question_number + 1}. {num1} * {num2} = ')
    timestamp_start = time.time()
    available_attempts = 3
    while available_attempts > 0:
        response = input()
        try:
            response = int(response)
            if time.time() - timestamp_start > 8:
                available_attempts -= 1
                print('Out of time!')
                break
            if response == num1 * num2:
                correct_answers += 1
                print('Correct!')
                break
            else:
                available_attempts -= 1
                print('Incorrect!')
        except:
            print('Incorrect!')
            available_attempts -= 1
        finally:
            time.sleep(1)

print(f'You answered correctly {correct_answers} out of {total_questions} questions.')
