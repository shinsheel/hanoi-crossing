from typing import Optional, List
from hanoi_crossing.errors import HandIsFullError, IllegalMoveError

class Disk:
    def __init__(self, size: int):
        self.size = size

class Tower:
    def __init__(self, max_disks: int):
        self.disks: List[Disk] = []
        self.max_disks = max_disks

    def append(self, disk: Disk) -> None:
        if self.disks and self.disks[-1].size <= disk.size:
            raise IllegalMoveError()
        self.disks.append(disk)

    def pop(self) -> Disk:
        if not self.disks:
            raise IllegalMoveError()
        return self.disks.pop()

    def is_empty(self) -> bool:
        return not self.disks

    def is_full(self) -> bool:
        return len(self.disks) == self.max_disks

class Hand:
    def __init__(self):
        self.content: Optional[Disk] = None

    def lift(self, disk: Disk) -> None:
        if self.content is not None:
            raise HandIsFullError()
        self.content = disk

    def lift_from_tower(self, tower: Tower) -> None:
        disk = tower.pop()
        self.lift(disk)

    def drop_to_tower(self, tower: Tower) -> None:
        if self.content is None:
            raise IllegalMoveError()
        disk = self.content
        self.content = None
        tower.append(disk)

class Player:
    def __init__(self, towers: List[Tower]):
        self.hand = Hand()
        self.towers: List[Tower] = towers

    @property
    def is_won(self) -> bool:
        return self.towers[0].is_empty() and self.towers[-1].is_full()

    def move(self, from_tower: Tower, to_tower: Tower) -> None:
        self.hand.lift_from_tower(from_tower)
        self.hand.drop_to_tower(to_tower)


    
class Game:

    def __init__(self, max_disks: Optional[int] = 3, players_num: Optional[int] = 2, move_order: Optional[List[int]] = None):
        self.max_disks = max_disks
        self.players_num = players_num
        self.move_order = move_order if move_order is not None else [i for i in range(players_num)]
        self.move_order_curr_cycle = self.move_order.copy()
        self.current_player_index = self.move_order_curr_cycle.pop(0)
        self.players = [Player([]) for _ in range(players_num)]
        self.biggest_disk_size = max_disks * 2

        crossing_tower = Tower(max_disks)
        for player in self.players:
            start_tower = Tower(self.max_disks)
            end_tower = Tower(self.max_disks)
            player.towers = [start_tower, crossing_tower, end_tower]

        for player_idx, player in enumerate(self.players):
            # Player A (even index): odd sizes, largest at bottom (e.g. 5, 3, 1).
            # Player B (odd index): even sizes, largest at bottom (e.g. 6, 4, 2).
            for i in range(self.max_disks):
                size = (self.max_disks - i) * 2 - (1 if player_idx % 2 == 0 else 0)
                player.towers[0].append(Disk(size))

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]
        
    def display_ascii(self) -> str:
        towers = self.current_player.towers
        col_width = self.biggest_disk_size + (self.biggest_disk_size % 2 == 0)
        height = max(self.max_disks, max((len(tower.disks) for tower in towers), default=0))

        def cell(text: str) -> str:
            extra = col_width - len(text)
            left = extra // 2
            return " " * left + text + " " * (extra - left)

        lines: List[str] = []
        for level in range(height - 1, -1, -1):
            cells = []
            for tower in towers:
                if level < len(tower.disks):
                    cells.append(cell("=" * tower.disks[level].size))
                else:
                    cells.append(cell("|"))
            lines.append("  ".join(cells))

        lines.append("  ".join(cell(str(i + 1)) for i in range(len(towers))))

        hand = self.current_player.hand.content
        if hand is not None:
            lines.append(f"Hand: {'=' * hand.size} ({hand.size})")
        else:
            lines.append("Hand: empty")

        return "\n".join(lines)

    def print_ascii_total(self) -> None:
        for player_idx in range(self.players_num):
            self.current_player_index = player_idx
            print(f"Player {player_idx + 1}")
            print(self.display_ascii())

    def next_turn(self) -> None:
        if not self.move_order_curr_cycle:
            self.move_order_curr_cycle = self.move_order.copy()
        self.current_player_index = self.move_order_curr_cycle.pop(0)

    def move(self, from_tower: Tower, to_tower: Tower, player_idx: Optional[int] = None) -> None:
        player = self.current_player if player_idx is None else self.players[player_idx]
        player.move(from_tower, to_tower)
        self.next_turn()

    @property
    def is_over(self) -> bool:
        return any(player.is_won for player in self.players)
