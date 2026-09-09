import argparse
import sys
from typing import List, Optional

from hanoi_crossing.models import Game


DEFAULT_MAX_DISKS = 3
DEFAULT_PLAYERS_NUM = 2
DEFAULT_MOVE_ORDER = [0, 1]


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hanoi Crossing")
    parser.add_argument(
        "--order",
        nargs="+",
        type=int,
        default=None,
        metavar="PLAYER",
        help="Turn order as player indices, e.g. --order 0 1 0",
    )
    parser.add_argument(
        "--replay",
        default=None,
        metavar="SOURCE",
        help="Replay recorded moves",
    )
    parser.add_argument(
        "--format",
        choices=["ascii", "yaml"],
        default="ascii",
        help="Output format for board state",
    )
    return parser.parse_args(argv)


def main(args: Optional[List[str]] = None) -> None:
    def play_game(game: Game) -> None:
        while not game.is_over:
            print(f"Player {game.current_player_index + 1}'s turn")
            print(game.display())
            input_move = input("Enter your move (from_tower to_tower): ")
            from_tower_raw, to_tower_raw = input_move.split(" ")
            from_idx, to_idx = int(from_tower_raw), int(to_tower_raw)
            from_tower = game.current_player.towers[from_idx - 1]
            to_tower = game.current_player.towers[to_idx - 1]
            game.move(from_tower, to_tower)

        print("Game over!")
        print(f"Player {game.current_player.index + 1} won!")

    def replay_game(game: Game, replay_source: str) -> None:
        try:
            with open(replay_source, "r") as file:
                for line in file:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    player_idx, from_tower_idx, to_tower_idx = [int(x) for x in stripped.split(" ")]
                    player = game.players[player_idx]
                    from_tower = player.towers[from_tower_idx]
                    to_tower = player.towers[to_tower_idx]
                    game.move(from_tower, to_tower, player_idx)
        except Exception as e:
            print(f"error: {e}")
            
                
        game.display_total()
        

    parsed = parse_args(args)
    order = parsed.order
    replay = parsed.replay

    game = Game(DEFAULT_MAX_DISKS, DEFAULT_PLAYERS_NUM, order, format=parsed.format)
    if not replay:
        play_game(game)
    else:
        replay_game(game, replay)


if __name__ == "__main__":
    params = sys.argv[1:]

    print("Welcome to the game of Hanoi!")
    print("The goal is to move all the disks from the start tower to the end tower.")

    main(params)
