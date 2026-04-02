# tic_tac_toe.py

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def display_board(self):
        # ANSI color codes
        colors = {"X": "\033[94m", "O": "\033[91m", "reset": "\033[0m"}
        lines = []
        for i in range(0, 9, 3):
            row = []
            for j in range(3):
                idx = i + j
                cell = self.board[idx]
                if cell == " ":
                    cell_display = f"\033[90m{idx+1}\033[0m"
                else:
                    cell_display = f"{colors[cell]}{cell}{colors['reset']}"
                row.append(cell_display)
            lines.append(" │ ".join(row))
        divider = "───┼───┼───"
        print("\n")
        for i, line in enumerate(lines):
            print(" " + line)
            if i < 2:
                print(" " + divider)
        print("\n")

    def make_move(self, position):
        if 1 <= position <= 9 and self.board[position-1] == " ":
            self.board[position-1] = self.current_player
            return True
        return False

    def check_winner(self):
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return True
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return True
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return True
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return True
        return False

    def is_board_full(self):
        return " " not in self.board

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

def main():
    game = TicTacToe()
    print("\033[96mWelcome to Tic Tac Toe!\033[0m")
    print("Positions are numbered from 1-9, left to right, top to bottom.\n")
    
    while True:
        game.display_board()
        print(f"Player \033[1m{game.current_player}\033[0m's turn")
        
        try:
            position = int(input("Enter position (1-9): "))
            if not game.make_move(position):
                print("\033[93mInvalid move! Try again.\033[0m")
                continue
        except ValueError:
            print("\033[93mPlease enter a number between 1 and 9!\033[0m")
            continue

        if game.check_winner():
            game.display_board()
            print(f"\033[92mPlayer {game.current_player} wins!\033[0m")
            break
            
        if game.is_board_full():
            game.display_board()
            print("\033[95mIt's a tie!\033[0m")
            break
            
        game.switch_player()

    play_again = input("Would you like to play again? (y/n): ")
    if play_again.lower() == 'y':
        main()

if __name__ == "__main__":
    main()