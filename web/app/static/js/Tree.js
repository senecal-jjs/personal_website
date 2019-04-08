function Tree(gameBoard, secondPlayer) {
    this.root = new Node(gameBoard, secondPlayer); //X

    // Create branches for children based on available moves
    this.createChildren = function makeChildren(inRoot) {
        let nextPlayer = "";
        let availableMoves = [];

        // Check whose move it is 
        if (inRoot.currentPlayer == "X") {
            nextPlayer = "O";
        } else {
            nextPlayer = "X";
        }

        // Find valid move locations
        for (let i=0; i<9; i++) {
            if (inRoot.gameBoard[i] == "") {
                availableMoves.push(i);
            }
        }

        // Create child nodes based on available moves 
        for (let i=0; i<availableMoves.length; i++) {
            let newGameBoard = Array.from(inRoot.gameBoard);
            newGameBoard[availableMoves[i]] = inRoot.currentPlayer;
            let child = new Node(newGameBoard, nextPlayer);
            if (child.isFinal()) {
                child.isLeaf = true;
                child.value = child.evaluateBoard();
            } 
            inRoot.children.push(child);
        }

        // Recursively create children for each of the newly created children
        inRoot.children.forEach(function(element) {
            if (!element.isLeaf) {
                makeChildren(element);
            }
        });
    }

    this.traversal = function postorder(node, isMaxPlayer) {
        if (node.isLeaf) {
            return;
        }

        // recur on children
        node.children.forEach(function(element) {
            postorder(element, !isMaxPlayer);
        });

        childValues = []
        node.children.forEach(function(element) {
            childValues.push(element.value);
        })

        //update parent node with maximin strategy 
        if (isMaxPlayer) {
            node.value = Math.max(...childValues);
        } else {
            node.value = Math.min(...childValues);
        }
    }
}