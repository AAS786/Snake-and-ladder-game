import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt

class SnakeAndLadder:
    def __init__(self, num_players, player_colors):
        self.board = {i: i for i in range(1, 101)}
        self.ladders = {2: 23, 8: 34, 20: 77, 32: 68, 41: 79, 74: 88}
        self.snakes = {25: 4, 39: 3, 47: 13, 56: 37, 85: 56, 99: 27}
        self.players = {i: 0 for i in range(1, num_players + 1)}  # All players start outside the board
        self.player_colors = player_colors
        self.current_player = 1
        self.setup_board()

    def setup_board(self):
        for start, end in self.ladders.items():
            self.board[start] = end
        for start, end in self.snakes.items():
            self.board[start] = end

    def move_player(self, player, steps):
        if self.players[player] == 0 and steps == 6:
            self.players[player] = 1  # Move player to the starting position
        elif self.players[player] != 0 and self.players[player] + steps <= 100:
            self.players[player] += steps
            self.players[player] = self.board[self.players[player]]
        if steps != 6 or (95 <= self.players[player] <= 99):
            self.current_player = (self.current_player % len(self.players)) + 1

    def get_player_position(self, player):
        return self.players[player]

    def get_current_player(self):
        return self.current_player

    def check_winner(self):
        for player, position in self.players.items():
            if position == 100:
                return player
        return None

# Initialize game state
if 'num_players' not in st.session_state:
    st.session_state.num_players = 4
if 'player_colors' not in st.session_state:
    st.session_state.player_colors = ['yellow', 'blue', 'red', 'green']

if 'game' not in st.session_state:
    st.session_state.game = SnakeAndLadder(st.session_state.num_players, st.session_state.player_colors)
if 'steps' not in st.session_state:
    st.session_state.steps = 0

# Define button actions
def roll_dice():
    steps = random.randint(1, 6)
    st.session_state.steps = steps
    current_player = st.session_state.game.get_current_player()
    st.session_state.game.move_player(current_player, steps)

# Plot the board
def plot_board():
    board_img = np.zeros((10, 10, 3), dtype=int)
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Color the cells and add numbers
    for row in range(10):
        for col in range(10):
            if row % 2 == 0:
                num = 1 + (row * 10) + col
            else:
                num = 1 + (row * 10) + (9 - col)
                
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                color = (255, 192, 203)  # Light Pink
            else:
                color = (210, 180, 140)  # Light Brown
            board_img[row, col, :] = color

            # Highlight ladders and snakes
            if num in st.session_state.game.ladders:
                ax.text(col + 0.5, 9 - row + 0.5, f"L{num}->{st.session_state.game.ladders[num]}", 
                        ha='center', va='center', color='blue', fontsize=8)
            elif num in st.session_state.game.snakes:
                ax.text(col + 0.5, 9 - row + 0.5, f"S{num}->{st.session_state.game.snakes[num]}", 
                        ha='center', va='center', color='red', fontsize=8)
            else:
                ax.text(col + 0.5, 9 - row + 0.5, f"{num}", ha='center', va='center', fontsize=10, fontweight='bold')

    ax.imshow(board_img, extent=[0, 10, 0, 10], origin='lower')
    ax.set_xticks([])
    ax.set_yticks([])

    # Plot players
    for player, position in st.session_state.game.players.items():
        if position == 0:  # Players outside the board
            ax.plot(-1, 10 - player, 'o', color=st.session_state.game.player_colors[player - 1], markersize=20)
            ax.text(-1, 10 - player, player, ha='center', va='center', color='black', fontsize=12)
        else:
            row, col = divmod(position - 1, 10)
            if row % 2 == 1:
                col = 9 - col
            ax.plot(col + 0.5, 9 - row + 0.5, 'o', color=st.session_state.game.player_colors[player - 1], markersize=20)
            ax.text(col + 0.5, 9 - row + 0.5, player, ha='center', va='center', color='black', fontsize=12)

    st.pyplot(fig)

# Game controls
st.title("**Snake and Ladder Game**")

# Sidebar for player settings
st.sidebar.title("Game Settings")

# Select number of players
st.session_state.num_players = st.sidebar.selectbox("Select Number of Players", options=[2, 3, 4], index=2)
player_colors = ['yellow', 'blue', 'red', 'green']

# Select player colors
for i in range(st.session_state.num_players):
    st.session_state.player_colors[i] = st.sidebar.selectbox(f"Select Color for Player {i+1}", options=player_colors, index=i)

# Reinitialize game with selected number of players and colors
if st.sidebar.button("Start New Game"):
    st.session_state.game = SnakeAndLadder(st.session_state.num_players, st.session_state.player_colors)

# Display the current player's turn and roll dice
if st.button("**Roll Dice**"):
    roll_dice()
    st.write(f"**Player {st.session_state.game.get_current_player()}'s turn**")

# Display dice roll
st.write(f"**Dice Roll: {st.session_state.steps}**")

# Plot the board
plot_board()

# Check for winner
winner = st.session_state.game.check_winner()
if winner:
    st.write(f"**Player {winner} wins!**")
