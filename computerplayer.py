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

    def make_beginnermove(self, stack: list[int]) -> str:
        moves = self.available_moves(stack)
        stack_card = self.show_stack()
        waiting_stacks = self.show_waiting_stack()
        hand = self.show_hand()

        if moves["stack"]:
            return moves["stack"][0]

        move_length: list[dict[str, str]] = []

        for h_move in moves["hand"]:
            origin = int(h_move[2])
            length = abs(hand[origin] - stack_card)
            move_length.append({"value": str(length), "move": h_move})

        for w_move in moves["w_stack"]:
            origin = int(w_move[2])
            length = abs(waiting_stacks[origin] - stack_card)
            move_length.append({"value": str(length), "move": w_move})

        move_length = sorted(move_length, key=lambda d: d["value"])

        if move_length:
            return move_length[0]["move"]

        move_length = []

        for end_turn in moves["end_turn"]:
            origin = int(end_turn[2])
            target = int(end_turn[1])
            length = abs(hand[origin] - waiting_stacks[target])
            if waiting_stacks[target] == 0:
                length = 1
            elif hand[origin] > waiting_stacks[target]:
                length *= 2
            move_length.append({"value": str(length), "move": end_turn})

        move_length = sorted(move_length, key=lambda d: d["value"])

        if move_length:
            return move_length[0]["move"]

        return "exit"
