from typing import Optional
from errors import HandIsFullError, IllegalMoveError

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


    