from inspect import stack
import shutil
from time import sleep

from game import Game
from computerplayer import ComputerPlayer
from player import Player
from ui import UI

ui = UI(shutil.get_terminal_size().columns)


def parse_action(action: str) -> list[int]:
    actions: list[int] = []
    for l in action:
        if l.isdigit():
            actions.append(int(l))

    if len(actions) < 3:
        actions.extend([0, 0, 0])

    return actions[:3]


# False - won, True - next turn
def player_turn(
    game: Game,
    player: Player,
    ui: UI,
    t: str = "0",
    players: list[Player] = [],
    delay: float = 0.5,
) -> bool:
    turn = game.show_turn()

    if delay:
        ui.draw_frame(game, player, turn)

    action = ""
    if isinstance(player, ComputerPlayer):
        action = player.make_move(game.show_stack(), t)
        sleep(delay)
    else:
        action = input("action: ")

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

        if not len(player.show_hand()):
            player.take_cards(game.give_cards(5))

    # end turn
    elif command == 3:
        player.end_turn(origin, target)
        player.take_cards(game.give_cards(5 - len(player.show_hand())))
        return True

    if not player.show_stack():
        if delay:
            ui.draw_frame(game, player, turn)
        for plyr in players:
            game.add_points(plyr.stack_length())
        if delay:
            print(
                f"{player.identity()} Won! in {turn} turns, with {game.show_points()} points."
            )
        return False

    return player_turn(game, player, ui, t, players, delay)


def game_loop(
    meta_player0: dict[str, str], meta_player1: dict[str, str], delay: float = 0.5
) -> dict[str, str]:
    end = True

    game = Game()
    player0 = ComputerPlayer(game.give_cards(30), meta_player0["name"])
    player0.take_cards(game.give_cards(5))
    player1 = ComputerPlayer(game.give_cards(30), meta_player1["name"])
    player1.take_cards(game.give_cards(5))

    winner = ""

    while end:
        end = player_turn(game, player0, ui, meta_player0["type"], [player1], delay)
        if end == False:
            winner = player0.identity()
            break
        sleep(delay)
        end = player_turn(game, player1, ui, meta_player1["type"], [player0], delay)
        if end == False:
            winner = player1.identity()
            break
        sleep(delay)
        game.next_turn()
    return {"name": winner, "points": str(game.show_points())}


if __name__ == "__main__":
    meta0, meta1 = ui.draw_menu()
    players = {meta0["name"]: "0", meta1["name"]: "0"}

    games = 1
    for game in range(games):
        results = game_loop(meta0, meta1, 0.05)

        current_player_points = int(players[results["name"]])
        players[results["name"]] = str(current_player_points + int(results["points"]))

    print(players)
