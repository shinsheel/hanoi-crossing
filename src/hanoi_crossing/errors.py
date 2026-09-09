# Hand is full error
class HandIsFullError(Exception):
    def __str__(self):
        return "Hand is full"
    pass

# illegal move error
class IllegalMoveError(Exception):
    def __str__(self):
        return "Illegal move"
