import shutil

from game import Game
from player import Player
from ui import UI


def parse_action(action: str) -> list[int]:
    actions: list[int] = []
    for l in action:
        if l.isdigit():
            actions.append(int(l))

    if len(actions) < 3:
        actions.extend([0, 0, 0])

    return actions[:3]


if __name__ == "__main__":
    columns = shutil.get_terminal_size().columns

    game = Game()
    player = Player(game.give_cards(30), "Julian")
    ui = UI(columns)

    # game loop
    action = "0"
    turn = 1

    while action != "exit":
        if not player.show_stack():
            print(f"You Won! in {turn} turns".center(columns))
            break

        if not len(player.show_hand()):
            player.take_cards(game.give_cards(5))

        ui.draw_frame(game, player, turn)
        action = input("action: ")
        if action == "help":
            ui.show_help()
            input("Press enter to continue")
            continue
        if action == "reset":
            pass
        command, target, origin = parse_action(action)

        # place something from stack
        if command == 0:
            player_stack = player.show_stack()

            added = game.add_to_stack(target, player_stack)
            if added:
                player.give_stack_card()

        # place something from waiting stack
        elif command == 1:
            added = game.add_to_stack(target, player.show_waiting_stack()[origin])
            if added:
                player.give_wait_card(origin)

        # place something from the hand
        elif command == 2:
            added = game.add_to_stack(target, player.show_hand()[origin])
            if added:
                player.give_card(origin)

        # end turn
        elif command == 3:
            player.end_turn(origin, target)
            player.take_cards(game.give_cards(5 - len(player.show_hand())))
            turn += 1
