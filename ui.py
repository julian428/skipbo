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
        print(self.draw_cards(game.show_stack() + [-1, game.show_cards_length()]))
        print("\n\n")
        print(f"{player.identity()}'s stack".center(self.columns))
        print(self.draw_cards([player.show_stack()]))
        print("\n")
        print(f"{player.identity()}'s waiting stack".center(self.columns))
        print(self.draw_cards(player.show_waiting_stack()))
        print("\n")
        print(f"{player.identity()}'s hand".center(self.columns))
        print(self.draw_cards(player.show_hand()))
        print("\n\n")
        print("type 'help' to get help".center(self.columns))
        print("\n")

    def show_help(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n")
        print("type 'exit' to exit game".center(self.columns))
        print("\n")
        print("type 'reset' to restart game".center(self.columns))
        print("\n")
        print("0 (take from stack) 0-3 (target stack)".center(self.columns))
        print("\n")
        print(
            "1 (take from waiting stacks) 0-3 (target stack) 0-3 (origin stack)".center(
                self.columns
            )
        )
        print("\n")
        print(
            "2 (take from hand) 0-3 (target stack) 0-4 (origin hand index)".center(
                self.columns
            )
        )
        print("\n")
        print(
            "3 (end turn) 0-3 (target waiting stack) 0-4 (origin hand index)".center(
                self.columns
            )
        )

    def draw_menu(self) -> tuple[dict[str, str], dict[str, str]]:
        os.system("cls" if os.name == "nt" else "clear")

        print("Skipbo")
        print("\n")

        player0_name = input("Player 0 name: ") or "Player zero"
        print("\n")
        print("0 - human, 1 - computer")
        t = input("Player type: ")
        player0_type = "0"
        if t == "1":
            print("\n")
            print("0 - dumb level, 1 - beginner level")
            player0_type = input("Computer level: ") or "0"
        print("\n\n")

        player1_name = input("Player 1 name: ") or "Player one"
        print("\n")
        print("0 - human, 1 - computer")
        t = input("Player type: ")
        player1_type = "0"
        if t == "1":
            print("\n")
            print("0 - dumb level, 1 - beginner level")
            player1_type = input("Computer level: ") or "0"
        print("\n\n")

        return (
            {"name": player0_name, "type": player0_type},
            {"name": player1_name, "type": player1_type},
        )

    def draw_cards(self, cards: list[int]) -> str:
        cards_template: list[str] = [
            "",
            "",
            "",
            "",
        ]  # [0] top  [1] padding  [2] value  [3] bottom

        for card in cards:
            if 0 > card or card > 13:
                color = "\033[89m"
            else:
                color = self.colors[math.ceil(card / 4)]
            display_value = str(card)
            if card == 13:
                display_value = "Ski"
            elif card == 0:
                display_value = " "

            if len(cards_template[0]):
                cards_template[0] += "       "
            if len(cards_template[1]):
                cards_template[1] += "       "
            if len(cards_template[2]):
                cards_template[2] += "       "
            if len(cards_template[3]):
                cards_template[3] += "       "

            if card < 0:
                continue

            cards_template[0] += f"{color} _____ {self.end_color}"
            cards_template[1] += f"{color}|     |{self.end_color}"
            cards_template[2] += f"{color}|{display_value.center(5)}|{self.end_color}"
            cards_template[3] += f"{color}|_____|{self.end_color}"

        for i in range(len(cards_template)):
            cards_template[i] = cards_template[i].center(
                self.columns + (len(cards_template[i]) // 3 + 4)
            )

        return "\n".join(cards_template)
