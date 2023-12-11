class Player:
    def __init__(self, stack: list[int], name: str = "Player") -> None:
        self.__name = name
        self.__hand: list[int] = []
        self.__stack = stack
        self.__wait_stack: list[list[int]] = [[0], [0], [0], [0]]
        pass

    def identity(self) -> str:
        return self.__name

    def show_hand(self) -> list[int]:
        return self.__hand

    def show_stack(self) -> int:
        if len(self.__stack) < 1:
            return 0
        return self.__stack[-1]

    def show_waiting_stack(self) -> list[int]:
        return [stack[-1] for stack in self.__wait_stack]

    def take_cards(self, cards: list[int] = []) -> list[int]:
        hand_size = len(self.__hand)
        cards_to_take = cards[: 5 - hand_size]

        self.__hand.extend(cards_to_take)

        return cards[5 - hand_size :]

    def end_turn(self, card_index: int, wait_stack_index: int) -> bool:
        if wait_stack_index > 3:
            wait_stack_index = 3
        elif wait_stack_index < 0:
            wait_stack_index = 0

        if card_index > len(self.__hand) - 1:
            card_index = len(self.__hand) - 1
        elif card_index < 0:
            card_index = 0

        card = self.__hand.pop(card_index)
        self.__wait_stack[wait_stack_index].append(card)
        return True

    def give_card(self, card_index: int) -> int:
        return self.__hand.pop(card_index)

    def give_stack_card(self) -> int:
        return self.__stack.pop(-1)

    def give_wait_card(self, wait_stack_index: int) -> int:
        return self.__wait_stack[wait_stack_index].pop(-1)


# testing
if __name__ == "__main__":
    player = Player([1, 2, 3], "Tester")

    # identify
    print(player.identity())

    # taking
    print(
        player.take_cards([0, 1, 2, 3, 4, 5, 6, 7])
    )  # should give back cards if there are too many

    # ending
    player.end_turn(0, 0)

    # giving

    # showing
    print(player.show_hand())
    print(player.show_stack())
    print(player.show_waiting_stack())

    pass
