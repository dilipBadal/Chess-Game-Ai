# Chess-Game-Ai
A complete chess game using Python with a simple Ai. Two players can play against each other or a player can play against the Ai.

Technologies used: 
  1. Python and its libraries like pygame, tkinter, pandas.
  2. MySQL (Database is required to save the game)

Features:
  1. Two players(Local) or Single player support.
  2. User Login, Register and Password reset.
  3. Ability to save game.
  4. Clean Ui with sound effects.
  5. Various Themes.

How to use:
 1. Make sure you have 'Python 3.10' or later installed a 'MySQL' server running.  From the database folder, use the database file to create a database called 'gamedata'.
 2. Open the 'database' file from the source code and edit the 'user' and 'password' to your database USN and Password.
 3. Go to 'pieces.py' and in the line 132, edit the path of texture to your folder path where it is saved. 
    eg: f"C:/Users/dilip/PycharmProjects/chessAi/assets/images/imgs-{size}px/{self.color}_{self.name}.png") change this to,
        f"C:/Users/Your_Folder_Path/chessAi/assets/images/imgs-{size}px/{self.color}_{self.name}.png") 
        do not change anything else in it.
 4. Open Main.py in a code editor (I prefer Pycharm) and click on run, enjoy!!!  
