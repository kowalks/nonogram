from enum import Enum, auto


class Cell(Enum):
    UNKNOWN = auto()
    BLACK = auto()
    WHITE = auto()

class Line:
    size: int
    clues: list[int]

    def __init__(self, size: int, clues: list[int], default: Cell = Cell.UNKNOWN):
        self.size = size
        self.clues = clues
        self.data = [default] * self.size
        self.solutions = list(self.generate_solutions(size, clues))
        self.is_completed = False
    
    @classmethod
    def generate_solutions(cls, size: int, clues: list[int]):
        if size <= 0:
            return 

        if len(clues) == 0:
            yield (Cell.WHITE, ) * size
            return

        if len(clues) == 1:
            clue = clues[0]
            for before in range(size-clue+1):
                after = size-clue-before
                sol = (Cell.WHITE, ) * before + (Cell.BLACK, ) * clue + (Cell.WHITE, ) * after
                yield sol
            return
        
        # First
        clue = clues[0]
        first = (Cell.BLACK, ) * clue + (Cell.WHITE, )
        solutions = Line.generate_solutions(size - clue - 1, clues[1:])
        for solution in solutions:
            yield first + solution

        # Not first
        solutions = Line.generate_solutions(size - 1, clues)
        first = (Cell.WHITE, )
        for solution in solutions:
            yield first + solution
    
    def update(self, i: int, cell: Cell):
        self.data[i] = cell
        for sol in self.solutions:
            if sol[i] != cell:
                self.solutions.remove(sol)
        
        for cell in self.data:
            if cell == Cell.UNKNOWN:
                return
        self.is_completed = True
    
    def upgrade(self):
        for i in range(self.size):
            cell = self.solutions[0][i]
            all_equal = True
            for sol in self.solutions:
                if sol[i] != cell:
                    all_equal = False
                    break
            if all_equal:
                self.data[i] = cell
                yield i, cell


class Nonogram:
    size: tuple[int, int]
    clues_u: list[list[int]]
    clues_v: list[list[int]]

    def __init__(self, clues_u: list[list[int]], clues_v: list[list[int]]):
        self.clues_u = clues_u
        self.clues_v = clues_v
        self.size = (len(clues_u), len(clues_v))

        size_u, size_v = self.size
        self.data = [[Cell.UNKNOWN for _ in range(size_v)] for _ in range(size_u)]
        self.lines_u = [Line(size_u, clues_u[u]) for u in range(size_u)]
        self.lines_v = [Line(size_v, clues_v[v]) for v in range(size_v)]

    def solve(self):
        while not self.is_completed():
            for u, line in enumerate(self.lines_u):
                for v, cell in line.upgrade():
                    self.update(u, v, cell)

            for v, line in enumerate(self.lines_v):
                for u, cell in line.upgrade():
                    self.update(u, v, cell)

    def update(self, u: int, v: int, cell: Cell):
        self.data[u][v] = cell
        self.lines_u[u].update(v, cell)
        self.lines_v[v].update(u, cell)
    
    def is_completed(self):
        for line in self.lines_u:
            if not line.is_completed:
                return False
        
        for line in self.lines_v:
            if not line.is_completed:
                return False
        
        return True

    def print(self):
        size_u, size_v = self.size
        for u in range(size_u):
            for v in range(size_v):
                match self.data[u][v]:
                    case Cell.UNKNOWN:
                        print("  ", end='')
                    case Cell.BLACK:
                        print("⬛", end='')
                    case Cell.WHITE:
                        print("⬜", end='')
            print('')

if __name__ == '__main__':
    clues_u = [[7], [3, 1], [3, 1], [3, 1], [3, 1], [9], [10], [8, 1], [10], [2, 2]]
    clues_v = [[4], [10], [10], [9], [1, 4], [1, 4], [9], [1, 5], [2, 2], [3]]
    nono = Nonogram(clues_u, clues_v)
    print('optimizing')
    nono.solve()
    nono.print()

    u = [[6],[1,7],[2,7],[3,1,3,2],[7,4],[11],[2,3],[3,3,1],[1,2],[1,3,1],[4,3],[1,2,2],[2,7],[5,8],[5,6,1],[5,2,4,2],[8,2,1,4],[7,1,8],[8,9],[8,9]]
    v = [[4],[7],[7],[7],[2,8],[2,1,4],[2,1,5],[4,1,5],[11,2],[5,1,6],[3,2,1,2,6],[3,2,1,5,2],[3,2,1,2,4,3],[4,1,1,5,3],[4,9,4],[7,1,1,3],[4,6],[2,5],[2,4],[1,4]]
    nono = Nonogram(u, v)
    print('optimizing')
    nono.solve()
    nono.print()