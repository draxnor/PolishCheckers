# PolishCheckers
A International Checkers (Polish version)  game written in Python, Pygame.

AI is using minimax algorithm with alpha-beta pruning.

Project built as Python and OOP practice.

# General features

### Sample gameplay

 ![til](./showoff/gifs/ai_v_h.gif)


## Game rules

Game follows the rules included in:
https://en.wikipedia.org/wiki/International_draughts

### Game objective:

The objective of the game is to capture all the pieces of the enemy or make enemy player unable to perform any move.

### Victory conditions:
- Enemy player is unable to perform any valid move due to lack of pieces or due to his pieces being blocked by other pieces.

### Draw conditions:
- The same position repeats itself for the third time (not necessarily consecutive), with the same player having the move each time.
- During 25 consecutive moves, there were only king movements, without piece movements or jumps.
- When there is only 1 queen vs (1 queen + 2 pieces or queens), each player can play 16 turns till game ends as a draw.
- When there is only 1 queen vs (1 queen + 1 piece/queen), each player can play 5 turns till game ends as a draw.
- After there are only 1 queen vs 1 queen left on the board, there is only 1 last turn possible (not 1 turn per each player) till game ends as a draw.


### Most important gameplay rules:
- Game is played on 10x10 board
- Each player starts with 20 pieces
- If capturing of enemy piece is possible, it is also mandatory
- Pieces can move 1 square forward or jump over enemy pieces forward and backwards.
- Multiple successive jumps (captures) are possible.
- There is an obligation to capture as many enemy pieces as possible in one's turn.
- Queens can move forward and backward any number of squares.
- While jumping over enemy piece queens can land any number of squares behind captured piece and they can continue jumping from that chosen square.
- Piece becomes a queen at the end of player's turn, if it reached the edge of the board and stopped there.
- Pieces do not become queens in the middle of the sequence of consecutive jumps. Read rule above.

For all other details on rules, please visit link attached at the beginning of the section.

## Options
Game options can be set by selecting:
- Main Menu -> Options 

![til](./showoff/gifs/options.gif)


There one can set:
- Starting side
- Game mode
- AI difficulty

### Game modes

Game offers 3 general game modes:
- Human vs Human (default)

![til](./showoff/mp4/h_v_h.mp4)
- Human vs AI

![til](./showoff/gifs/ai_v_h.gif)

- AI vs AI

![til](./showoff/gifs/ai_v_ai.gif)


### Starting player

In the Options screen one can choose the starting side using self-explanatory buttons: *BOTTOM* and *TOP*.

Highlighted button describe currently set starting side.


### AI difficulty

AI difficulty is described by an integer, and it can be checked/changed inside Options screen in *AI DIFFICULTY* field.

Value entered into *AI DIFFICULTY* field is used as a maximum depth for *MINIMAX* algorithm with alpha-beta pruning.

*AI DIFFICULTY* fields are not rendered unless player changes Game Mode so that there is at least 1 AI player.


To change difficulty, you can enter any integer from 0 to 9. 
To confirm changes press *Enter* or *left-click* on app screen.

Note that entering any number higher than 6 will end up in long computing time.

Entering incorrect characters ends up in no changes.
Any number higher than 9 will be trimmed so that first digit will be set as your difficulty level.


## Gameplay

Podświetlanie poprzedniej tury

Podświetlanie dozwolonych ruchów wybranego piona

Restart gry SPACE

Powrót do Menu ESCAPE

