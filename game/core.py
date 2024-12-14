import random
from pathlib import Path


class GeoWar:
    def __init__(self):
        self.wait_for_input = False
        self.messages = []
        self.user_input = None
        self.total_shots = None
        self.targets = None
        self.hits = None
        self.direct_hits = None

    @staticmethod
    def description():
        yield "DO YOU WANT A DESCRIPTION OF THE GAME? (1=YES, 0=NO) "
        response = input()
        if response == "1":
            readme = Path('../README.md').read_text()
            yield readme

    def on_start_game(self):
        self.targets = [random.randint(1, 89) for _ in range(5)]
        self.hits = 0
        self.direct_hits = 0
        self.total_shots = 0
        self.user_input = None

    def shoot(self, angle):
        self.total_shots += 1

        if angle in self.targets:
            self.hits += 1
            self.direct_hits += 1

            self.targets.remove(angle)
            yield f"..CONGRATULATIONS..   A HIT."
            return

        for target in self.targets:
            if target - 3 <= angle <= target + 3:
                self.hits += 1
                yield "A NEAR HIT. ENEMY HAS RELOCATED."
                return
        yield "NO LUCK -- TRY AGAIN."

    def get_user_message(self, message):
        self.user_input = message
        self.wait_for_input = False

    def wait_user_input(self):
        self.user_input = None
        while self.user_input is None:
            yield None
        yield self.user_input

    def yield_play(self):

        while True:
            self.on_start_game()
            self.description()

            while self.user_input != 'y':
                yield "READY FOR A NEW GAME?"

                self.wait_for_input = True
                yield self.get_user_message

            while self.targets:
                try:
                    yield "ENTER DEGREE OF SHOT"

                    self.wait_for_input = True
                    yield self.get_user_message

                    angle = int(self.user_input)
                    if angle < 1 or angle > 90:
                        yield "ANGLE MUST BE BETWEEN 1 AND 90."
                        continue
                    shot_generator = self.shoot(angle)
                    yield next(shot_generator)
                except ValueError:
                    yield "PLEASE ENTER A VALID INTEGER."

            yield f"GAME TOTALS: {self.hits} HITS AND {self.direct_hits} DIRECT HITS ON {self.total_shots} SHOTS."

    def play(self):
        state = self.yield_play()
        while True:
            current_state = next(state)
            if type(current_state) is str:
                print(current_state)
            else:
                inp = input()
                current_state(inp)


if __name__ == "__main__":
    GeoWar().play()
