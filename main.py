
import enum
from operator import contains
from random import choice


# GAME SETTINGS

class Difficulty(Enum):
    BEGGINER = 3
    EASY = 4
    INTERMEDIATE = 5
    ADVANCED = 6
    HARD = 7


class Mode(Enum):
    SOLO = 0
    COMPETITIVE = 1
    SOCIAL = 2
    QUICK_GAME = 3

#################


def draw_letter():
    # Show canvas to user
    pass


def classify_letter():
    # Gets image, returns character
    pass


def draw(difficulty):
    letters = []
    # Draw a letter for each character
    for i in range(difficulty):
        drawing_letter = draw_letter()
        classified_letter = classify_letter(drawing_letter)
        # Confirm the letter with the user ???
        letters.append(classified_letter)

        # Make sure it is the right capitalization

    # Put the letters together in a word
    guess = " ".join([str(letter) for letter in letters])
    return guess


class Game:

    def __init__(self, game_difficulty=Difficulty.INTERMEDIATE, game_mode=Mode.QUICK_GAME):
        self.difficulty = game_difficulty
        self.word_list
        self.guessed_list = []
        self.game_mode = game_mode
        self.word_to_guess
        self.time_played = 0
        self.player
        self.attempts
        self.current_attempt = 0

    def start_game(self, player='Anonymous'):
        self.player = player

        # Get random word from the selected difficulty level wordlist
        self.word_to_guess = choice(self.word_list)

        # Start timer

        while self.current_attempt < self.attempts:
            if self.guess_word(draw(self.difficulty)) == "CORRECT":
                break
            else:
                self.attempts -= 1

        # Stop game after win or too many atempts
        self.stop_game()

    def stop_game(self):
        # Stop timer

        # Show word
        print("The word was" + self.word_to_guess)

        # Send results

        # Show pop-up with results, ask to play again or go to menu [if win, offer next level, if lose, keep same level]
        pass

    def set_difficulty(self,  difficulty, attempts=6):
        self.difficulty = difficulty
        self.attempts = attempts
        self.word_list = ["HELLO, AUDIO, VIDEO, TRAIN"]
        # Display menu with game options

    def guess_word(self, guess):

        # Check if is the right word
        if (guess == self.word_list):
            print("Congratulations you guessed the word")

            return "CORRECT"
        else:
            # Check if word has the correct amount of letters
            if len(guess) == self.difficulty:
                # Check if the word is in our dictionary
                if contains(self.word_list, guess):
                    # Check if that word has already been usef
                    if contains(self.guessed_list, guess):
                        # Add new guess to the list
                        self.guessed_list.append(guess)
                        # Check the letters
                        for i, letter in enumerate(guess):
                            if self.word_to_guess[i] == guess[i]:
                                # Letter is in the correct place
                                print("Letter is in the correct place")

                            elif letter in self.word_to_guess:
                                # Letter is in the word but in the wrong place
                                print(
                                    "Letter is in the word but in the wrong place")
                            else:
                                # Letter is not in the word
                                print(
                                    "Letter is in the word but in the wrong place")

                    else:
                        print("You have already used this word, try another word")

                else:
                    print("The word is not in the dictionary, try another word")

            else:
                print("The word needs to have" + self.difficulty + "letters")
                return "INCORRECT"


if __name__ == '__main__':
    print("wordle")
    game = Game()
    game.start_game('Lucia')
