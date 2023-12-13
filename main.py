import shutil
from time import sleep

from game import Game
from computerplayer import ComputerPlayer
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
    stack_size = 30

    game = Game()
    player = ComputerPlayer(game.give_cards(stack_size))

    ui = UI(columns)

    # game loop
    action = ""
    turn = 1

    while action != "exit":
        if not player.show_stack():
            ui.draw_frame(game, player, turn)
            print(f"You Won! in {turn} turns".center(columns))
            break

        if not len(player.show_hand()):
            player.take_cards(game.give_cards(5))

        ui.draw_frame(game, player, turn)

        if player is Player:
            action = input("action: ")
        else:
            action = player.make_dumbmove(game.show_stack())
            sleep(0.3)

        if action == "help":
            ui.show_help()
            input("Press enter to continue")
            continue
        elif action == "reset":
            game = Game()
            player = ComputerPlayer(game.give_cards(stack_size), name)
            turn = 1
            action = "0"
            continue

        command, target, origin = parse_action(action)

        # place something from stack
        if command == 0:
            player_stack = player.show_stack()

            added = game.add_to_stack(target, player_stack)
            if added:
                player.give_stack_card()

        # place something from waiting stack
        elif command == 1:
            w_stack = player.show_waiting_stack()

            if len(w_stack) - 1 < origin:
                origin = len(w_stack) - 1

            added = game.add_to_stack(target, w_stack[origin])
            if added:
                player.give_wait_card(origin)

        # place something from the hand
        elif command == 2:
            hand = player.show_hand()

            if len(hand) - 1 < origin:
                origin = len(hand) - 1

            added = game.add_to_stack(target, hand[origin])
            if added:
                player.give_card(origin)

        # end turn
        elif command == 3:
            player.end_turn(origin, target)
            player.take_cards(game.give_cards(5 - len(player.show_hand())))
            turn += 1
