import os

from game import Game
from player import Player


class UI:
    def __init__(self, columns) -> None:
        self.columns = columns
        pass

    def draw_frame(self, game: Game, player: Player, turn: int) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print("Skipbo".center(self.columns))
        print("\n")
        print(f"turn: {turn}".center(self.columns))
        print("\n")
        print(self.draw_stacks(game.show_stack()))
        print("\n\n")
        print(f"{player.identity()}'s stack".center(self.columns))
        print(self.draw_card(player.show_stack()))
        print("\n")
        print(f"{player.identity()}'s waiting stack".center(self.columns))
        print(self.draw_stacks(player.show_waiting_stack()))
        print("\n")
        print(f"{player.identity()}'s hand".center(self.columns))
        print(self.draw_hand(player.show_hand()))
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

    def draw_card(self, number: int) -> str:
        top = " _____ ".center(self.columns)
        padding = "|     |".center(self.columns)
        value = f'|{f"{number}".center(5)}|'.center(self.columns)
        bottom = "|_____|".center(self.columns)

        return "\n".join([top, padding, value, bottom])

    def draw_stacks(self, cards: list[int]) -> str:
        if len(cards) > 4:
            cards = cards[:4]
        elif len(cards) < 4:
            cards.extend([0 for _ in range(4 - len(cards))])

        top = " _____         _____         _____         _____ ".center(self.columns)
        padding = "|     |       |     |       |     |       |     |".center(
            self.columns
        )
        value = f'|{f"{cards[0]}".center(5)}|       |{f"{cards[1]}".center(5)}|       |{f"{cards[2]}".center(5)}|       |{f"{cards[3]}".center(5)}|'.center(
            self.columns
        )
        bottom = "|_____|       |_____|       |_____|       |_____|".center(
            self.columns
        )

        return "\n".join([top, padding, value, bottom])

    def draw_hand(self, hand: list[int]) -> str:
        new_hand = hand + [0 for _ in range(5 - len(hand))]

        top = " _____         _____         _____         _____         _____ ".center(
            self.columns
        )
        padding = (
            "|     |       |     |       |     |       |     |       |     |".center(
                self.columns
            )
        )
        value = f'|{f"{new_hand[0]}".center(5)}|       |{f"{new_hand[1]}".center(5)}|       |{f"{new_hand[2]}".center(5)}|       |{f"{new_hand[3]}".center(5)}|       |{f"{new_hand[4]}".center(5)}|'.center(
            self.columns
        )
        bottom = (
            "|_____|       |_____|       |_____|       |_____|       |_____|".center(
                self.columns
            )
        )

        return "\n".join([top, padding, value, bottom])
