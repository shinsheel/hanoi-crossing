import sys

from models import Game


DEFAULT_MAX_DISKS = 3
DEFAULT_PLAYERS_NUM = 2
DEFAULT_MOVE_ORDER = [0, 1]


def main(args: List[str]) -> None:
    def play_game(game: Game) -> None:
        while not game.is_over:
            print(f"Player {game.current_player_index + 1}'s turn")
            print(game.display_ascii())
            input_move = input("Enter your move (from_tower to_tower): ")
            from_tower_raw, to_tower_raw = input_move.split(" ")
            from_idx, to_idx = int(from_tower_raw), int(to_tower_raw)
            from_tower = game.current_player.towers[from_idx - 1]
            to_tower = game.current_player.towers[to_idx - 1]
            game.move(from_tower, to_tower)
            game.next_turn()

        print("Game over!")
        print(f"Player {game.current_player.index + 1} won!")

    order = DEFAULT_MAX_DISKS
    if args:
        order = [int(arg) for arg in args]
    
    game = Game(DEFAULT_MAX_DISKS, DEFAULT_PLAYERS_NUM, order)
    play_game(game)


if __name__ == "__main__":
    args = sys.argv[1:]
    print("Welcome to the game of Hanoi!")
    print("The goal is to move all the disks from the start tower to the end tower.")
    main(args)