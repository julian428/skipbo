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


def game_loop(player_type="p", verbose=True) -> int:
    columns = shutil.get_terminal_size().columns
    stack_size = 30

    game = Game()
    player: Player | ComputerPlayer = Player([])
    if player_type == "p":
        player = Player(game.give_cards(stack_size))
    elif player_type[0] == "c":
        player = ComputerPlayer(game.give_cards(stack_size))

    ui = UI(columns)

    action = ""
    turn = 1

    while action != "exit":
        if not player.show_stack():
            if verbose:
                ui.draw_frame(game, player, turn)
                print(f"You Won! in {turn} turns".center(columns))
            break

        if not len(player.show_hand()):
            player.take_cards(game.give_cards(5))

        if verbose:
            ui.draw_frame(game, player, turn)

        if isinstance(player, ComputerPlayer):
            if len(player_type) and player_type[1] == "d":
                action = player.make_dumbmove(game.show_stack())
            elif len(player_type) and player_type[1] == "b":
                action = player.make_beginnermove(game.show_stack())
            sleep(verbose * 0.5)
        else:
            action = input("action: ")

        if action == "help":
            ui.show_help()
            input("Press enter to continue")
            continue
        elif action == "reset":
            game = Game()
            if player_type == "p":
                player = Player(game.give_cards(stack_size))
            elif player_type == "c":
                player = ComputerPlayer(game.give_cards(stack_size))
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

    return turn


if __name__ == "__main__":
    games = 0
    r = 1

    # p - player, cd - compute_dumb, cb - computer_beginner
    for i in range(r):
        games += game_loop("cb", True)
    print(games / r)
