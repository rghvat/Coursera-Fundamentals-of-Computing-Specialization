'''
Guess the number Assignment 3
Raghav Atreya
raghavpushkalatreya@gmail.com
'''

import random
import simplegui

start_limit = 0
end_limit = 100
inp_text = None
guess = 7
number = 0

# helper function to start and restart the game
def new_game():
    '''
    # initialize global variables used in your code here

    '''
    global start_limit, end_limit, guess, number
    print('New game. Range is from 0 to', end_limit)
    print('Numer of guess remaining is ', guess)
    number = random.randint(start_limit, end_limit)


# define event handlers for control panel
def range100():
    '''This function sets the range varible to 100
        button that changes the range to [0,100) and starts a new game
    '''
    global end_limit, guess
    end_limit = 100
    guess = 7
    new_game()


def range1000():
    '''
    button that changes the range to [0,1000) and starts a new game
    this function sets the range variable to 1000 and limit to
    '''

    global end_limit, guess
    end_limit = 1000
    guess = 10
    new_game()


def input_guess(guess):
    '''
    # main game logic goes here
    # similar to binary search algo
    '''
    entered_number = inp_text.get_text()
    global guess, number

    if guess > 0:
        if int(number) == int(entered_number):
            print('Correct')
        elif int(number) > int(entered_number):
            print('Higher')
        else:
            print('Lower')
        guess -= 1
        print('Numer of guess remaining is ', guess)
    else:
        print('All try exhausted')
        print('correct answer is ', int(number))


# create frame
# (framename, width, height, controlwidth)
frame = simplegui.create_frame('Guess the Number Game', 350, 350, 100)
frame.set_canvas_background('#DEB887')

btn1 = frame.add_button('For Range 100', range100)
btn2 = frame.add_button('For Range 1000', range1000)

# input box
inp_text = frame.add_input('Enter a input', input_guess, 50)
frame.start()
# register event handlers for control elements and start frame
# call new_game
new_game()
