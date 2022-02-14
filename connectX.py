import numpy as np

class connectX:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.grid = np.asarray([0]*42).reshape(self.rows, self.cols)
        self.player = 1
        # self.gameOver = False

    def dropPiece(self, node, col, player):
        grid = node.copy()
        for row in range(self.rows - 1, -1, -1):
            if grid[row][col] == 0:
                break
        grid[row][col] = player
        return grid

    def isTerminalWindow(self, window):
        return window.count(1)== 4 or window.count(2) == 4

    #check if next-step winning
    def isTerminalNode(self, grid):
        #check if draw
        if list(grid[0, :]).count(0) == 0:
            return True

        #check horizontal
        for r in range(self.rows):
            for c in range(self.cols-3):
                window = list(grid[r, c:c+4])
                if self.isTerminalWindow(window):
                    return True

        #check vertical
        for r in range(self.rows-1, self.rows - 4, -1):
            for c in range(self.cols):
                window = list(grid[r:r-4:-1, c])
                if self.isTerminalWindow(window):
                    return True
        
        #check negative diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = list(grid[range(r,r+4), range(c, c+4)])
                if self.isTerminalWindow(window):
                    return True
        
        #check positive diagonal
        for r in range(self.rows - 1, 2, -1):
            for c in range(self.cols -3):
                window = list(grid[range(r,r-4,-1), range(c,c+4)])
                if self.isTerminalWindow(window):
                    return True
        
        return False
    
    def isValid(self, grid, col):
        if 0>col or col>=7:
            return False
        if grid[0][col] != 0:
            return False
        return True
    
    def gamePlay(self):
        while not self.isTerminalNode(self.grid):
            if self.player == 1:
                self.showBoard()
                move = int(input("Enter your move: "))

                while not self.isValid(self.grid, move):
                    print("Invalid move. Try again!!!")
                    move = int(input("Enter your move: "))
            
                self.grid = self.dropPiece(self.grid, move, self.player)
            
            elif self.player == 2:
                move = self.ai()
                self.grid = self.dropPiece(self.grid, move, self.player)

            self.player = self.get_enemy(self.player)

        if self.isTerminalNode(self.grid):
            #self.gameOver = True
            self.showBoard()
            if list(self.grid[0, :]).count(0) == 0:
                print("Draw")
                print("see you next time")
            if self.player == 1:
                print("2 win")
            else:
                print("1 win")

            print("See you next time")

    def showBoard(self):
        print(self.grid)
        print("  0 1 2 3 4 5 6")

    def get_enemy(self, player):
        if player == 1:
            return 2
        return 1

    def evaluate(self, grid):
        #Fix bug: numThree = self.countWindows(grid, 3, 1->2)
        numThree = self.countWindows(grid, 3, 2)
        numFour = self.countWindows(grid, 4, 2)
        numThreeOpp = self.countWindows(grid, 3, 1)
        numFourOpp = self.countWindows(grid, 4, 1)
        score = 10000*numFour + 100*numThree - 100*numThreeOpp - 10000*numFourOpp
        return score

    def countWindows(self, grid, numDiscs, player):
        count = 0
        #check horizontal
        for r in range(self.rows-1, -1, -1):
            for c in range(self.cols-3):
                window = list(grid[r, c:c+4])
                if self.checkWindow(window, numDiscs, player):
                    count+=1
        
        #check vertical
        for r in range(self.rows - 1, 2, -1):
            for c in range(self.cols):
                window = list(grid[r:r-4:-1,c])
                if self.checkWindow(window, numDiscs, player):
                    count +=1
        
        #check negative diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = list(grid[range(r,r+4), range(c, c+4)])
                if self.checkWindow(window, numDiscs, player):
                    count +=1
        
        #check positive diagonal
        for r in range(self.rows - 1, 2, -1):
            for c in range(self.cols -3):
                window = list(grid[range(r,r-4,-1), range(c,c+4)])
                if self.checkWindow(window, numDiscs, player):
                    count +=1
        
        return count

    def checkWindow(self, window, numDiscs, player):
        return (window.count(player) == numDiscs and window.count(0) == 4 - window.count(player))

    def minimax(self, node, depth, player):
        isTerminal = self.isTerminalNode(node)

        if depth == 0 or isTerminal:
            return self.evaluate(node)
        
        best = 10**8 if player == 1 else -10**8
        for c in range(self.cols):
            if self.isValid(node, c):
                nxt_node = self.dropPiece(node, c, player)
                val = self.minimax(nxt_node, depth-1, self.get_enemy(player))

                if player == 1:
                    best = min(best, val)
                elif player == 2:
                    best = max(best, val)
        
        return best

    def ai(self):
        n_step_lookahead = 4
        bestVal = -10**8
        bestMove = -1
        player = 2

        for c in range (self.cols):
            if self.isValid(self.grid, c):
                nxt_node = self.dropPiece(self.grid, c, player)
                val = self.minimax(nxt_node, n_step_lookahead - 1, self.get_enemy(player))

                if val > bestVal:
                    bestVal = val
                    bestMove = c

        return bestMove

    # def debug(self, node):
    #     tmp = self.dropPiece(node, 2, 1)
    #     print(node)
    #     print(tmp)

# def debug():
#     game = connectX()
#     node = np.asarray([0]*42).reshape(6,7)
#     game.debug(node)

# debug()
def main():
    game = connectX()
    game.gamePlay()

main()