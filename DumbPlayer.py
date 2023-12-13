from player import Player


class DumbPlayer(Player):
    def __init__(self, stack: list[int], name: str = "Player") -> None:
        super().__init__(stack, name)
