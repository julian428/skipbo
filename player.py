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

    def available_moves(self, stack: list[int]) -> dict[str, list[int]]:
        moves = {"stack": [], "w_stack": [], "hand": [], "end_turn": []}
        waiting_stack = self.show_waiting_stack()
        stack_card = self.show_stack()
        hand = self.show_hand()

        for i, card in enumerate(stack):
            # player stack moves
            if stack_card == 13 or stack_card == card + 1:
                moves["stack"].append("0" + str(i))

            # player waiting stack moves
            for j, w_card in enumerate(waiting_stack):
                if w_card == 13 or w_card == card + 1:
                    moves["w_stack"].append("1" + str(i) + str(j))

            # player hand moves
            for j, h_card in enumerate(hand):
                if h_card == 13 or h_card == card + 1:
                    moves["hand"].append("2" + str(i) + str(j))

            for j in range(len(hand)):
                moves["end_turn"].append("3" + str(i) + str(j))

        return moves
