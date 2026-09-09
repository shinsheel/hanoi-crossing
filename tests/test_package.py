from hanoi_crossing import Game


def test_game_imports_and_starts() -> None:
    game = Game()
    assert game.players_num == 2
    assert not game.is_over
