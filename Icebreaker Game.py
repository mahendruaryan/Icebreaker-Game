#3145291
#Milestone 3 Icebreaker
from graphics import *

class Icebreaker:    
    """
    Purpose: to initialize the icebreaker game with 5*5 board size and creating the game window
    Parameters: board_size (tuple): the dimensions of the game board defaults to (5, 5)
    Returns:None
    """
    def __init__(self, board_size=(5, 5)):
        self.show_splash_screen()
        self.board_size = board_size
        self.win = GraphWin("Icebreaker by Aryan Mahendru Milestone 3 08 April 2024", 600, 620)
        self.players = [Player("red", (0, 0)), Player("blue", (4, 4))] 
        self.board = Board(self.win, board_size, self.players)
        self.status_message = Text(Point(300, 570), "Player 0 Turn: Move")
        self.additional_status_message = Text(Point(300, 600), "MOUSE") 
        self.status_message.draw(self.win)
        self.additional_status_message.draw(self.win) 
        self.create_buttons()
        self.current_player = self.players[0]
        self.current_task = 'move'

    def show_splash_screen(self):
        """
        Purpose: to show a splash screen before the game starts
        Parameters: None
        Returns: None
        """
        splash_win = GraphWin("Icebreaker Splash Screen", 400, 400)
        splash_win.setBackground("Yellow")
        splash_win.setCoords(0, 0, 400, 400)

        text = Text(Point(200, 350), "Welcome to the Icebreaker game\nThis game is written in part by Aryan Mahendru\nfor CMPT 103, Winter session 2024")
        text.setSize(12)
        text.draw(splash_win)

        play_button_rect = Rectangle(Point(100, 170), Point(300, 230))
        play_button_rect.setFill('green')
        play_button_rect.draw(splash_win)
        play_button = Text(Point(200, 200), "Play Game")
        play_button.draw(splash_win)

        no_thanks_button_rect = Rectangle(Point(100, 100), Point(300, 160))
        no_thanks_button_rect.setFill('red')
        no_thanks_button_rect.draw(splash_win)
        no_thanks_button = Text(Point(200, 130), "No Thanks")
        no_thanks_button.draw(splash_win)

        while True:
            click_point = splash_win.getMouse()
            if self.is_button_clicked(click_point, play_button_rect):
                splash_win.close()
                break
            elif self.is_button_clicked(click_point, no_thanks_button_rect):
                splash_win.close()
                self.win.close()
                exit()                 

    def create_buttons(self):
        """
        Purpose: to create quit and reset buton
        Parameters:None
        Returns:None
        """
        self.quit_button_rect = Rectangle(Point(50, 570), Point(150, 590))
        self.quit_button_rect.setFill('red')
        self.quit_button_rect.draw(self.win)
        self.quit_button = Text(Point(100, 580), "QUIT")
        self.quit_button.draw(self.win)

        self.reset_button_rect = Rectangle(Point(450, 570), Point(550, 590))
        self.reset_button_rect.setFill('green')
        self.reset_button_rect.draw(self.win)
        self.reset_button = Text(Point(500, 580), "RESET")
        self.reset_button.draw(self.win)

    def play(self):
        """
        Purpose: handling mouse clicks for playing the game or quitting or resetting
        Parameters:None
        Returns:None
        """        
        while True:
            click_point = self.win.getMouse()
            if self.is_button_clicked(click_point, self.quit_button_rect):
                self.additional_status_message.setText("BYE BYE !!")
                self.win.getMouse()
                self.win.close()
                break
            elif self.is_button_clicked(click_point, self.reset_button_rect):
                self.players[0].position = (0, 0)  
                self.players[1].position = (4, 4)  
                self.board.reset_board() 
                self.board.update_player_position(self.players[0])
                self.board.update_player_position(self.players[1])
                self.current_player = self.players[0]
                self.current_task = 'move'
                for player in self.players:
                    player.wins=0 
                self.update_status_messages("Player 0 turn: Move", "RESET")
            else:
                self.handle_board_click(click_point)                 

                    

    def display_score_screen(self):
        """
        Purpose: to show a score screen when a player looses
        Parameters: None
        Returns: None
        """
        score_win = GraphWin("Game Score", 300, 200)
        score_win.setBackground("cyan")

        player0_score = Text(Point(150, 50), f"Player 0: {self.players[0].wins}")
        player1_score = Text(Point(150, 80), f"Player 1: {self.players[1].wins}")
        player0_score.draw(score_win)
        player1_score.draw(score_win)

        next_round_button = Rectangle(Point(75, 120), Point(225, 150))
        next_round_button.setFill('magenta')
        next_round_button.draw(score_win)
        next_round_text = Text(next_round_button.getCenter(), "Next Round")
        next_round_text.draw(score_win)

        no_thanks_button = Rectangle(Point(75, 160), Point(225, 190))
        no_thanks_button.setFill('magenta')
        no_thanks_button.draw(score_win)
        no_thanks_text = Text(no_thanks_button.getCenter(), "No Thanks")
        no_thanks_text.draw(score_win)

        while True:
            click_point = score_win.getMouse()
            if self.is_button_clicked(click_point, next_round_button):
                score_win.close()
                self.reset_board_for_new_round()
                break
            elif self.is_button_clicked(click_point, no_thanks_button):
                score_win.close()
                self.win.close()
                exit()
    
    def reset_board_for_new_round(self):
        """
        Purpose: reset board when a player looses for a new round
        Parameters: None
        Returns: None
        """
        self.players[0].position = (0, 0)
        self.players[1].position = (4, 4)
        self.board.reset_board()
        for player in self.players:
            self.board.update_player_position(player)
        self.current_player = self.players[0]
        self.current_task = 'move'
        self.update_status_messages("Player 0 turn: Move", "NEW ROUND")                    



    def handle_board_click(self, click_point):
        """
        Purpose: Handles mouse click events on the game board during gameplay.
        Parameters:- click_point (Point): The coordinates of the click event on the window.
        Returns:None
        """
        if self.current_task == 'move' and self.board.is_click_inside_board(click_point):
            if self.current_player.player_clicked(click_point, self.board):
                self.board.update_player_position(self.current_player) 
                player_can_move = [player.can_move(self.board) for player in self.players]
                if all(player_can_move):
                    self.current_task = 'break'
                    self.update_status_messages(f"PLAYER {self.players.index(self.current_player)}: Break ICE",f"PLAYER {self.players.index(self.current_player)}: Moved to {self.current_player.position}")
                else:
                    winner_index = player_can_move.index(True)  
                    self.players[winner_index].wins += 1  
                    self.update_status_messages(f"PLAYER {winner_index}: WIN", "")
                    self.display_score_screen()
                    

            else:
                self.additional_status_message.setText("Not a valid move")
        elif self.current_task == 'break' and self.board.is_click_inside_board(click_point):
            if self.board.break_ice(click_point):
                player_can_move = [player.can_move(self.board) for player in self.players]
                if all(player_can_move):  
                    self.switch_players()
                    self.update_status_messages(f"PLAYER {self.players.index(self.current_player)}: {self.current_player.position} MOVE","Ice broken")
                else:
                    winner_index = player_can_move.index(True)  
                    self.players[winner_index].wins += 1  
                    self.update_status_messages(f"PLAYER {winner_index}: WIN", "")
                    self.display_score_screen()  
            else:
                self.additional_status_message.setText("Not a valid move")


    def switch_players(self):
        """
        Purpose:Switches the current player to the other player and updates the game state.
        Parameters:None
        Returns:None
        """
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        self.current_task = 'move'
        self.status_message.setText(f"PLAYER {self.players.index(self.current_player)}: {self.current_player.position} MOVE")


    def update_status_messages(self, player_status, click_status):
        """
        Purpose:Updates the status messages displayed on the game window.
        Parameters:   - player_status (str): The main status message to be displayed, typically indicating the current player and task
                      - click_status (str): The additional status message to be displayed, typically indicating the outcome of the last action
        Returns:None              
        """
        self.status_message.setText(player_status)
        self.additional_status_message.setText(click_status)


    def is_button_clicked(self, click_point, button_rect):
        """
        Purpose:To determine if a mouse click is within the bounds of a button
        Parameters: click_point (Point): The point where the mouse was clicked
                    button_rect (Rectangle): The rectangle defining the buttons boundaries
        Returns: bool: true if the button was clicked otherwise false
        """
        x_min = button_rect.getP1().getX()
        x_max = button_rect.getP2().getX()
        y_min = button_rect.getP1().getY()
        y_max = button_rect.getP2().getY()
        return x_min <= click_point.getX() <= x_max and y_min <= click_point.getY() <= y_max
    




