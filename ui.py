import os
import math

from game import Game
from player import Player


class UI:
    def __init__(self, columns) -> None:
        self.columns = columns
        self.colors = ["\033[90m", "\033[94m", "\033[92m", "\033[91m", "\033[93m"]
        self.end_color = "\033[0m"

    def draw_frame(self, game: Game, player: Player, turn: int) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"turn: {turn}".center(self.columns))
        print("\n")
        print(self.draw_cards(game.show_stack()))
        print("\n\n")
        print(f"{player.identity()}'s stack".center(self.columns))
        print(self.draw_cards([player.show_stack()]))
        print("\n")
        print(f"{player.identity()}'s waiting stack".center(self.columns))
        print(self.draw_cards(player.show_waiting_stack()))
        print("\n")
        print(f"{player.identity()}'s hand".center(self.columns))
        print(self.draw_cards(player.show_hand()))
        print("\n")
        print("0 (take from stack) 0-3 (target stack)".center(self.columns))
        print(
            "1 (take from waiting stacks) 0-3 (target stack) 0-3 (origin stack)".center(
                self.columns
            )
        )
        print(
            "2 (take from hand) 0-3 (target stack) 0-4 (origin hand index)".center(
                self.columns
            )
        )
        print(
            "3 (end turn) 0-3 (target waiting stack) 0-4 (origin hand index)".center(
                self.columns
            )
        )
        print("\n")

    def draw_cards(self, cards: list[int]) -> str:
        cards_template: list[str] = [
            "",
            "",
            "",
            "",
        ]  # [0] top  [1] padding  [2] value  [3] bottom

        for card in cards:
            color = self.colors[math.ceil(card / 4)]

            if len(cards_template[0]):
                cards_template[0] += "       "
            if len(cards_template[1]):
                cards_template[1] += "       "
            if len(cards_template[2]):
                cards_template[2] += "       "
            if len(cards_template[3]):
                cards_template[3] += "       "

            cards_template[0] += f"{color} _____ {self.end_color}"
            cards_template[1] += f"{color}|     |{self.end_color}"
            cards_template[
                2
            ] += f'{color}|{(str(card) if card != 13 else "Ski").center(5)}|{self.end_color}'
            cards_template[3] += f"{color}|_____|{self.end_color}"

        for i in range(len(cards_template)):
            cards_template[i] = cards_template[i].center(
                self.columns
                + 7 * (len(cards) if len(cards) < 4 else len(cards) + 1)
                + 1
            )

        return "\n".join(cards_template)
