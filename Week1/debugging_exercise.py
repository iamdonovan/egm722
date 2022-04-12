# import random

# pick a random number for the user to guess
rand = random.randint(0, 100)

print('Guess a number between 0 and 20.')
guess = int(input())  # number needs to be an integer

while guess != rand:
    if guess > rand:  # if the guess is too high, tell the user.
        print('Too high. Guess again.')
    else:  # if the guess is too low, tell the user.
        print('Too high. Guess again.')

    print('Enter a new guess: ')
    guess = input()

print('You got it! The number was {}'.format(rand))