class Board:
    def __init__(self, win, board_size, players):
        """
        Purpose: initialize the game board as a 2D grid of squares 
        Parameters: win (GraphWin): the main game window in which the board is displayed
                    board_size (tuple): the dimensions of the game board
        Returns:None
        """
        self.win = win
        self.board_size = board_size
        self.players = players
        self.squares = []
        self.player_circles = []
        self.occupied_positions = set()  
        self.initialize_board()

    def initialize_board(self):
        """
        Purpose: draw the game board on the window
        Parameters:None
        Returns:None
        """
        for i in range(self.board_size[0]):
            row = []
            for j in range(self.board_size[1]):
                square = Rectangle(Point(j*100+50, i*100+50), Point(j*100+150, i*100+150))
                square.setFill("white")
                square.draw(self.win)
                row.append(square)
            self.squares.append(row)

        for player in self.players:
            position = player.position
            circle = Circle(Point(position[0]*100+100, position[1]*100+100), 30)
            circle.setFill(player.color)
            circle.draw(self.win)
            self.player_circles.append(circle)
              


    def update_player_position(self, player):
        """
        Purpose: updates the graphical representation of a player position on the board
        Parameters:- player (Player): The player whose position has been updated and needs to be redrawn
        Returns:None 
        """
        new_circle_position = Point(player.position[0]*100+100, player.position[1]*100+100)
        for i, p in enumerate(self.players):
            if p == player:
                self.player_circles[i].undraw()  # Remove the old circle
                new_circle = Circle(new_circle_position, 30)
                new_circle.setFill(player.color)
                new_circle.draw(self.win)
                self.player_circles[i] = new_circle  

    def is_occupied(self, position):
        """
        Purpose:Checks if a given position on the board is currently occupied
        Parameters:- position (tuple): A tuple of (x, y) coordinates representing the position to check.
        Returns:bool: true if the position is occupied otherwise false
        """
        return position in self.occupied_positions

    def break_ice(self, click_point):
        """
        Purpose:Handles the action of breaking ice at a specified position on the board.
        Parameters:- click_point (Point): the point where the mouse was clicked indicating the square to break ice at
        Returns: bool: True if the ice was successfully broken at the specified position False if the action is invalid
        """
        position = self.get_board_coordinates(click_point)

        if position in [player.position for player in self.players]:
            return False  

        if position not in self.occupied_positions:
            square = self.squares[position[1]][position[0]]
            square.setFill("light blue")
            self.occupied_positions.add(position)
            return True
        else:
            return False



    def reset_board(self):
        """
        Purpose: to reset all squares on the board, restarting the game
        Parameters:None
        Returns:None
        """
        for row in self.squares:
            for square in row:
                square.setFill("white")
        self.occupied_positions.clear()    

    def is_click_inside_board(self, click_point):
        """
        Purpose:to check if a given mouse click is within the game board
        Parameters:click_point (Point): the point where the mouse was clicked
        Returns:bool: true if the click is inside the board otherwise false
        """
        return 50 <= click_point.getX() <= 50 + self.board_size[1]*100 and 50 <= click_point.getY() <= 50 + self.board_size[0]*100
    
    def get_board_coordinates(self, click_point):
        """
        Convert click coordinates to board indices.
        Parameters:
            click_point (Point): The point where the mouse was clicked.
        Returns:
            tuple: A tuple representing the board coordinates (x, y).
        """
        x_index = int((click_point.getX() - 50) / 100)
        y_index = int((click_point.getY() - 50) / 100)
        return (x_index, y_index)
    
