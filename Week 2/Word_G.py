import random
import string


class WordBank:
    """Responsible for storing the pool of possible words and picking one."""

    DEFAULT_WORDS = [
        "python", "variable", "function", "iterator", "notebook",
        "pipeline", "dataset", "computer", "research", "analytics"
    ]

    def __init__(self, words=None):
        # Allow custom word lists to be injected, otherwise use the default pool
        self.words = words if words is not None else self.DEFAULT_WORDS

    def get_random_word(self):
        # Pick and return a random word from the bank
        return random.choice(self.words)


class Board:
    """Keeps track of the secret word and which letters have been revealed."""

    def __init__(self, word):
        self.word = word
        # One blank per letter in the word, e.g. "cat" -> ["_", "_", "_"]
        self.blanks = ["_" for _ in word]

    def reveal_letter(self, letter):
        """
        Fill in every occurrence of `letter` in the word.
        Returns True if the letter was found at least once.
        """
        found_any = False
        for i, ch in enumerate(self.word):
            if ch == letter and self.blanks[i] == "_":
                self.blanks[i] = letter
                found_any = True
        return found_any

    def is_complete(self):
        # The word is fully guessed once there are no more blanks left
        return "_" not in self.blanks

    def __str__(self):
        # Nicely formatted string like "_ a _ _ o n" for printing
        return " ".join(self.blanks)


class Player:
    """Handles player input and keeps track of letters already tried."""

    def __init__(self):
        self.used_letters = set()

    def prompt_for_letter(self):
        """
        Keep asking until the player enters a valid, unused single letter.
        Returns the accepted letter and records it as used.
        """
        while True:
            guess = input("Guess a letter: ").strip().lower()
            if len(guess) != 1 or guess not in string.ascii_lowercase:
                print(" → Please enter a single A-Z letter.")
                continue
            if guess in self.used_letters:
                print(" → You already tried that letter.")
                continue
            self.used_letters.add(guess)
            return guess


class WordGuessingGame:
    """Orchestrates a full game: setup, turn loop, win/lose conditions."""

    def __init__(self, max_lives=6, word_bank=None):
        self.word_bank = word_bank if word_bank is not None else WordBank()
        self.max_lives = max_lives
        self.lives = max_lives
        self.player = Player()

        # Pick the secret word and set up the board for this round
        secret = self.word_bank.get_random_word()
        self.board = Board(secret)

    def _print_intro(self):
        print("\nWelcome to Word Guessing!")
        print(f"The word has {len(self.board.word)} letters.")
        print(self.board)

    def _handle_guess(self, guess):
        """Process a single guessed letter and update game state accordingly."""
        if self.board.reveal_letter(guess):
            print("\n Well done, Nice job! You found a letter.")
            print(self.board)
        else:
            self.lives -= 1
            print(f"\nNope. You lose a life. Lives left: {self.lives}")
            print(self.board)

    def _is_won(self):
        return self.board.is_complete()

    def _is_lost(self):
        return self.lives <= 0

    def _print_win(self):
        print("\n Congratulation! You guessed the word!")
        print(f"Word: {self.board.word}")
        print("GAME OVER")

    def _print_loss(self):
        print("\n Out of lives & Sad story!")
        print(f"The word was: {self.board.word}")
        print("GAME OVER")

    def play(self):
        """Main game loop: alternates between prompting and checking state."""
        self._print_intro()

        while True:
            guess = self.player.prompt_for_letter()
            self._handle_guess(guess)

            if self._is_won():
                self._print_win()
                break
            if self._is_lost():
                self._print_loss()
                break


if __name__ == "__main__":
    game = WordGuessingGame(max_lives=6)
    game.play()