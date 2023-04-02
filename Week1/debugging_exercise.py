# import random

# pick a random number for the user to guess
rand = random.randint(1, 100)

print('Guess a number between 1 and 20.')
guess = int(input())  # number needs to be an integer

while guess != rand:  # if the guess is not equal to the random number, you have to guess again
    if guess > rand:  # if the guess is too high, tell the user.
        print('Too low. Guess again.')
    else:  # if the guess is too low, tell the user.
        print('Too high. Guess again.')

    print('Enter a new guess: ')
    guess = input()

print('You got it! The number was {}'.format(rand))
