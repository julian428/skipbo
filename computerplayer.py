from random import randint
from player import Player


class ComputerPlayer(Player):
    def __init__(self, stack: list[int], name: str = "Computer") -> None:
        super().__init__(stack, name)

    def make_dumbmove(self, stack: list[int]) -> str:
        moves = self.available_moves(stack)

        if moves["stack"]:
            index = 0
            if len(moves["stack"]) > 0:
                index = randint(0, len(moves["stack"]) - 1)
            return moves["stack"][index]

        elif moves["hand"]:
            index = 0
            if len(moves["hand"]) > 0:
                index = randint(0, len(moves["hand"]) - 1)
            return moves["hand"][index]

        elif moves["w_stack"]:
            index = 0
            if len(moves["stack"]) > 0:
                index = randint(0, len(moves["w_stack"]) - 1)
            return moves["w_stack"][index]

        index = 0
        if len(moves["end_turn"]) > 0:
            index = randint(0, len(moves["end_turn"]) - 1)
        if not moves["end_turn"]:
            return "exit"
        return moves["end_turn"][index]
