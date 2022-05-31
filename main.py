from rich.prompt import Prompt
from enum import Enum
from operator import contains
from random import choice
import os
from time import sleep, time
import VirtualPainter
from lxml import etree


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


def parse_hocr(fp):
    character_confidence = []
    character = []
    has_identified_char = False

    with open(fp, 'r') as f:
        doc = etree.parse(f)

        for path in doc.xpath('//*'):
            if 'ocrx_cinfo' in path.values():
                conf = [x for x in path.values() if 'x_conf' in x][0]
                character_confidence.append(conf.split('x_conf ')[1])
                character.append(path.text)
                has_identified_char = True

    if not has_identified_char:
        character.append(0)
        character_confidence.append(0)

    return(character[0], character_confidence[0])


def draw_letter():
    VirtualPainter.painter()
    # Show canvas to user?


def classify_letter():
    # Gets image, returns character
    # Configured to ony recognize danish characters -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzøåæABCDEFGHIJKLMNOPQRSTUVWXYZØÅÆ
    stream = os.popen(
        'tesseract letter.jpg outputbase -l dan+eng --oem 1 --psm 10 -c hocr_char_boxes=1 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzøåæABCDEFGHIJKLMNOPQRSTUVWXYZØÅÆ hocr')
    stream.close()
    character, character_confidence = parse_hocr('outputbase.hocr')

    # Confirm with the user if the confidence is low
    if float(character_confidence) > 97:
        return character.capitalize()
    else:
        print("Did you draw an " + character.capitalize() + " ?")
        return Prompt.ask("Please type the letter you drew").upper()[0]

    # output = stream.read().splitlines()[0]
    # output = output.replace('\n', '')
    # print("The letter is: " + output.capitalize())
    # return output.capitalize()


def draw(difficulty):
    letters = []
    # Draw a letter for each character
    for i in range(difficulty):
        draw_letter()
        classified_letter = classify_letter()
        print(classified_letter)

        letters.append(classified_letter)
        print(letters)
        # Make sure it is the right capitalization

        # Confirm the letter with the user ???

        print("Waiting 2 seconds...")
        sleep(2)

    # Put the letters together in a word
    guess = "".join([str(letter) for letter in letters])
    return guess


class Game:

    def __init__(self, game_difficulty=Difficulty.INTERMEDIATE, game_mode=Mode.QUICK_GAME):
        self.difficulty = game_difficulty
        self.word_list = []
        self.guessed_list = []
        self.game_mode = game_mode
        self.word_to_guess = ""
        self.time_played = 0
        self.player = ""
        self.attempts = 6
        self.current_attempt = 0

    def start_game(self, player='Anonymous'):
        self.player = player

        print("Hello " + player + ", the game is about to start")
        # Get random word from the selected difficulty level wordlist
        self.word_to_guess = choice(self.word_list)
        print("The word to guess is ", self.word_to_guess)
        self.time_played = time()

        while self.current_attempt < self.attempts:
            print("Guess the word! (" + str(self.attempts -
                  self.current_attempt) + " attempts remaining)")

            if self.guess_word(draw(self.difficulty.value)) == "CORRECT":
                break
            else:
                self.current_attempt += 1

        # Stop game after win or too many atempts
        self.stop_game()

    def stop_game(self):
        # Stop timer
        self.time_played = time() - self.time_played
        # Show word
        print("The word was " + self.word_to_guess)

        # Send results
        print("It took you: " + str(self.time_played.__ceil__()) +
              " seconds and " + str(self.current_attempt) + " attempts")

        # Show pop-up with results, ask to play again or go to menu [if win, offer next level, if lose, keep same level]

    def set_difficulty(self,  difficulty, attempts=6):
        self.difficulty = difficulty
        self.attempts = attempts
        # self.word_list = ["HELLO, AUDIO, VIDEO, TRAIN, START, BEGIN, TRACE, TRUMP"]
        self.word_list = ["NOP", "PON", "BON", "DON", "MOD"]

        # Display menu with game options

    def guess_word(self, guess):
        print("YOUR GUESS: " + guess)

        # Check if is the right word
        if (guess == self.word_to_guess):
            print("Congratulations you guessed the word ")

            return "CORRECT"
        else:
            # Check if word has the correct amount of letters
            if len(guess) == self.difficulty.value:
                # Check if the word is in our dictionary
                if contains(self.word_list, guess):
                    # Check if that word has already been usef
                    if not contains(self.guessed_list, guess):
                        # Add new guess to the list
                        self.guessed_list.append(guess)
                        # Check the letters
                        for i, letter in enumerate(guess):
                            if self.word_to_guess[i] == guess[i]:
                                # Letter is in the correct place
                                print("Letter "+guess[i] +
                                      " is in the correct place")

                            elif letter in self.word_to_guess:
                                # Letter is in the word but in the wrong place
                                print(
                                    "Letter "+guess[i] + " is in the word but in the wrong place")
                            else:
                                # Letter is not in the word
                                print(
                                    "Letter "+guess[i] + " is not in the worc")

                    else:
                        print("You have already used " +
                              guess + ", try another word")

                else:
                    print("The word " + guess +
                          " is not in the dictionary, try another word")

            else:
                print("The word " + guess + " needs to have " +
                      str(self.difficulty.value) + " letters")
                return "INCORRECT"


if __name__ == '__main__':
    print("wordle")
    game = Game()
    game.set_difficulty(Difficulty.BEGGINER)
    game.start_game('Lucia')
