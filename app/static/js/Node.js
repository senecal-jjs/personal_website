function Node(gameBoard, currentPlayer) {
    this.gameBoard = gameBoard;
    this.children = [];
    this.currentPlayer = currentPlayer;
    this.value = 0;
    this.isLeaf = false;
    
    // On terminal boards evaluate winner or loser
    this.evaluateBoard = function() {
        //Check top row win, human player is X
        if (this.gameBoard[0] == "O" && this.gameBoard[1] == "O" && this.gameBoard[2] == "O") {
            return 1;
        } else if (this.gameBoard[0] == "X" && this.gameBoard[1] == "X" && this.gameBoard[2] == "X") {
            return -1;
        }

        //Check mid row horizontal win
        if (this.gameBoard[3] == "O" && this.gameBoard[4] == "O" && this.gameBoard[5] == "O") {
            return 1;
        } else if (this.gameBoard[3] == "X" && this.gameBoard[4] == "X" && this.gameBoard[5] == "X") {
            return -1;
        }

        // Check bottom row horizontal row
        if (this.gameBoard[6] == "O" && this.gameBoard[7] == "O" && this.gameBoard[8] == "O") {
            return 1;
        } else if (this.gameBoard[6] == "X" && this.gameBoard[7] == "X" && this.gameBoard[8] == "X") {
            return -1;
        }

        // Check left row vertical win
        if (this.gameBoard[0] == "O" && this.gameBoard[3] == "O" && this.gameBoard[6] == "O") {
            return 1;
        } else if (this.gameBoard[0] == "X" && this.gameBoard[3] == "X" && this.gameBoard[6] == "X") {
            return -1;
        }

        // Check mid row vertical win
        if (this.gameBoard[1] == "O" && this.gameBoard[4] == "O" && this.gameBoard[7] == "O") {
            return 1;
        } else if (this.gameBoard[1] == "X" && this.gameBoard[4] == "X" && this.gameBoard[7] == "X") {
            return -1;
        }

        // Check right row vertical win
        if (this.gameBoard[2] == "O" && this.gameBoard[5] == "O" && this.gameBoard[8] == "O") {
            return 1;
        } else if (this.gameBoard[2] == "X" && this.gameBoard[5] == "X" && this.gameBoard[8] == "X") {
            return -1;
        }

        // Check left to right diag
        if (this.gameBoard[0] == "O" && this.gameBoard[4] == "O" && this.gameBoard[8] == "O") {
            return 1;
        } else if (this.gameBoard[0] == "X" && this.gameBoard[4] == "X" && this.gameBoard[8] == "X") {
            return -1;
        }

        // Check right to left diag
        if (this.gameBoard[2] == "O" && this.gameBoard[4] == "O" && this.gameBoard[6] == "O") {
            return 1;
        } else if (this.gameBoard[2] == "X" && this.gameBoard[4] == "X" && this.gameBoard[6] == "X") {
            return -1;
        }

        // If none of the above conditions have been met the game is a draw or not finished 
        return 0; 
    };

    // Test if board is terminal board 
    this.isFinal = function() {
        boardFull = true;

        for (let i=0; i<this.gameBoard.length; i++) {
            if (this.gameBoard[i] == "") {
                boardFull = false;
            }
        }

        if (0 == this.evaluateBoard() && !boardFull) {
            return false;
        }
        return true; 
    }
}