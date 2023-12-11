from random import shuffle


class Game:
    def __init__(self) -> None:
        self.__stack = [0, 0, 0, 0]
        self.__cards = self.shuffle_cards()

    def show_stack(self) -> list[int]:
        return self.__stack

    def shuffle_cards(self) -> list[int]:
        cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] * 12 + [13] * 18
        shuffle(cards)
        return cards

    def add_to_stack(self, stack_index: int, value: int) -> bool:
        if stack_index > 3:
            stack_index = 3
        elif stack_index < 0:
            stack_index = 0

        stack_value = self.__stack[stack_index]
        if value > 13:
            return False
        elif stack_value == 12 and (value == 1 or value == 13):
            self.__stack[stack_index] = 1
            return True
        elif value == 13:
            self.__stack[stack_index] += 1
            return True
        elif value != stack_value + 1:
            return False

        self.__stack[stack_index] = value
        return True

    def give_cards(self, quantity: int) -> list[int]:
        if len(self.__cards) < quantity:
            self.__cards = self.shuffle_cards()
        player_cards = self.__cards[-quantity:]
        self.__cards = self.__cards[:-quantity]
        return player_cards
