from checkers.Board import Board

def run_test():
    board_org = Board()
    board_copied = board_org
    board_deepcopied = board_org.deepcopy()
    board_copied.board[0][0] = 0
    board_copied.board[0][1] = 1

    board_deepcopied.board[0][0] = 6
    board_deepcopied.board[0][1] = 6


    print('Original:')
    print(board_org.board[0])

    print('Copy:')
    print(board_copied.board[0])

    print('Copy:')
    print(board_deepcopied.board[0])


if __name__ == '__main__':
    run_test()