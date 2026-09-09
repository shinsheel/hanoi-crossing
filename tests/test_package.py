import pytest
import yaml

from hanoi_crossing import Game, IllegalMoveError


def test_game_imports_and_starts() -> None:
    game = Game()
    assert game.players_num == 2
    assert not game.is_over


def test_yaml_display_includes_player_view() -> None:
    game = Game(format="yaml")
    view = yaml.safe_load(game.display())
    assert view["player"] == 0
    assert view["hand"] is None
    assert view["towers"][0] == [5, 3, 1]
    assert view["towers"][1] == []
    assert view["towers"][2] == []


def test_illegal_move_does_not_lose_disk() -> None:
    game = Game(max_disks=2)
    player = game.current_player
    start, shared, _goal = player.towers
    player.move(start, shared)

    with pytest.raises(IllegalMoveError):
        player.move(start, shared)

    assert [disk.size for disk in start.disks] == [3]
    assert [disk.size for disk in shared.disks] == [1]
    assert player.hand.content is None


def test_yaml_total_includes_both_players() -> None:
    game = Game(format="yaml")
    total = yaml.safe_load(game.display_yaml_total())
    assert len(total["players"]) == 2
    assert total["players"][1]["towers"][0] == [6, 4, 2]
    assert total["winner"] is None
