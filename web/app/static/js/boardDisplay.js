// AI object for handling turns and game operations
function AI(initialBoard, secondPlayer, isMax) {
    this.tree = new Tree(initialBoard, secondPlayer);
    this.currentRoot = this.tree.root;

    this.tree.createChildren(this.currentRoot);
    this.tree.traversal(this.currentRoot, isMax); //false if AI plays first 

    // Update current game state based on human player's move 
    this.updateRoot = function(currentBoard) {
        this.currentRoot.children.forEach((child) => {
            isEqual = arraysEqual(child.gameBoard, currentBoard);
            if (isEqual) {
                this.currentRoot = child;
            }
        })
    }

    // The AI player will choose the game board with a matching value 
    this.chooseAction = function() {
        console.log(this.currentRoot);
        let curChildren = this.currentRoot.children;
        for (let i=0; i<curChildren.length; i++) {
          if (this.currentRoot.value == curChildren[i].value) {
            this.currentRoot = curChildren[i];
            let board = curChildren[i].gameBoard;
            return board;
          }
        }
    }

    // Check if two arrays are equivalent by position and value of indices 
    function arraysEqual(arr1, arr2) {
      for(var i = 0; i < arr1.length; i++) {
          if(arr1[i] != arr2[i]) {
              return false;
          }
      }
      return true;
    } 
}

//=============================
//    Game Utility Functions
//=============================

// choose a random location to play 
function randomMove(inPlayer, gameBoard) {
    let position = Math.floor(Math.random() * Math.floor(9));
    gameBoard[position] = inPlayer;
    translate(false, gameBoard);
    return gameBoard;
}

// translate array game board to display game board
function translate(toArray, inArray) {
    locationMap = {0:'ul', 1:'um', 2:'ur', 3:'ml', 4:'mm', 5:'mr', 6:'ll', 7:'lm', 8:'lr'};

    if (toArray) {
        gameBoard = []
        for (let i=0; i<9; i++) {
            let box = document.querySelector('#' + locationMap[i]);
            let play = box.textContent;
            gameBoard.push(play);
        }
        return gameBoard; 
    } else {
        for (let i=0; i<9; i++) {
            let box = document.querySelector('#' + locationMap[i]);
            box.textContent = inArray[i];
            if (inArray[i] != "") {
              draw(locationMap[i], inArray[i]);
            }
        }
    }
}

//Draw an X in the box selected by the user
function draw(id, player) {
  let box = document.querySelector('#' + id);
  box.textContent = player;

  //Add player (X || O) to classlist when box is filled
  box.classList.toggle(player);
}


