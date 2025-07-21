'''
36 Valid Sudoku
https://leetcode.com/problems/valid-sudoku/description/

Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need to be validated according to the following rules:
    Each row must contain the digits 1-9 without repetition.
    Each column must contain the digits 1-9 without repetition.
    Each of the nine 3 x 3 sub-boxes of the grid must contain the digits 1-9 without repetition.

Note:
A Sudoku board (partially filled) could be valid but is not necessarily solvable.
Only the filled cells need to be validated according to the mentioned rules.


Example 1:
Input: board =
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true

Example 2:
Input: board =
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.

Constraints:
board.length == 9 (Thus, N = 9)
board[i].length == 9
board[i][j] is a digit 1-9 or '.'.

Solution:
1. Brute Force:
Step 1: For each row, init a hash set and read the values from column indices 0,...,N-1. If an element is not present in the hash set, add it to the hash set. If an element is present in the hash set, then we have found a duplicate value and hence return False.
Step 2: Repeat Step 1 for columns
Step 3: Repeat Step 1 for boxes. For boxes, we use the starting index pair (i,j) of the box (left top corner) to scan the remaining cells by adding 0,1,2 to (i,j) independently.

The disadvantage of this method is we perform 3 separate scans of the matrix.

T: O(3N^2), S: O(1) (Note: N=9 is a constant. N doesn't change)

2. Sub-optimal:
We perform only 1 scan of the matrix. But we increase the size by introducing of 3 hash maps for row, col, and box.

The row hash map has row indices as the keys (0,...,N-1). For each key, we maintain a separate hash set that stores the the elements of the row corresponding to the key.

Likewise, the column hash map has column indices as the keys (0,...,N-1). For each key, we maintain a separate hash set that stores the the elements of the column corresponding to the key.

The box hash map maintains a tuple as the keys, where the tuples are:
(0,0) for the left top 3x3 box
(0,1) for the mid top 3x3 box
(0,2) for the right top 3x3 box

(1,0) for the left mid 3x3 box
(1,1) for the mid mid 3x3 box
(1,2) for the right mid 3x3 box

(2,0) for the left bottom 3x3 box
(2,1) for the mid bottom 3x3 box
(2,2) for the right bottom 3x3 box

Thus, for a given board[i][j], the key for the corresponding box = (i//3, j//3)

Time: O(N^2), Space: O(3N) (Note: N=9 is a constant. N doesn't change)

3. Optimal:
We can do away with the row hash map by maintaining a single hash set. We init the same hash set for every row and scan the columns. This way, we don't need to maintain N hash sets (one for each row) as we were doing with the sub-optimal approach.

Time: O(N^2), Space: O(2N) (Note: N=9 is a constant. N doesn't change)

'''
from typing import List
from collections import defaultdict

def isValidSudokuBrute(board: List[List[str]]) -> bool:
    ''' Time: O(3N^2), Space: O(1) '''
    def box(x,y):
        delta = [0,1,2]
        h = {k:v for k,v in g.items()}
        for i in delta:
            for j in delta:
                x_, y_ = x + i, y + j
                if board[x_][y_] != '.':
                    h[board[x_][y_]] += 1
                    if h[board[x_][y_]] > 1:
                        return False
        return True

    N = len(board)
    g = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0}

    for i in range(N):
        h = {k:v for k,v in g.items()} # Space: O(1)
        for j in range(N):
            if board[i][j] != '.':
                h[board[i][j]] += 1
                if h[board[i][j]] > 1:
                    return False

    for j in range(N):
        h = {k:v for k,v in g.items()}
        for i in range(N):
            if board[i][j] != '.':
                h[board[i][j]] += 1
                if h[board[i][j]] > 1:
                    return False

    for i in list(range(0,N,3)):
        for j in list(range(0,N,3)):
                if not box(i,j):
                    return False

    return True

def isValidSudokuSubOptimal(board: List[List[str]]) -> bool:
    ''' Time: O(N^2), Space: O(3N) = O(N)'''
    N = len(board)

    # Define 3 hash maps - row, col, box.
    # Each hash map has N keys. The corresponding value for each key is a hash set of fixed size 10. Thus, the size of the hash set is independent of N. Thus, the size of hash map is O(10N) = O(N)
    row = defaultdict(set) # O(N)
    col = defaultdict(set) # O(N)
    box = defaultdict(set) # O(N)

    for i in range(N):
        for j in range(N):
            value = board[i][j]
            if value == ".":
                continue
            else:
                bi = (i//3, j//3)
                if value in row[i] or value in col[j] or value in box[bi]:
                    return False
                row[i].add(value)
                col[j].add(value)
                box[bi].add(value)
    return True

def isValidSudokuOptimal(board: List[List[str]]) -> bool:
    ''' Time: O(N^2), Space: O(2N+1) = O(N)'''
    N = len(board)

    col = defaultdict(set) # O(N)
    box = defaultdict(set) # O(N)

    for i in range(N):
        row = set() # O(1)
        for j in range(N):
            value = board[i][j]
            if value == ".":
                continue
            else:
                bi = (i//3, j//3)
                if value in row or value in col[j] or value in box[bi]:
                    return False
                row.add(value)
                col[j].add(value)
                box[bi].add(value)
    return True

def run_isValidSudoku():
    tests = [ ([["5","3",".",".","7",".",".",".","."],
                ["6",".",".","1","9","5",".",".","."],
                [".","9","8",".",".",".",".","6","."],
                ["8",".",".",".","6",".",".",".","3"],
                ["4",".",".","8",".","3",".",".","1"],
                ["7",".",".",".","2",".",".",".","6"],
                [".","6",".",".",".",".","2","8","."],
                [".",".",".","4","1","9",".",".","5"],
                [".",".",".",".","8",".",".","7","9"]], True),
              ([["8","3",".",".","7",".",".",".","."],
                ["6",".",".","1","9","5",".",".","."],
                [".","9","8",".",".",".",".","6","."],
                ["8",".",".",".","6",".",".",".","3"],
                ["4",".",".","8",".","3",".",".","1"],
                ["7",".",".",".","2",".",".",".","6"],
                [".","6",".",".",".",".","2","8","."],
                [".",".",".","4","1","9",".",".","5"],
                [".",".",".",".","8",".",".","7","9"]], False),
            ]
    for test in tests:
        grid, ans = test[0], test[1]
        print(f"\nGrid = {grid}")
        for method in ['brute','suboptim','optim']:
            if method == 'brute':
                valid = isValidSudokuBrute(grid)
            elif method == "suboptim":
                valid = isValidSudokuSubOptimal(grid)
            elif method == "optim":
                valid = isValidSudokuOptimal(grid)
            print(f"Method {method}: Valid Sudoku = {valid}")
            print(f"Pass: {ans == valid}")

run_isValidSudoku()