# Constants
WHITE, BLACK = 'white', 'black'  # Defining constants for white and black pieces

# Chess Pieces Classes
class Piece:
    def __init__(self, color):
        self.color = color  # Every piece has a color (white or black)
        self.has_moved = False  # Tracks whether the piece has moved (important for castling)

    def valid_moves(self, pos):
        pass  # This is a placeholder method to be implemented by specific piece types

# Class for Pawn Piece
class Pawn(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        moves = []  # List to store valid moves for the pawn
        x, y = pos  # Current position of the pawn
        direction = -1 if self.color == WHITE else 1  # Pawns move up (for white) or down (for black)

        # Move forward by one square
        if 0 <= x + direction < 8 and board.get_piece((x + direction, y)) == ' ':
            moves.append((x + direction, y))  # Add the forward move
            # Two-square move from starting position
            if not self.has_moved and 0 <= x + 2 * direction < 8 and board.get_piece((x + 2 * direction, y)) == ' ':
                moves.append((x + 2 * direction, y))  # Add the two-square move

        # Diagonal captures
        for dy in [-1, 1]:  # Check both diagonal directions (left and right)
            if 0 <= y + dy < 8:  # Ensure it's within board limits
                target = board.get_piece((x + direction, y + dy))  # Get the piece diagonally
                if target != " " and target.color != self.color:  # If there's an enemy piece, capture
                    moves.append((x + direction, y + dy))
                # En Passant capture
                if en_passant_target == (x + direction, y + dy):  # Special rule: capture via en passant
                    moves.append((x + direction, y + dy))

        return moves  # Return the list of valid moves

# Class for Rook Piece
class Rook(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Rook can move in four directions (up, down, left, right)
        return self._generate_sliding_moves(board, pos, directions)  # Generate all valid moves for rook

    # Helper method for sliding pieces (rook and bishop)
    def _generate_sliding_moves(self, board, pos, directions):
        moves = []  # List to store valid moves
        x, y = pos  # Current position of the rook
        for dx, dy in directions:  # Iterate over each direction
            nx, ny = x + dx, y + dy  # Move in the direction
            while 0 <= nx < 8 and 0 <= ny < 8:  # While the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == ' ':  # If the square is empty, add it as a valid move
                    moves.append((nx, ny))
                elif target.color != self.color:  # If it's an opponent's piece, capture and stop moving further
                    moves.append((nx, ny))
                    break
                else:
                    break  # Stop moving if it's our own piece
                nx, ny = nx + dx, ny + dy  # Move further in the same direction
        return moves  # Return the list of valid moves

# Class for Knight Piece
class Knight(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):

        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]  # Knight's L-shaped moves
        x, y = pos  # Current position of the knight
        valid_moves = []  # List to store valid moves
        for dx, dy in directions:  # Iterate over each possible L-shaped move
            nx, ny = x + dx, y + dy  # Calculate the new position
            if 0 <= nx < 8 and 0 <= ny < 8:  # Ensure the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == " " or target.color != self.color:  # Move if it's empty or an opponent's piece

                    valid_moves.append((nx, ny))
        return valid_moves  # Return the list of valid moves

# Class for Bishop Piece
class Bishop(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Bishop moves diagonally in four directions
        return self._generate_sliding_moves(board, pos, directions)  # Generate all valid moves for bishop

    # Helper method for sliding pieces (same as in Rook)
    def _generate_sliding_moves(self, board, pos, directions):
        moves = []  # List to store valid moves
        x, y = pos  # Current position of the bishop
        for dx, dy in directions:  # Iterate over each diagonal direction
            nx, ny = x + dx, y + dy  # Move in the direction
            while 0 <= nx < 8 and 0 <= ny < 8:  # While the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == ' ':  # If the square is empty, add it as a valid move
                    moves.append((nx, ny))
                elif target.color != self.color:  # If it's an opponent's piece, capture and stop moving further
                    moves.append((nx, ny))
                    break
                else:
                    break  # Stop moving if it's our own piece
                nx, ny = nx + dx, ny + dy  # Move further in the same direction
        return moves  # Return the list of valid moves

# Class for Queen Piece
class Queen(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        # Combine Rook and Bishop movement logic since Queen moves like both
        return Rook(self.color).valid_moves(board, pos) + Bishop(self.color).valid_moves(board, pos)

# Class for King Piece
class King(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # King's movement: one square in any horizontal or vertical direction
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Also one square diagonally
        ]
        moves = []  # List to store valid moves
        x, y = pos  # Current position of the king
        for dx, dy in directions:  # Iterate over each direction
            nx, ny = x + dx, y + dy  # Calculate the new position
            if 0 <= nx < 8 and 0 <= ny < 8:  # Ensure the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == ' ' or target.color != self.color:  # Move if it's empty or an opponent's piece
                    moves.append((nx, ny))
        return moves  # Return the list of valid moves

# Chess Board Setup
class ChessBoard:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn = WHITE #game starts with the player controlling the white pieces
        self.en_passant_target = None #track the target square for an en passant capture
        self.castling_rights = {
            WHITE: {'kingside': True, 'queenside': True},
            BLACK: {'kingside': True, 'queenside': True}
        } #Both players start with the ability to castle on both the kingside and queenside.


    @staticmethod
    def file_rank_to_coords(file, rank):
        # File is the letter and rank is the number

        # Returns (rank, file)
        return (int(rank) - 1, ord(file) - ord("A"))

    #creates the starting layout of the chessboard.Each list contains the pieces in their starting positions, with the black pieces at the top and white pieces at the bottom. Empty squares are represented by spaces 
    def initialize_board(self):
        return [
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)],
            [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)]
        ] 

    def print_board(self):
        piece_symbols = {
            Rook: 'R', Knight: 'N', Bishop: 'B', Queen: 'Q', King: 'K', Pawn: 'P'
        } # maps chess piece classes to their standard chess symbols.


        print("A  B  C  D  E  F  G  H\n")
        for i, row in enumerate(self.board):
            print(' '.join([f"{piece.color[0].upper()}{piece_symbols[type(piece)]}" if isinstance(piece, Piece) else '  ' for piece in row]), " ", i + 1)
        print()

    # takes a position as input and returns the piece located at that position on the board.
    def get_piece(self, pos):
        x, y = pos
        piece = self.board[x][y]
        return piece if piece != ' ' else " "

    def move_piece(self, start, end):
        sx, sy = start
        ex, ey = end
        self.board[ex][ey] = self.board[sx][sy]
        self.board[sx][sy] = ' '
        piece = self.get_piece(end)
        piece.has_moved = True  # Track if the piece has moved

    def is_valid_move(self, start, end):
        piece = self.get_piece(start)
        if not piece:
            print("No piece at start position.")
            return False
        if piece.color != self.turn:
            print("Piece belongs to the opponent.")
            return False
        valid_moves = piece.valid_moves(self, start, self.en_passant_target)
        if end not in valid_moves:
            print("End position is not a valid move.")
            return False
        return True
        
    def is_in_check(self, color):
        # Simplified check detection logic
        king_pos = None
        for x in range(8):
            for y in range(8):
                if isinstance(self.get_piece((x, y)), King) and self.get_piece((x, y)).color == color:
                    king_pos = (x, y)
                    break
        for x in range(8):
            for y in range(8):
                target_piece = self.get_piece((x, y))
                if target_piece != ' ' and target_piece.color != color:
                    if king_pos in target_piece.valid_moves(self, (x, y)):
                        return True
        return False

    def check_checkmate(self):
        for x in range(8):
            for y in range(8):
                piece = self.get_piece((x, y))
                if piece != ' ' and piece.color == self.turn:
                    for move in piece.valid_moves(self, (x, y)):
                        start = (x, y)
                        end = move
                        self.move_piece(start, end)
                        if not self.is_in_check(self.turn):
                            self.move_piece(end, start)  # Undo move
                            return False
                        self.move_piece(end, start)  # Undo move
        return True




# Game Loop without AI
def play_game():
    board = ChessBoard()

    while True:
        board.print_board()

        # Player move (simple manual input for demonstration)
        start = tuple(input(f"{board.turn.capitalize()}'s turn. Enter start position (FileRank): ").upper())
        start = ChessBoard.file_rank_to_coords(start[0], start[1])
        print(start)
        end = tuple(input("Enter the end position (FileRank): ").upper())
        end = ChessBoard.file_rank_to_coords(end[0], end[1])
        print(end)

        if board.is_valid_move(start, end):
            board.move_piece(start, end)
            
            # Switch turns
            board.turn = BLACK if board.turn == WHITE else WHITE
            
            # Check for checkmate
            if board.check_checkmate():
                print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                break
        else:
            print("Invalid move. Try again.")

# Run the game
if __name__ == "__main__":
    play_game()
