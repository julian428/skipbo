import shutil

from game import Game
from player import Player
from ui import UI


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

        # place something from stack
        if action.startswith("0"):
            target = int(action.split(" ")[1])
            player_stack = player.show_stack()

            added = game.add_to_stack(target, player_stack)
            if added:
                player.give_stack_card()

        elif action.startswith("1"):
            target = int(action.split(" ")[1])
            origin = int(action.split(" ")[2])

            added = game.add_to_stack(target, player.show_waiting_stack()[origin])
            if added:
                player.give_wait_card(origin)

        elif action.startswith("2"):
            target = int(action.split(" ")[1])
            origin = int(action.split(" ")[2])

            added = game.add_to_stack(target, player.show_hand()[origin])
            if added:
                player.give_card(origin)

        elif action.startswith("3"):
            target = int(action.split(" ")[1])
            origin = int(action.split(" ")[2])

            player.end_turn(origin, target)
            player.take_cards(game.give_cards(5 - len(player.show_hand())))
            turn += 1
