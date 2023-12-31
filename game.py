from random import shuffle


class Game:
    def __init__(self) -> None:
        self.__stack = [[0], [0], [0], [0]]
        self.__cards = self.shuffle_cards()
        self.__turn = 1
        self.__points = 0

    def next_turn(self) -> None:
        self.__turn += 1

    def show_points(self) -> int:
        return self.__points

    def add_points(self, value: int) -> None:
        self.__points += value

    def show_turn(self) -> int:
        return self.__turn

    def show_stack(self) -> list[int]:
        top_stack = [self.joker_to_value(i) for i in range(len(self.__stack))]

        return top_stack

    def show_cards_length(self) -> int:
        return len(self.__cards)

    def shuffle_cards(self, cards: list[int] = []) -> list[int]:
        if not cards:
            cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] * 12 + [13] * 18
        shuffle(cards)
        return cards

    def refill_cards(self, stack_index: int) -> None:
        cards = self.__stack[stack_index][1:]
        shuffle(cards)
        self.__cards = cards + self.__cards

    def joker_to_value(self, stack_index) -> int:
        jokers = 0
        stack_value = self.__stack[stack_index][-1]
        while stack_value == 13:
            jokers += 1
            stack_value = self.__stack[stack_index][-1 * (jokers + 1)]

        stack_value += jokers
        return stack_value

    def add_to_stack(self, stack_index: int, value: int) -> bool:
        if stack_index > 3:
            stack_index = 3
        elif stack_index < 0:
            stack_index = 0

        stack_value = self.joker_to_value(stack_index)

        if value > 13:
            return False
        elif stack_value == 12 and (value == 1 or value == 13):
            self.refill_cards(stack_index)
            self.__stack[stack_index] = [0, value]
            return True
        elif value != 13 and value != stack_value + 1:
            return False

        self.__stack[stack_index].append(value)
        return True

    def give_cards(self, quantity: int) -> list[int]:
        if len(self.__cards) < quantity:
            return []
        player_cards = self.__cards[-quantity:]
        self.__cards = self.__cards[:-quantity]
        return player_cards
