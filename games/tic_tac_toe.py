class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def display_board(self):
        print("\n")
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")
        print("\n")

    def make_move(self, position):
        if 1 <= position <= 9 and self.board[position-1] == " ":
            self.board[position-1] = self.current_player
            return True
        return False

    def check_winner(self):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return True
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return True
        # Check diagonals
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
    print("Welcome to Tic Tac Toe!")
    print("Positions are numbered from 1-9, left to right, top to bottom.")
    
    while True:
        game.display_board()
        print(f"Player {game.current_player}'s turn")
        
        try:
            position = int(input("Enter position (1-9): "))
            if not game.make_move(position):
                print("Invalid move! Try again.")
                continue
        except ValueError:
            print("Please enter a number between 1 and 9!")
            continue

        if game.check_winner():
            game.display_board()
            print(f"Player {game.current_player} wins!")
            break
            
        if game.is_board_full():
            game.display_board()
            print("It's a tie!")
            break
            
        game.switch_player()

    play_again = input("Would you like to play again? (y/n): ")
    if play_again.lower() == 'y':
        main()

if __name__ == "__main__":
    main()