class Player:
    def __init__(self, color, start_position):
        """
        Purpose:initializes a new player with a color and  position
        Parameters:- color (str): The color of the player
                    - start_position (tuple): The starting position of the player on the board as (x, y) coordinates
        Returns:None            
        """
        self.color = color
        self.position = start_position
        self.wins = 0  

    

    def move_player(self, new_position):
        """
        Purpose:updates the player position to a new location
        Parameters:- new_position (tuple): The new position for the player as a tuple of (x, y) coordinates
        Returns:None
        """
        self.position = new_position

    def player_clicked(self, click_point, board):
        """
        Purpose:processes a player move based on a mouse click on the game board
        Parameters:- click_point (Point): The coordinates of the click event on the window
                - board (Board): The game board object, used to check if the clicked position is occupied
        Returns:bool: True if the move was successful false otherwise
        """
        x_index, y_index = board.get_board_coordinates(click_point)
        new_position = (x_index, y_index)

        if new_position == self.position:
            return False  

        if self.is_adjacent(new_position) and not board.is_occupied(new_position) and not any(p.position == new_position for p in board.players if p != self):
            self.move_player(new_position)
            return True
        else:
            return False

    def is_adjacent(self, new_position):
        """
        Purpose:checks if a given position is adjacent to the player current position
        Parameters:- new_position (tuple): The target position as a tuple of (x, y) coordinates.
        Returns:bool: true if the target position is adjacent to the player current position otherwise false
        """
        x, y = self.position
        x_new, y_new = new_position
        return abs(x - x_new) <= 1 and abs(y - y_new) <= 1
    
    def can_move(self, board):
        """
        Purpose: check if the player can move to any adjacent squares
        Parameters: board (Board): The game board object to check for adjacent squares
        Returns: bool: true if the player can move otherwise false
        """
        x, y = self.position
        directions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]  # Diagonal movements

        for new_position in directions:
            if (0 <= new_position[0] < board.board_size[0]) and (0 <= new_position[1] < board.board_size[1]):
                if not board.is_occupied(new_position)and not any(p.position == new_position for p in board.players):
                    return True  
        return False 

def main():
    game = Icebreaker((5, 5))  
    game.play()

if __name__ == "__main__":
    main()

